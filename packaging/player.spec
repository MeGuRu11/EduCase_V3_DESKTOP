# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec для Player. Сборка: pyinstaller packaging/player.spec
# Запуск из корня репозитория.

a = Analysis(
    ["../src/educase_player/__main__.py"],
    pathex=["src"],
    binaries=[],
    datas=[],            # TODO: добавить QSS/ресурсы по мере появления
    hiddenimports=[],
    hookspath=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz, a.scripts, a.binaries, a.datas, [],
    name="EduCase-Player",
    console=False,
    upx=False,
)
