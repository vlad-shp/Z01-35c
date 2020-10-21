@echo off
if %1 EQU 1 (echo 1 & exit /b)

setlocal enabledelayedexpansion
set /a fib1 = 1
set /a fib2 = 1
echo %fib1%

for /l %%i in (1,1,%1) do (
	set /a temp = !fib1! + !fib2!
	set /a fib1 = !fib2!
	echo !fib2!
	set /a fib2 = !temp!
)
