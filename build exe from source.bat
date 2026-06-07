@echo off
cd /d "%~dp0"
pyinstaller --onefile --noconsole --icon=app_icon.ico --add-data "background.jpg;." --add-data "app_icon.ico;." --add-data "template_8mb.bin;." -n "PS2 VMC Tool" PS2_OneClick_VMC.py
echo.
echo ===== Done!! You are the Programist Congratulations =====
pause >nul
