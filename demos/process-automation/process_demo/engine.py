"""Pure decision engine for a fictitious business process: no network, no mutations."""
from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass
import csv
from pathlib import Path
import re

REQ_FIELDS = ('request_id', 'account_id', 'action', 'target_plan', 'approved')
ACCOUNT_FIELDS = ('account_id', 'status', 'plan')
ACTIONS = {'ACTIVATE', 'CANCEL', 'CHANGE_PLAN'}
PLANS = {'BASIC', 'PLUS', 'PRO'}
ID_PATTERN = re.compile(r'^[A-Za-z0-9_-]{1,40}$')


@dataclass(frozen=True)
class Decision:
    row: int
    request_id: str
    account_id: str
    action: str
    outcome: str
    reason: str
    target_plan: str = ''

    def to_dict(self) -> dict:
        return asdict(self)


def load_csv(path: Path, expected_fields: tuple[str,...]) -> list[dict[str,str]]:
    if not path.is_file():
        raise ValueError(f'No se encuentra el archivo de entrada: {path}')
    with path.open('r',encoding='utf-8-sig',newline='') as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != list(expected_fields):
            raise ValueError(f'Encabezado incorrecto de {path.name}; esperado: {expected_fields}')
        rows = []
        for line_num, row in enumerate(reader,start=2):
            if any(k is None or v is None for k,v in row.items()):
                raise ValueError(f'Fila CSV irregular: {path.name}:{line_num}')
            rows.append({k: v.strip() for k,v in row.items()})
    return rows


def make_account_index(rows: list[dict[str,str]]) -> dict[str,dict[str,str]]:
    index = {}
    for n, row in enumerate(rows,start=2):
        key = row['account_id']
        if not ID_PATTERN.fullmatch(key) or key in index:
            raise ValueError(f'ID inválido o duplicado en accounts.csv, fila {n}')
        status = row['status'].upper()
        plan = row['plan'].upper()
        if status not in {'ACTIVE','INACTIVE'} or plan not in PLANS:
            raise ValueError(f'Estado o plan inválidos en accounts.csv, fila {n}')
        index[key] = {'status':status,'plan':plan}
    return index


def evaluate(requests: list[dict[str,str]], accounts: dict[str,dict[str,str]]) -> list[Decision]:
    seen_request_ids = set()
    planned_accounts = set()
    decisions = []
    for line_num, row in enumerate(requests,start=2):
        request_id = row['request_id']
        account_id = row['account_id']
        action = row['action'].upper()
        plan = row['target_plan'].upper()
        approved = row['approved'].lower()
        outcome = ''
        reason = ''
        if not ID_PATTERN.fullmatch(request_id) or not ID_PATTERN.fullmatch(account_id):
            outcome,reason = 'REVIEW_INVALID_ID','Identificador con formato no permitido'
        elif request_id in seen_request_ids:
            outcome,reason = 'SKIP_DUPLICATE','Solicitud duplicada en el lote; no se planifica de nuevo'
        else:
            seen_request_ids.add(request_id)
            if action not in ACTIONS:
                outcome,reason = 'REVIEW_INVALID_ACTION','Acción fuera del catálogo permitido'
            elif approved not in {'true','false'}:
                outcome,reason = 'REVIEW_INVALID_APPROVAL','Aprobación debe ser true o false'
            elif approved == 'false':
                outcome,reason = 'HOLD_NOT_APPROVED','La solicitud aún no está autorizada'
            elif account_id not in accounts:
                outcome,reason = 'REVIEW_UNKNOWN_ACCOUNT','Cuenta inexistente en catálogo local'
            elif action == 'CHANGE_PLAN' and plan not in PLANS:
                outcome,reason = 'REVIEW_INVALID_PLAN','Plan objetivo inválido'
            elif action != 'CHANGE_PLAN' and plan:
                outcome,reason = 'REVIEW_UNEXPECTED_PLAN','El plan objetivo debe estar vacío para esta acción'
            elif account_id in planned_accounts:
                outcome,reason = 'HOLD_ACCOUNT_CONFLICT','Ya existe otra operación planificada para esta cuenta'
            else:
                current = accounts[account_id]
                if action == 'ACTIVATE' and current['status'] == 'ACTIVE':
                    outcome,reason = 'SKIP_ALREADY_SATISFIED','Cuenta ya está activa'
                elif action == 'CANCEL' and current['status'] == 'INACTIVE':
                    outcome,reason = 'SKIP_ALREADY_SATISFIED','Cuenta ya está inactiva'
                elif action == 'CHANGE_PLAN' and current['status'] != 'ACTIVE':
                    outcome,reason = 'HOLD_INACTIVE_ACCOUNT','No se cambia el plan de una cuenta inactiva'
                elif action == 'CHANGE_PLAN' and current['plan'] == plan:
                    outcome,reason = 'SKIP_ALREADY_SATISFIED','El plan actual coincide con el solicitado'
                else:
                    outcome,reason = 'WOULD_EXECUTE','Operación elegible: solo simulación, sin mutación'
                    planned_accounts.add(account_id)
        decisions.append(Decision(line_num,request_id,account_id,action,outcome,reason,plan))
    return decisions


def process_files(requests_file: Path, accounts_file: Path) -> list[Decision]:
    if requests_file.resolve() == accounts_file.resolve():
        raise ValueError('Solicitudes y catálogo no pueden ser el mismo archivo')
    requests = load_csv(requests_file,REQ_FIELDS)
    accounts = make_account_index(load_csv(accounts_file,ACCOUNT_FIELDS))
    return evaluate(requests,accounts)


def summarize(decisions: list[Decision]) -> dict:
    counts = Counter(d.outcome for d in decisions)
    return {'mode':'DRY_RUN_ONLY','total':len(decisions),'would_execute':counts['WOULD_EXECUTE'],
            'hold':sum(n for k,n in counts.items() if k.startswith('HOLD_')),
            'review':sum(n for k,n in counts.items() if k.startswith('REVIEW_')),
            'skip':sum(n for k,n in counts.items() if k.startswith('SKIP_')),
            'by_outcome':dict(sorted(counts.items())),'external_mutations':0}
