@echo off
cd /d "%~dp0"

call .venv\Scripts\activate.bat

start "" powershell -WindowStyle Hidden -Command "Start-Sleep -Seconds 5; Start-Process 'http://127.0.0.1:8000'"

python -m fastapi dev main.py

pause