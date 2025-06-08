@echo off
echo [*] Cleaning previous build...
rmdir /s /q build
rmdir /s /q dist
del /q installer.spec

echo [*] Building installer.exe...
pyinstaller --onefile ^
  --name "AutoMata-Test Installer" ^
  --add-data "commandlinetools.zip;." ^
  --add-data "java-17.zip;." ^
  --add-data "AutoMata-Test Tools.zip;." ^
  installer.py

echo [*] Done. Find installer.exe in the /dist folder.
pause
