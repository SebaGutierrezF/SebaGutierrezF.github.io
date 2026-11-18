"""Command-line entry point; no --apply option by design."""
from __future__ import annotations
import argparse
from pathlib import Path
from .engine import process_files
from .report import write_evidence


def main(argv: list[str]|None=None)->int:
    parser=argparse.ArgumentParser(description='Conciliación sintética segura. Solo DRY RUN, sin APIs.')
    parser.add_argument('--requests',type=Path,required=True)
    parser.add_argument('--accounts',type=Path,required=True)
    parser.add_argument('--output',type=Path,default=Path('evidence'))
    args=parser.parse_args(argv)
    output=args.output.resolve()
    if output in {args.requests.resolve(),args.accounts.resolve()}:
        parser.error('El destino no puede ser un archivo de entrada')
    for filename in ('summary.json','audit.jsonl','report.html'):
        target=(output/filename).resolve()
        if target in {args.requests.resolve(),args.accounts.resolve()}:
            parser.error('La salida no puede sobrescribir archivos de entrada')
    try:
        decisions=process_files(args.requests,args.accounts)
        summary=write_evidence(decisions,output)
    except (ValueError,OSError) as exc:
        parser.error(str(exc))
    print(f"MODE=DRY_RUN_ONLY TOTAL={summary['total']} ELIGIBLE={summary['would_execute']} "
          f"HOLD={summary['hold']} REVIEW={summary['review']} SKIP={summary['skip']} EXTERNAL_MUTATIONS=0")
    print(f'REPORT={output / "report.html"}')
    return 0

if __name__=='__main__':
    raise SystemExit(main())
