@echo off
set python_path=%LocalAppData%\programs\python\python36
set PATH=%python_path%;%PATH%

python %~dp0pdf2png.py --dpi 200 --rot 270 --fmt jpg %1
rem cmd /e:on /v:on /k

pause
