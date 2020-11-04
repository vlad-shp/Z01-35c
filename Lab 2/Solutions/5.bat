@ECHO off 

SET _ffmpeg="C:\Program Files\ffmpeg\bin\ffmpeg.exe"
SET _outoutPath=%cd%
SET /P _fileVideo=Podaj plik wideo: 	

%_ffmpeg% -i %_fileVideo% -vframes 1 "%_fileVideo%_miniature.jpg"  >nul 2>nul

ECHO Ok.

PAUSE