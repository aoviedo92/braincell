@echo off
set name=BrainCell
set icon=icon.ico
set script=main.py
pyinstaller -n %name% -w -F --hidden-import=atexit -i %icon% %script%
start dist
pause