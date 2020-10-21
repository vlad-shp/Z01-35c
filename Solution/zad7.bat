@echo off

setlocal enabledelayedexpansion
set /a temp =1
set /a wynik =1

for /l %%i in (1,1,%1) do (
	set /a wynik = !wynik!*!temp!
	set /a temp = !temp!+1
)
	echo !wynik!

