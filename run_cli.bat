@echo off
REM Run the CLI Dashboard
REM Double-click this file to launch the CLI

cd /d "%~dp0"
set PYTHONPATH=%CD%
python src/dashboard.py

pause
