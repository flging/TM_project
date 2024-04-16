# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['packge\\src\\report_generator.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['TM_find_page', 'TM_agent_getindex', 'TM_extract_text', 'TM_agent', 'Indextranslate'],
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
    name='report_generator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
