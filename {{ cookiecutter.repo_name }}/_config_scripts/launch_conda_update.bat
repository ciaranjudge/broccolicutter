@echo off
echo --------------------------------------------------------
echo                  *** DON'T PANIC! ***
echo --------------------------------------------------------
call %LOCALAPPDATA%\Continuum\miniconda3\Scripts\activate.bat
call python .\_config_scripts\update_conda.py

