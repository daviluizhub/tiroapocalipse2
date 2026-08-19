# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['tiroapocalipsejogo.py'],
    pathex=['C:\\Users\\kehlk\\Downloads\\Jogos Do Davi'],  # Path da tua pasta
    binaries=[],
    datas=[
        ('player.png', '.'),
        ('enemy.png', '.'),
        ('boss.png', '.'),
        ('tiro.png', '.'),
        ('laserShoot.wav', '.'),
        ('fundo.jpg', '.'),
        ('fundo2.jpg', '.'),
        ('fundo3.jpg', '.'),
        ('fundo4.jpg', '.'),
        ('fundo5.jpg', '.'),
        ('fundo6.jpg', '.'),
        ('fundo7.jpg', '.'),
        ('fundo8.jpg', '.'),
        ('fundo9.png', '.'),
        ('save.json', '.')  # Se usar
    ],  # Força inclusão de TODOS os assets na raiz do bundle
    hiddenimports=['pygame', 'pygame.mixer'],  # Pra Pygame não dar pau
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='tiroapocalipsejogo',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Sem console (--windowed)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)