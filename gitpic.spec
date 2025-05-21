# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['gitpic.py', 'delete_api.py','drop_image_widget.py','message_box.py','my_enum.py','show_img_widget.py','sidebar.py','stack_page.py','switch_button.py','upload_api.py'],
    pathex=[],
    binaries=[],
    datas=[('img', 'img'), ('fonts', 'fonts')],
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
    [],
    exclude_binaries=True,
    name='gitpic',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='gitpic',
)
