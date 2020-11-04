@echo off

if exist %1 (robocopy %1 %2 /e /xf * & exit /b) 
echo "Podana sciezka nie istnieje"