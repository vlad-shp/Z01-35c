@ECHO off

SET /P _path= Podaj sciezke:
SET /P _extencion= Podaj rozszerzenie:

DIR "%_path%\*.%_extencion%" /B 

PAUSE
