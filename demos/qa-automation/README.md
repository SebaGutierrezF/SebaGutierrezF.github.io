# QA Automation — evidencia técnica complementaria

Este proyecto reutiliza **sin modificar** [QA Automation Starter Kit Community Free v0.1.1](https://github.com/SebaGutierrezF/qa-automation-starter-kit-free). La muestra pública original contiene 2 casos API con pytest y 2 casos UI con Selenium y un Page Object.

El código de esta carpeta aporta un **convertidor de JUnit XML a HTML/JSON** y un ejecutor PowerShell para recopilar evidencias de una ejecución futura del Starter Kit Free en Windows.

## Qué se validó

- `python -m unittest discover -s tests -v` (desde esta carpeta): **6/6 pruebas** del convertidor aprobaron localmente en Python 3.13.5 el 18-11-2026.
- Las pruebas consideran éxito, fallo, error, omisiones, XML vacío y escape de HTML.
- **No** se ejecutaron aquí las 4 pruebas originales API/Selenium del Starter Kit Free: requieren Python 3.12, pytest 8.3.4, Selenium 4.28.1 y Chrome/ChromeDriver locales compatibles para la UI.

## Ejecución en Windows

1. Obtener el Starter Kit Free desde GitHub y preparar el Python local con las versiones especificadas en su README.
2. Ejecutar `scripts/run_portfolio.ps1 -StarterKitPath 'C:\ruta\qa-automation-starter-kit-free' -PythonExecutable 'C:\ruta\python.exe'` para API.
3. Definir `CHROMEDRIVER_PATH` y agregar `-IncludeUI` para los cuatro casos, cuando el navegador y driver estén disponibles.
4. Inspeccionar los archivos de salida locales: `evidence/pytest.xml`, `evidence/summary.json`, `evidence/index.html`.

El runner usa el verificador de nombres JUnit del repositorio original. Si una prueba falla o se omite, **no** se presenta el resultado como PASS. Nunca reutilizar resultados del convertidor para afirmar que Selenium aprobó.

**Límites:** todo se basa en una aplicación local sintética. No hay datos de clientes, proyectos contratados ni ROI demostrados. El código comercial del Starter Kit Pro no se distribuye.

Licencia MIT para este complemento.
