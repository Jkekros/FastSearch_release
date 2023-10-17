@echo off
tasklist /fi "ImageName eq FastSearch.exe" /fo csv 2>NUL | find /I "FastSearch.exe">NUL
if "%ERRORLEVEL%"=="1" set RETURNVALUE="1" && goto :stop else  goto :end 

:end
echo msgbox "FastSearch Already running" > %tmp%\tmp.vbs
cscript /nologo %tmp%\tmp.vbs
del %tmp%\tmp.vbs
exit 
:stop
start FastSearch.exe
