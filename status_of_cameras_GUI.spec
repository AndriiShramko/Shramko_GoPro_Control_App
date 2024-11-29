# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['status_of_cameras_GUI.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('camera_cache.json', '.'),  # JSON файл для кэша
        ('camera_orientation_lock.py', '.'),
        ('copy_to_pc.py', '.'),
        ('copy_to_pc_and_scene_sorting.py', '.'),
        ('date_time_sync.py', '.'),
        ('format_sd.py', '.'),
        ('Gopro_Gui_Interface.py', '.'),
        ('goprolist_and_start_usb.py', '.'),
        ('goprolist_and_start_usb_sync_all_settings_date_time.py', '.'),
        ('goprolist_usb_activate_time_sync.py', '.'),
        ('goprolist_usb_activate_time_sync_record.py', '.'),
        ('prime_camera_sn.py', '.'),
        ('read_and_write_all_settings_from_prime_to_other.py', '.'),
        ('recording.py', '.'),
        ('set_preset_0.py', '.'),
        ('set_video_mode.py', '.'),
        ('sleep.py', '.'),
        ('status_of_cameras.py', '.'),
        ('status_of_cameras_GUI.py', '.'),
        ('stop_record.py', '.'),
        ('sync_and_record.py', '.'),
        ('Turn_Off_Cameras.py', '.'),
        ('icon.ico', '.'),  # Иконка для приложения
        ('ico/a2d48c62-b5d0-4da1-b944-ff767a22f643.jpg', './ico/'),
        ('ico/icon.ico', './ico/'),
    ],
    hiddenimports=[
        'zeroconf._utils.ipaddress',
        'zeroconf._handlers.answers',
        'zeroconf._core',
        'zeroconf._engine',
        'zeroconf._services.info',
        'zeroconf._services.names',
        'zeroconf._protocol.outgoing',
        'zeroconf._protocol.incoming',
        'zeroconf._exceptions',
        'sip',  # Необходимо для PyQt5
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
    a.binaries,
    a.datas,
    [],
    name='status_of_cameras_GUI',
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
    icon='icon.ico',  # Иконка для вашего приложения
)
