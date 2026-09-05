@echo off
REM add_demo_data.bat — fills FILMO with sample accounts, auditions and entries
REM so the website looks alive when you demo it.
REM Just double-click this file. Safe to run more than once.
cd /d "%~dp0"
venv\Scripts\python.exe seed_demo.py
REM Keeps the window open so you can read the login details it prints.
pause
