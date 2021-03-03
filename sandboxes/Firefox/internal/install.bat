@echo off

REM This is automatically executed by the main `install.bat` in parent directory
REM and this allows saving the output into a .log file

for /F "tokens=2" %%i in ('date /t') do set mydate=%%i
set mytime=%time%
echo Current time is %mydate%:%mytime%

REM Download/install latest version of Firefox
curl -L "https://download.mozilla.org/?product=firefox-latest-ssl&os=win64&lang=en-GB" --output "C:\users\WDAGUtilityAccount\Downloads\Firefox Setup Latest.exe"
"C:\users\WDAGUtilityAccount\Downloads\Firefox Setup Latest.exe" /S

REM Download/install a given Python 3.8 and dependencies
curl -L "https://www.python.org/ftp/python/3.8.8/python-3.8.8-amd64.exe" --output "C:\users\WDAGUtilityAccount\Downloads\python-3.8.8-amd64.exe"
"C:\users\WDAGUtilityAccount\Downloads\python-3.8.8-amd64.exe" /quiet InstallAllUsers=1 PrependPath=1 TargetDir=C:\Python38-x64
C:\Python38-x64\Scripts\pip3.8.exe install psutil

REM Debug / development
REM curl -L "https://github.com/notepad-plus-plus/notepad-plus-plus/releases/download/v7.9.3/npp.7.9.3.Installer.x64.exe" --output "C:\users\WDAGUtilityAccount\Downloads\npp.7.9.3.Installer.x64.exe"
REM "C:\users\WDAGUtilityAccount\Downloads\npp.7.9.3.Installer.x64.exe" /S

REM Copy Firefox profile from shared folder into the sandbox
C:\Python38-x64\python.exe C:\Users\WDAGUtilityAccount\Desktop\Firefox\internal\profile.py

REM We are done, so start the browser
"C:\Program Files\Mozilla Firefox\firefox.exe"