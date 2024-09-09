cd c:\temp

python -m nuitka ^
    --onefile ^
    --mingw64 ^
    --lto=no ^
    --windows-disable-console ^
    --enable-plugin=tk-inter ^
    --windows-icon-from-ico=edit_clear.ico ^
    -o aqicn_gui.exe ^
    aqicn_gui.py
pause

