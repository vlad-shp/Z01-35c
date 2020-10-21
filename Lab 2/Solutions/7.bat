@ECHO off
SET _silnia=1
IF %1 GEQ 13 GOTO :err

FOR /l %%g IN (1,1,%1) DO (
	SET /a _silnia=_silnia*%%g
)
ECHO Result: %_silnia%
GOTO :eof

:err
ECHO Result: Invalid number. Numbers are limited to 32-bits of precision.
GOTO :eof