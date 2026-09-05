@echo off
REM remove_demo_data.bat — takes the sample data back out again.
REM Your own accounts (admin, maker, star) and anything you made by hand stay.
cd /d "%~dp0"
venv\Scripts\python.exe seed_demo.py remove
pause
