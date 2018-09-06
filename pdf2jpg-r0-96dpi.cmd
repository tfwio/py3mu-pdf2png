@echo off
set python_path=%LocalAppData%\programs\python\python36
set PATH=%python_path%;%PATH%

python %~dp0pdf2png.py --dpi 96 --fmt jpg %1

pause
