# Automatización y conciliación de procesos — evidencia técnica pública

Demostración educativa original en **Python 3.10+**, sin dependencias externas. Reutiliza el motor del proyecto de portafolio preparado el 18-11-2026. Solo usa CSV ficticios; no incorpora código, procesos internos, credenciales ni información real de WOM Chile.

## En una frase

Prevalidación de solicitudes operativas: comparar un lote CSV con el estado conocido de cuentas ficticias, justificar qué operaciones podrían planificarse y cuáles deben bloquearse, revisarse u omitirse **antes** de modificar cualquier sistema.

## Reproducción

Desde esta carpeta, en Windows, macOS o Linux:

1. `python -m unittest discover -s tests -v`
2. `python -m process_demo.cli --requests data/requests.csv --accounts data/accounts.csv --output evidence`
3. Abrir `evidence/report.html` y revisar `evidence/summary.json`, `evidence/audit.jsonl`.

**Resultado esperado con el dataset incluido:** 14/14 pruebas unitarias OK, 10 solicitudes, 3 WOULD_EXECUTE (no ejecutadas), 2 HOLD, 3 REVIEW, 2 SKIP, 0 mutaciones externas.

El CLI no tiene opción `--apply`, no realiza llamadas a APIs, no modifica bases de datos y nunca accede a servicios externos. Es un ejemplo de toma de decisiones, no una herramienta productiva.

## Decisiones ilustrativas (dataset incluido)

| Solicitud ficticia | Motivo | Decisión |
| --- | --- | --- |
| `R-1001`, segunda aparición | Identificador repetido en el mismo lote | `SKIP_DUPLICATE` |
| `R-1007` | Ya hay una operación elegible planificada para `C-002` en el lote | `HOLD_ACCOUNT_CONFLICT` |
| `R-1009` | Campo `approved` no es `true` ni `false` | `REVIEW_INVALID_APPROVAL` |

El motor detecta duplicados y conflictos **solo dentro del lote procesado**. No mantiene un registro persistente de idempotencia entre distintas ejecuciones.

## Evidencia pública y cómo interpretarla

- [Entradas ficticias](data/requests.csv) y [catálogo ficticio de cuentas](data/accounts.csv): permiten comprobar el origen de cada decisión.
- [Reglas de decisión](process_demo/engine.py) y [14 pruebas unitarias](tests/test_engine.py): muestran la lógica y los casos cubiertos.
- [Log local de tests, 18-11-2026](evidence-snapshot/tests.log) y [resumen JSON histórico](evidence-snapshot/summary.json): acreditan la validación registrada; **no son ejecuciones de GitHub Actions** ni pruebas con clientes.
- [Caso de estudio](../../proyectos/automatizacion-procesos.html) e [informe de ejemplo](../../proyectos/evidencia-procesos.html): explican el proceso y muestran las 10 decisiones.

El CLI guarda `summary.json`, `audit.jsonl` y `report.html` en el directorio que selecciones con `--output`. El instante UTC cambia en cada ejecución; con las mismas entradas se espera la misma clasificación, salvo ese sello temporal. `WOULD_EXECUTE` significa **elegible en simulación**, no ejecutado.

## Estructura

- `process_demo/engine.py`: reglas, catálogo, validación y decisiones por solicitud.
- `process_demo/cli.py`: ejecución local solo DRY RUN.
- `process_demo/report.py`: informes HTML, JSON y JSONL con escape de contenido.
- `data/`: CSV públicos totalmente ficticios.
- `tests/test_engine.py`: 14 tests incluyendo duplicados, conflictos y datos inválidos.
- `evidence-snapshot/`: evidencia publicada de una ejecución real en el entorno de preparación, distinguible de nuevas ejecuciones.

## Aplicación a un caso real: trabajo adicional necesario

Las reglas actuales son deliberadamente sencillas y están limitadas a CSV ficticios. Antes de usarse en una empresa haría falta acordar reglas de negocio, fuentes y aprobaciones autorizadas, gestionar acceso y credenciales, implementar idempotencia persistente y control de permisos, integrar APIs/bases de datos, y probar fallos y recuperación. Ninguna de esas capacidades productivas se considera demostrada por esta demo.

## Interpretación de métricas

Las métricas profesionales de WOM Chile que figuran en el [portafolio](../../proyectos/automatizacion-procesos.html) son experiencia laboral declarada, **no** medidas de esta demo ni una auditoría independiente. No hay clientes ni ROI demostrados por este ejercicio.

Licencia: MIT.
