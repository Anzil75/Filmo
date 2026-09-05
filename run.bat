@echo off
REM run.bat — starts the FILMO website.
REM Just double-click this file, or type  run  in cmd.

REM Move to the folder this file is sitting in, whatever folder you started from.
cd /d "%~dp0"

echo.
echo  Starting FILMO...
echo  Open your browser at:  http://127.0.0.1:5001
echo  Press Ctrl+C in this window to stop the server.
echo.

venv\Scripts\python.exe app.py

REM Keeps the window open if the app stops, so you can read any error message.
pause
