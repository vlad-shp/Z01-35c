@ECHO off

SETLOCAL EnableDelayedExpansion
SET /P n= Wpisz N:

IF %n% equ 1 GOTO :input_1
IF %n% equ 0 GOTO :end

SET a=1
SET b=1

SET /a n=n-2

SET s=%a% %b%
FOR /l %%g IN (1,1,%n%) DO (
	SET /a c=a+b
	SET s=!s! !c!
	SET /a a=b
	SET /a b=c
)

ECHO !s!
GOTO :end

:input_1
ECHO 1

:end
ENDLOCAL

PAUSE