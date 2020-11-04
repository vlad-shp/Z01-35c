@echo off

if exist %1 (dir %1\*.%2 & exit /b)
echo "Podana sciezka nie istnieje"
