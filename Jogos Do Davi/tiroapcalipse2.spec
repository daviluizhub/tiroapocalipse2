# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['tiroapcalipse2.py'],
    pathex=[],
    binaries=[],
    datas=[('player.png', '.'), ('enemy.png', '.'), ('boss.png', '.'), ('tiro.png', '.'), ('laserShoot.wav', '.'), ('fundo.jpg', '.'), ('armadediadasmaes.png', '.'), ('armademesdosnamorados.png', '.'), ('armademesdospais.png', '.'), ('armadeoutono.png', '.'), ('armadepascoa.png', '.'), ('armadoce.png', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='tiroapcalipse2',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
