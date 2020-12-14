@ECHO off

SET space=--
SET /P _path=Podaj sciezke: 
CALL :printTree %_path%
PAUSE
GOTO :eof

:printTree
SET _string=%1
SET _string=%_string:"=%
FOR /f "tokens=*" %%G IN ('dir "%_string%\" /a:d /b') DO ( 
CALL :print "%%G" %space%
SET space=%space%--
CALL :printTree "%_string%\%%G"
)
GOTO :eof

:print
SET string=%1
SET string=%string:"=%
ECHO  ^|%2%string%
GOTO :eof