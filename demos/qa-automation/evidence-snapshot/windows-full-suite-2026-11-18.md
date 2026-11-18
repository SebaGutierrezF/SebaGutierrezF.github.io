# Ejecución local completa · QA Automation Starter Kit Free

**Fecha reportada:** 18 de noviembre de 2026  
**Fuente:** salida de PowerShell/pytest compartida por el autor después de ejecutar la suite en Windows.  
**Naturaleza:** evidencia local resumida y sanitizada; **no** corresponde a GitHub Actions ni a una reproducción independiente desde el JUnit XML original.

## Comprobación y resultados

```text
PYTEST_PIN_OK
SELENIUM_PIN_OK
....  [100%]
4 passed in 8.86s
QA_SK_002_JUNIT_OK | TESTS=4 | SKIPPED=0 | FAILURES=0
TOTAL=4 STATUS=PASS
QA_PORTFOLIO_PASS | MODE=API_AND_UI
QA_FULL_VALIDATION_COMPLETE
```

En el resumen JSON local se observaron `total=4`, `overall=PASS`, `PASSED=4`, `FAILED=0`, `ERROR=0`, `SKIPPED=0`.

### Casos cubiertos

| Nombre real de prueba | Alcance | Estado según suite y verificador |
| --- | --- | --- |
| `test_api_001_health` | Endpoint de salud de la demo | PASS |
| `test_api_002_catalog` | Catálogo sintético | PASS |
| `test_ui_001_login_success` | Login válido con Selenium | PASS |
| `test_ui_002_invalid_login` | Error de login inválido con Selenium | PASS |

**Entorno:** Python 3.12.10, pytest 8.3.4, Selenium 4.28.1, Chrome 157.0.8103.79, ChromeDriver 157.0.8103.78; navegador headless. Se ejecutó el runner `demos/qa-automation/scripts/run_portfolio.ps1` con `-IncludeUI`.

## Qué se publicó y qué no

Se conservan únicamente las líneas relevantes del log y [el resumen JSON estructurado](windows-full-suite-2026-11-18.json). Se **omitieron** rutas locales con carpetas del equipo, números de puerto de DevTools, identificadores de sesión del navegador y detalles que no aportan evidencia técnica.

El **JUnit XML original (4 casos)** y el HTML/JSON generado por el runner están en el entorno local del autor, pero **no fueron compartidos como archivos** ni se inspeccionaron de forma independiente para esta publicación. Por tanto, este registro **no** prueba una ejecución de CI ni permite reproducir los resultados sin ejecutar el Starter Kit Free en otro equipo.

Para reproducir: seguir [las instrucciones del complemento](../README.md) y el [código Free original](https://github.com/SebaGutierrezF/qa-automation-starter-kit-free). Todo se ejecuta sobre una demo sintética local; las cifras de experiencia profesional no provienen de estas pruebas.
