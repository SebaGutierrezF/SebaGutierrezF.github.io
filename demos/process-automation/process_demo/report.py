"""Write deterministic, local, clearly-labeled reports for a synthetic dry-run."""
from __future__ import annotations
from datetime import datetime,timezone
from html import escape
import json
from pathlib import Path
from .engine import Decision,summarize


def render_report(decisions: list[Decision],summary: dict,generated_at: str) -> str:
    rows = '\n'.join('<tr>' + ''.join(f'<td>{escape(str(cell))}</td>' for cell in
        (d.row,d.request_id,d.account_id,d.action,d.outcome,d.reason))+'</tr>' for d in decisions)
    return f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Automatización de procesos · DRY RUN</title>
    <style>body{{margin:0 auto;max-width:1150px;padding:38px 24px;background:#0a1220;color:#eff5ff;font:16px system-ui}}
    h1{{font-size:32px}}p,small{{color:#abbad0}}.kpis{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px}}
    .kpi{{padding:16px;background:#1b2a40;border:1px solid #344560;border-radius:12px}}.kpi b{{display:block;font-size:28px}}
    table{{width:100%;border-collapse:collapse;margin-top:24px;font-size:14px}}th,td{{padding:12px 8px;border-bottom:1px solid #344560;text-align:left;vertical-align:top}}
    th{{color:#c4d8ec}} .scroller{{overflow-x:auto}}.notice{{border-left:3px solid #8ca8d6;padding:9px 16px;background:#152137}}</style></head>
    <body><small>Portafolio de Python · dataset ficticio · {escape(generated_at)}</small>
    <h1>Automatización de procesos</h1><p class="notice"><strong>DRY RUN EXCLUSIVAMENTE.</strong> Ninguna acción real ejecutada. No representa un sistema de clientes ni valida KPIs de una empresa.</p>
    <div class="kpis"><div class="kpi">Solicitudes<b>{summary['total']}</b></div>
    <div class="kpi">Elegibles (sin ejecutar)<b>{summary['would_execute']}</b></div>
    <div class="kpi">En espera<b>{summary['hold']}</b></div>
    <div class="kpi">Revisión manual<b>{summary['review']}</b></div>
    <div class="kpi">Omitidas<b>{summary['skip']}</b></div>
    <div class="kpi">Mutaciones externas<b>0</b></div></div>
    <div class="scroller"><table><thead><tr><th>Fila</th><th>Solicitud</th><th>Cuenta ficticia</th><th>Operación</th><th>Decisión</th><th>Motivo</th></tr></thead>
    <tbody>{rows}</tbody></table></div>
    <p>Datos generados para demostración pública, sin integración con WOM Chile ni otros servicios.</p></body></html>"""


def write_evidence(decisions: list[Decision],output:Path)->dict:
    output.mkdir(parents=True,exist_ok=True)
    summary=summarize(decisions)
    timestamp=datetime.now(timezone.utc).isoformat()
    (output/'summary.json').write_text(json.dumps({'generated_at_utc':timestamp,**summary},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    with (output/'audit.jsonl').open('w',encoding='utf-8',newline='\n') as f:
        for d in decisions:
            f.write(json.dumps({'mode':'DRY_RUN_ONLY','generated_at_utc':timestamp,**d.to_dict()},ensure_ascii=False)+'\n')
    (output/'report.html').write_text(render_report(decisions,summary,timestamp),encoding='utf-8')
    return summary
