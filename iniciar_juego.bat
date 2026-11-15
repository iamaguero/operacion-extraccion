@echo off
cd /d "%~dp0"
start "" http://localhost:8000
where python >nul 2>nul && (python -m http.server 8000 & goto :eof)
where py >nul 2>nul && (py -m http.server 8000 & goto :eof)
echo No se encontro Python. Usa Live Server en VS Code (ver README).
pause
