@echo off
REM Run the GUI Dashboard
REM Double-click this file to launch the GUI

cd /d "%~dp0"
set PYTHONPATH=%CD%
python src/gui_dashboard.py

pause
