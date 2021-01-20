@ECHO off

net session >nul 2>nul
IF %errorLevel% == 0 (
    ECHO Success: uruchomiony jako administrator.
) ELSE (
    ECHO Failure: Prawa administratora nie będą nadane.
)
