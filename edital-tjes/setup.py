from cx_Freeze import setup, Executable
from main import program_info
from sys import platform


build_exe_options = {'includes': ['docx', 'docx.text.paragraph', 'docx.opc.exceptions', 'tkinter', 'tkinter.ttk',
                                  'tkinter.filedialog', 'distutils.util', 'configparser', 'num2words']}


base = None

if platform == "win32":
    base = "Win32GUI"


setup(
    name=program_info['name'],
    version=program_info['version'],
    description=program_info['name'],
    
    author='Gustavo Marquezinho',
    author_email='gustavomarquezinho@gmail.com',

    options={'build_exe': build_exe_options},
    executables=[Executable(script='./source/main.py', base=base, icon='./source/assets/icon_medium.ico')]
)
