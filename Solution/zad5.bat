@echo off

set _ffmpeg="C:\jezyki skryptowe\ffmpeg.exe"
%_ffmpeg% -i %1 -vframes 1 miniatura.png 2>&1