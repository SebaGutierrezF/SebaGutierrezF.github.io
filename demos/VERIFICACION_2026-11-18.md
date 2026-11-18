# Registro de verificación técnica · 18 de noviembre de 2026

## Procedencia

- **Material:** archivos públicos de los paquetes de portafolio del 18-11-2026, incorporados a `demos/` en este repositorio. Los blobs del código Python, los archivos CSV y el ejecutor PowerShell coinciden exactamente con los archivos que pasaron las pruebas locales (verificación por Git blob SHA).
- **Entorno local de validación:** Python 3.13.5, biblioteca estándar. No se contactó ninguna API de negocio ni sistema de clientes.
- **Fecha:** 18-11-2026. Estos logs son una instantánea de la verificación; no son una ejecución automática de GitHub Actions.

## QA Automation: complemento de reportes

Desde `demos/qa-automation/`: `python -m unittest discover -s tests -v`.

- **6/6 tests aprobados**, 0 fallidos/errores de los 6 ejercicios del convertidor JUnit → HTML/JSON.
- Casos: XML vacío, error, fallo, pase, omisión y escape de contenido HTML.
- [Salida de unittest](qa-automation/evidence-snapshot/tests.log).
- **Validación posterior del 18-11-2026 en Windows (ejecutada por el autor):** suite Free de **4/4 PASS** (2 API, 2 UI/Selenium), **0 errores/omisiones/fallos**, pytest **8.86 s**, con verificador `QA_SK_002_JUNIT_OK | TESTS=4 | SKIPPED=0 | FAILURES=0`. Entorno: Python 3.12.10, pytest 8.3.4, Selenium 4.28.1, Chrome 157.0.8103.79 y ChromeDriver 157.0.8103.78. [Salida sanitizada proporcionada por el autor](qa-automation/evidence-snapshot/windows-full-suite-2026-11-18.md) · [Resumen estructurado](qa-automation/evidence-snapshot/windows-full-suite-2026-11-18.json). **No se ha adjuntado el XML JUnit original**, por lo que la validación pública se fundamenta en el log presentado por el autor, no en una verificación independiente de ese XML.

## Automatización y conciliación Python

Desde `demos/process-automation/`:

1. `python -m unittest discover -s tests -v`
2. `python -m process_demo.cli --requests data/requests.csv --accounts data/accounts.csv --output evidence`

- **14/14 tests unitarios aprobados**.
- **10 solicitudes ficticias**: 3 WOULD_EXECUTE, 2 HOLD, 3 REVIEW, 2 SKIP.
- **0 mutaciones externas**; DRY_RUN_ONLY.
- Dos ejecuciones consecutivas sobre los mismos datos devolvieron el mismo resumen después de ignorar únicamente el sello de tiempo.
- [Salida de unittest](process-automation/evidence-snapshot/tests.log) · [Resumen JSON histórico](process-automation/evidence-snapshot/summary.json).

## Límites

Las pruebas cubren estos casos sintéticos y no comprueban integración con sistemas reales, cargas de producción, concurrencia distribuida ni ingresos/ROI. Los hitos profesionales de WOM Chile corresponden a experiencia declarada y no se derivan de estas demos.

**Para ver resultados nuevos, cada persona debe ejecutar los comandos en su propio equipo.** Los logs publicados no son datos en tiempo real.
