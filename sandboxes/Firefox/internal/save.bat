@echo off

REM This is automatically executed by the main `save.bat` in parent directory
REM and this allows saving the output into a .log file

for /F "tokens=2" %%i in ('date /t') do set mydate=%%i
set mytime=%time%
echo Current time is %mydate%:%mytime%

C:\Python38-x64\python.exe C:\Users\WDAGUtilityAccount\Desktop\Firefox\internal\profile.py -s