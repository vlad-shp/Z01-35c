@echo off

verify >nul
net session >nul 2>&1
if %errorlevel% NEQ 0 ( echo "Nie masz uprawnien administratora.") else ( echo "Jestes administratorem")