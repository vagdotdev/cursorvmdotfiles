#!/usr/bin/env python3
"""Install the captured appearance for the current Linux user, outside XFCE."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import time
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / 'capture/bundle'


def verify():
    entries = json.loads((ROOT / 'CAPTURE-MANIFEST.json').read_text())
    for name, item in entries.items():
        path = ROOT / name
        if 'symlink' in item:
            assert path.is_symlink() and os.readlink(path) == item['symlink'], name
        else:
            assert not path.is_symlink() and path.is_file(), name
            assert hashlib.sha256(path.read_bytes()).hexdigest() == item['sha256'], name
    return len(entries)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true', help='Verify and describe; change nothing')
    args = parser.parse_args()
    print(f'Capture verified: {verify()} files and symlinks')
    if args.dry_run:
        print('Would back up destination paths, install per-user assets/configuration, and schedule XFCE session setup. No changes made.')
        return
    if platform.system() != 'Linux' or os.geteuid() == 0:
        raise SystemExit('Run as the destination Linux user, not root. No changes made.')
    for tool in ('pgrep', 'xfconf-query', 'plank', 'dconf', 'gsettings', 'fc-cache'):
        if not shutil.which(tool):
            raise SystemExit(f'Missing {tool}; install dependencies in FRESH_INSTALL.md first.')
    result = subprocess.run(['pgrep', '-u', str(os.getuid()), '-x', 'xfce4-session'], capture_output=True)
    if result.returncode != 1:
        raise SystemExit('Log out of XFCE and run from a text console/SSH. No changes made.')
    home = Path.home()
    if any(c in str(home) for c in '\"$`\n') or '\\' in str(home):
        raise SystemExit('Unusual home path; use the manual restore guide.')
    # Captured paths assume default XDG locations. Never silently install into the wrong profile.
    for name, default in (('XDG_CONFIG_HOME', home / '.config'), ('XDG_DATA_HOME', home / '.local/share'), ('XDG_STATE_HOME', home / '.local/state')):
        if os.environ.get(name) and Path(os.environ[name]) != default:
            raise SystemExit(f'Custom {name} detected; adapt the manual restore procedure first.')
    state = home / '.local/state/cursorvmdotfiles'
    if state.exists():
        raise SystemExit(f'An install/backup already exists at {state}. Inspect it before reapplying; nothing overwritten.')
    backup = state / ('backup-' + time.strftime('%Y%m%d-%H%M%S'))
    backup.mkdir(parents=True)
    record = []

    def install(source, relative):
        dest = home / relative
        # Avoid following user-created destination symlinks into unrelated locations.
        for parent in (dest, *dest.parents):
            if parent == home:
                break
            if parent.is_symlink():
                raise RuntimeError(f'Refusing symlink destination: {parent}')
        existed = dest.exists()
        if existed:
            saved = backup / relative
            saved.parent.mkdir(parents=True, exist_ok=True)
            if dest.is_dir():
                shutil.copytree(dest, saved, symlinks=True)
            else:
                shutil.copy2(dest, saved)
        record.append({'path': relative, 'existed': existed})
        (backup / 'paths.json').write_text(json.dumps(record, indent=2) + '\n')
        dest.parent.mkdir(parents=True, exist_ok=True)
        if source.is_dir():
            shutil.copytree(source, dest, symlinks=True, dirs_exist_ok=True)
        else:
            shutil.copy2(source, dest)
        return dest

    share = BUNDLE / 'system/usr/share'
    for group in ('themes', 'icons', 'fonts', 'backgrounds', 'pixmaps', 'plank'):
        # Back up and copy each captured child, not the user's entire shared-data directory.
        for source in (share / group).iterdir():
            install(source, f'.local/share/{group}/{source.name}')
    config = BUNDLE / 'home/home/ubuntu/.config'
    for group in ('gtk-3.0', 'plank'):
        install(config / group, f'.config/{group}')
    install(config / 'xfce4/terminal', '.config/xfce4/terminal')
    xml_dir = 'xfce4/xfconf/xfce-perchannel-xml'
    for channel in ('xsettings', 'xfwm4', 'xfce4-panel', 'xfce4-terminal', 'thunar'):
        dest = install(config / xml_dir / (channel + '.xml'), f'.config/{xml_dir}/{channel}.xml')
        if channel == 'xfce4-panel':
            tree = ET.parse(dest)
            for prop in tree.iter('property'):
                if prop.get('name') == 'button-icon' and prop.get('value') == 'cursor-logo':
                    prop.set('value', str(home / '.local/share/pixmaps/cursor-logo.svg'))
            tree.write(dest, encoding='UTF-8', xml_declaration=True)
    install(BUNDLE / 'manifest/plank.dconf', '.local/share/cursorvmdotfiles/plank.dconf')
    runner = install(ROOT / 'scripts/finish-session.sh', '.local/share/cursorvmdotfiles/finish-session.sh')
    runner.chmod(0o755)
    desktop = state / 'cursor-appearance-setup.desktop'
    desktop.write_text(f'[Desktop Entry]\nType=Application\nName=Finish Cursor desktop appearance\nExec=/bin/sh "{runner}"\nOnlyShowIn=XFCE;\nTerminal=false\n')
    install(desktop, '.config/autostart/cursor-appearance-setup.desktop')
    plank_autostart = state / 'cursor-plank.desktop'
    plank_autostart.write_text('[Desktop Entry]\nType=Application\nName=Plank\nExec=plank\nOnlyShowIn=XFCE;\nTerminal=false\n')
    install(plank_autostart, '.config/autostart/cursor-plank.desktop')
    subprocess.run(['fc-cache', '-f'], check=True)
    (state / 'installed').write_text(str(backup) + '\n')
    print(f'Appearance prepared. Backup: {backup}')
    print('Log into an XFCE/X11 session. Then review ~/.local/state/cursorvmdotfiles/session.log and compare the screenshots.')


if __name__ == '__main__':
    main()
