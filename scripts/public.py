from os import system
import platform

from .build import build


def public() -> None:
    remove_command = ''
    if platform.system() == 'Linux':
        remove_command = 'rm -rf'
    
    else:
        remove_command = 'del /F /Q'
        
    system(f"{remove_command} dist")
    system(f"{remove_command} tnotify.egg-info")

    build()
    system("twine upload dist/*")

    system(f"{remove_command} dist")
    system(f"{remove_command} tnotify.egg-info")

    print("SUCCESS")
