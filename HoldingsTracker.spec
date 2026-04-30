# -*- mode: python ; coding: utf-8 -*-


from pathlib import Path

spec_dir = Path('.').resolve()

a = Analysis(
    ['src/holdings_tracker_desktop/main.py'],
    pathex=[str(spec_dir / "src")],
    binaries=[],
    datas=[
        (str(spec_dir / "src/holdings_tracker_desktop/alembic"), "alembic"),
        (str(spec_dir / "alembic.ini"), "."),
        (str(spec_dir / "src/holdings_tracker_desktop/ui/flags"), "holdings_tracker_desktop/ui/flags"),
        (str(spec_dir / "src/holdings_tracker_desktop/ui/assets"), "holdings_tracker_desktop/ui/assets"),
    ],
    hiddenimports=[
        "logging.config",
    ],
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
    [],
    exclude_binaries=True,
    name='HoldingsTracker',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(spec_dir / "src/holdings_tracker_desktop/ui/assets/HoldingsTracker.ico"),
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='HoldingsTracker',
)
