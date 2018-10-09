@echo off
set python_path=%LocalAppData%\programs\python\python36
set PATH=%python_path%;%PATH%

pushd "%~dp1"
python %~dp0pdf2png.py --rot 90 --dpi 96 --fmt jpg %1
popd

REM cmd /e:on /v:on /k
rem pause
