# -*- mode: python -*-
a = Analysis(['main.py'],
             pathex=['D:\\adri\\work\\PycharmProjects\\braincell'],
             hiddenimports=['atexit'],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='BrainCell.exe',
          debug=False,
          strip=None,
          upx=True,
          console=False , icon='icon.ico')
