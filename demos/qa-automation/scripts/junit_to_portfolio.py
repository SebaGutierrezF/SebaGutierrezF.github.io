"""Convert real pytest JUnit XML results to safe offline HTML/JSON evidence."""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
from html import escape
import json
from pathlib import Path
import xml.etree.ElementTree as ET


def parse_junit(xml_path: Path) -> dict:
    root = ET.parse(xml_path).getroot()
    if root.tag not in {"testsuite", "testsuites"}:
        raise ValueError("La raíz de JUnit debe ser testsuite o testsuites")
    cases = []
    for node in root.iter("testcase"):
        if node.find("error") is not None:
            status = "ERROR"
        elif node.find("failure") is not None:
            status = "FAILED"
        elif node.find("skipped") is not None:
            status = "SKIPPED"
        else:
            status = "PASSED"
        cases.append({"name": node.attrib.get("name", "(sin nombre)"),
                      "class": node.attrib.get("classname", ""),
                      "status": status,
                      "seconds": node.attrib.get("time", "")})
    if not cases:
        raise ValueError("El XML no contiene casos de prueba; no se puede afirmar PASS")
    counts = Counter(c["status"] for c in cases)
    return {"source": "pytest JUnit XML real proporcionado por el ejecutor",
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            "total": len(cases), "counts": {s: counts[s] for s in ("PASSED", "FAILED", "ERROR", "SKIPPED")},
            "overall": "PASS" if counts["PASSED"] == len(cases) else "NOT_PASS",
            "cases": cases}


def write_report(data: dict, outdir: Path) -> None:
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "summary.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    rows = "\n".join(
        f"<tr><td>{escape(t['name'])}</td><td>{escape(t['class'])}</td>"
        f"<td><span class='{escape(t['status'].lower())}'>{t['status']}</span></td>"
        f"<td>{escape(t['seconds'])}</td></tr>" for t in data["cases"]
    )
    counts = data["counts"]
    html = f"""<!doctype html><html lang='es'><head><meta charset='utf-8'>
    <meta name='viewport' content='width=device-width,initial-scale=1'>
    <title>Evidencia QA · {escape(data['overall'])}</title>
    <style>body{{background:#0b1220;color:#e8eef7;font:16px system-ui;margin:0 auto;max-width:980px;padding:42px 24px}}
    h1{{font-size:32px}}p{{color:#9dacbf}}.metrics{{display:flex;flex-wrap:wrap;gap:12px;margin:22px 0}}
    .metric{{background:#172235;border:1px solid #33435d;border-radius:12px;padding:16px;min-width:135px}}
    .metric strong{{display:block;font-size:28px}}table{{width:100%;border-collapse:collapse;margin-top:20px}}
    th,td{{text-align:left;border-bottom:1px solid #293850;padding:13px 9px}}th{{color:#b4c5da}}
    .passed{{color:#6ee7b7}}.failed,.error{{color:#fda4af}}.skipped{{color:#fbd38d}}
    small{{color:#a3b5cb}}</style></head><body>
    <small>Informe generado desde XML JUnit (no es un resultado predefinido)</small>
    <h1>QA Automation · {escape(data['overall'])}</h1>
    <p>Fecha UTC: {escape(data['generated_at_utc'])}</p>
    <div class='metrics'><div class='metric'>Total<strong>{data['total']}</strong></div>
    <div class='metric'>Aprobados<strong>{counts['PASSED']}</strong></div>
    <div class='metric'>Fallidos<strong>{counts['FAILED']}</strong></div>
    <div class='metric'>Errores<strong>{counts['ERROR']}</strong></div>
    <div class='metric'>Omitidos<strong>{counts['SKIPPED']}</strong></div></div>
    <table><thead><tr><th>Prueba</th><th>Clase</th><th>Estado</th><th>Segundos</th></tr></thead><tbody>{rows}</tbody></table>
    <p>Fuente: resultados de pytest. Ejecutar contra la aplicación de demostración local; no representa un cliente real.</p>
    </body></html>"""
    (outdir / "index.html").write_text(html, encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("junit", type=Path)
    p.add_argument("--output", type=Path, default=Path("evidence"))
    args = p.parse_args()
    data = parse_junit(args.junit)
    write_report(data, args.output)
    print(f"REPORT={args.output / 'index.html'} TOTAL={data['total']} STATUS={data['overall']}")
    return 0 if data["overall"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
