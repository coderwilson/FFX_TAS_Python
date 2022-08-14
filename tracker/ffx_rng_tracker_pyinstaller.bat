@echo off
@REM yy.mm.dd format
set /a version_major = 100%date:~8,2% %% 100
set /a version_minor = 100%date:~3,2% %% 100
set /a version_micro = 100%date:~0,2% %% 100
set version=%version_major%.%version_minor%.%version_micro%
echo %version%>%~dp0data/VERSION
set name="FFX RNG tracker v%version%"
set data="%~dp0data;data/"
set ui_tkinter="%~dp0ui_tkinter;ui_tkinter/"
set file_name="%~dp0ffx_rng_tracker_ui.py"
pyinstaller --noconfirm --onefile --windowed --name=%name% --add-data %data% --add-data %ui_tkinter% %file_name%
pause
