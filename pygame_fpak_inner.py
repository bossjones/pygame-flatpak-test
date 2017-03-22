import os
from pathlib import Path
import pytoml
from shutil import copy2, copytree, ignore_patterns
import sys

ignore_pycache = shutil.ignore_patterns()

DESKTOP_TEMPLATE = """\
[Desktop Entry]
Type=Application
Name={name}
Icon={appid}
Exec=/app/bin/launch-game
Categories=Game
"""

LAUNCHER_TEMPLATE = """\
#!{python}
from {mod} import {func}
{func}()
"""

python_paths = {
    '3.6': '/app/bin/python3',
    '3.4': '/usr/bin/python3',
    '2.7': '/usr/bin/python',
}

def main()
    config = pytoml.load(sys.argv[1])
    install_dir = Path('/app/bin/mygame')
    install_dir.mkdir(parents=True)
    for file in config['files']:
        if os.path.isdir(file):
            copytree(file, str(install_dir / file),
                    ignore=ignore_patterns('__pycache__', '*.pyc'))
        else:
            copy2(file, str(install_dir))
    
    # Icons
    for size, path in config['icons'].items():
        target_path = '/app/share/icons/hicolor/{size}x{size}/apps/{appid}.png'.format(
                        size=size, appid=config['appid'])
        copy2(path, target_path)
    
    # Desktop file
    desktop_target = '/app/share/applications/{}.desktop'.format(config['appid'])
    with open(desktop_target, 'w') as f:
        f.write(DESKTOP_TEMPLATE.format_map(config))
    
    # Launcher
    module, func = config['entry-point'].split(':')
    launcher_file = install_dir / 'launch-game.py'
    with launcher_file.open('w') as f:
        f.write(LAUNCHER_TEMPLATE.format(
            python=python_paths[config['python']],
            mod = module, func=func
        ))
    launcher_file.chmod(0o755)
    Path('/app/bin/launch-game').symlink_to(launcher_file)
