@echo off
call %~dp0\chart_cfb\Scripts\activate.bat
python data_cleaner_openpyxl.py %1