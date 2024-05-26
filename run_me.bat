@echo off
REM Save the directory of this batch file
set script_dir=%~dp0

REM Change directory to the script directory
cd /d "%script_dir%"

REM Activate the virtual environment
call "%script_dir%.venv\Scripts\activate"

REM Run the Python script
python main.py

REM Pause the command prompt so it doesn't close immediately
pause
