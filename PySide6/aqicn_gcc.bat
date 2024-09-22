cd c:\temp

python -m nuitka ^
    --onefile ^
    --mingw64 ^
    --lto=no ^
    --enable-plugin=pyside6 ^
    --windows-disable-console ^
    --windows-icon-from-ico=edit_clear.ico ^
    aqicn_pyside.py
pause
