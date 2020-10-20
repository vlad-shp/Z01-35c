@ECHO off

SET /P _path= Podaj sciezke:

XCOPY %_path% %cd% /H /Y /C /R /I /E /T

ECHO Ok

PAUSE
