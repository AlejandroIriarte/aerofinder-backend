@echo off
setlocal
pytest -q
if errorlevel 1 exit /b 1
pytest --cov=app --cov-report=term-missing --cov-report=html --junitxml=evidencia\junit.xml
if not exist evidencia mkdir evidencia
rmdir /S /Q evidencia\coverage_html >nul 2>&1
mkdir evidencia\coverage_html
xcopy /E /I /Y htmlcov evidencia\coverage_html >nul
echo OK - Abrir evidencia\coverage_html\index.html
endlocal
