@echo off
setlocal

:: Set the name of the virtual environment
set "ENV_NAME=chart_cfb"

:: Create the virtual environment
python -m venv "%ENV_NAME%"

:: Activate the virtual environment
call "%ENV_NAME%\Scripts\activate.bat"

:: Install packages from the requirements.txt file
pip install -r requirements.txt

:: Deactivate the virtual environment
deactivate

endlocal