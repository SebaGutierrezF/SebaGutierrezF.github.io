# Automatización y conciliación de procesos — evidencia técnica pública

Demostración educativa original en **Python 3.10+**, sin dependencias externas. Reutiliza el motor del proyecto de portafolio preparado el 18-11-2026. Solo usa CSV ficticios; no incorpora código, procesos internos, credenciales ni información real de WOM Chile.

## Reproducción

Desde esta carpeta, en Windows, macOS o Linux:

1. `python -m unittest discover -s tests -v`
2. `python -m process_demo.cli --requests data/requests.csv --accounts data/accounts.csv --output evidence`
3. Abrir `evidence/report.html` y revisar `evidence/summary.json`, `evidence/audit.jsonl`.

**Resultado esperado con el dataset incluido:** 14/14 pruebas unitarias OK, 10 solicitudes, 3 WOULD_EXECUTE (no ejecutadas), 2 HOLD, 3 REVIEW, 2 SKIP, 0 mutaciones externas.

El CLI no tiene opción `--apply`, no realiza llamadas a APIs, no modifica bases de datos y nunca accede a servicios externos. Es un ejemplo de toma de decisiones, no una herramienta productiva.

## Estructura

- `process_demo/engine.py`: reglas, catálogo, validación y decisiones por solicitud.
- `process_demo/cli.py`: ejecución local solo DRY RUN.
- `process_demo/report.py`: informes HTML, JSON y JSONL con escape de contenido.
- `data/`: CSV públicos totalmente ficticios.
- `tests/test_engine.py`: 14 tests incluyendo duplicados, conflictos y datos inválidos.
- `evidence-snapshot/`: evidencia publicada de una ejecución real en el entorno de preparación, distinguible de nuevas ejecuciones.

## Interpretación de métricas

Las métricas profesionales de WOM Chile que figuran en el [portafolio](../../proyectos/automatizacion-procesos.html) son experiencia laboral declarada, **no** medidas de esta demo ni una auditoría independiente. No hay clientes ni ROI demostrados por este ejercicio.

Licencia: MIT.
