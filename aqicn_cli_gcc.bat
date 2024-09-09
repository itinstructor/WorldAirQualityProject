cd c:\temp

python -m nuitka ^
    --onefile ^
    --mingw64 ^
    --lto=no ^
    --windows-icon-from-ico=edit_clear.ico ^
    aqicn_cli.py
pause
