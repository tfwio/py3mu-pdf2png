@echo off
set python_path=%LocalAppData%\programs\python\python36
set PATH=%python_path%;%PATH%

python %~dp0pdf2png.py --rot 90 --dpi 200 --fmt jpg %1

REM cmd /e:on /v:on /k
rem pause
