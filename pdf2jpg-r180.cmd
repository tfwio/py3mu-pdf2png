@echo off
set python_path=%LocalAppData%\programs\python\python36
set PATH=%python_path%;%PATH%

pushd "%~dp1"
python %~dp0pdf2png.py --dpi 200 --rot 180 --fmt jpg %1
popd

REM cmd /e:on /v:on /k
REM pause
