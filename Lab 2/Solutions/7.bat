@ECHO off
:start
SET /P _n=Podaj N^<13: 
SET _silnia=1

IF %_n% GEQ 13 GOTO :start

FOR /l %%g IN (1,1,%_n%) DO (
	SET /a _silnia=_silnia*%%g
)

ECHO %_silnia%

PAUSE
GOTO :eof