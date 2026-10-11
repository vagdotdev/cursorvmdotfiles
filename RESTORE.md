# Restore the Cursor VM appearance

The original export is preserved unchanged under `capture/`, including its historical `RESTORE.md`. These instructions clarify the steps for a fresh Ubuntu XFCE account. Do not restore the recorded package inventory wholesale: it includes software unrelated to appearance.

## 1. Install the desktop components

On Ubuntu 24.04, install the components used by the reference:

```sh
sudo apt update
sudo apt install xfce4 xfce4-terminal thunar plank dconf-cli gtk2-engines-murrine gtk2-engines-pixbuf
```

Use an XFCE **X11** session. Install your browser separately; the captured dock launcher points to Google Chrome. Other distributions need equivalent packages.

## 2. Install the captured assets

From the repository root, copy only the appearance assets. This does not install the captured application `.desktop` files over your distribution's versions.

```sh
for directory in themes icons fonts backgrounds pixmaps plank; do
    sudo mkdir -p "/usr/share/$directory"
    sudo cp -a "capture/bundle/system/usr/share/$directory/." "/usr/share/$directory/"
done
fc-cache -f
```

Existing assets with the same names are overwritten. Use a fresh account/machine or back up those directories first. The original wallpaper is `/usr/share/backgrounds/desktop-background-3.png`.

## 3. Restore the account settings while logged out of XFCE

Log out of the graphical session, then use a text console or SSH **as the destination user**. From the repository root:

```sh
backup="$HOME/cursor-appearance-backup-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$backup" "$HOME/.config"
for directory in xfce4 gtk-3.0 plank; do
    if [ -d "$HOME/.config/$directory" ]; then
        cp -a "$HOME/.config/$directory" "$backup/"
    fi
done
cp -a capture/bundle/home/home/ubuntu/.config/gtk-3.0 "$HOME/.config/"
cp -a capture/bundle/home/home/ubuntu/.config/plank "$HOME/.config/"
mkdir -p "$HOME/.config/xfce4/terminal" "$HOME/.config/xfce4/xfconf/xfce-perchannel-xml"
cp -a capture/bundle/home/home/ubuntu/.config/xfce4/terminal/. "$HOME/.config/xfce4/terminal/"
for channel in xsettings xfwm4 xfce4-panel xfce4-terminal thunar; do
    cp "capture/bundle/home/home/ubuntu/.config/xfce4/xfconf/xfce-perchannel-xml/$channel.xml"        "$HOME/.config/xfce4/xfconf/xfce-perchannel-xml/"
done
```

The display and wallpaper XML remain in the archive for reference, but are deliberately not copied by these commands: the source used a `VNC-0` monitor that may not exist on your machine.

## 4. Finish inside the new XFCE session

- In **Desktop Settings**, select the supplied wallpaper for each desired monitor/workspace. Disable desktop icons to match the reference.
- From the repository root, run `dconf load /net/launchpad/plank/ < capture/bundle/manifest/plank.dconf`.
- Open Plank preferences and select **WhiteSur-Light**, bottom position, centered alignment, 48 px icons, and zoom to 150%. The original settings file is retained in `capture/bundle/home/home/ubuntu/.config/plank/dock1/settings`; newer Plank builds may require setting these preferences through their UI instead of reading that file.
- In **Session and Startup → Application Autostart**, add the command `plank`.
- Keep the Thunar and terminal launchers. Install Chrome or replace its dock item with your preferred installed browser. Copying a launcher does not install its application.
- If needed, select WhiteSur Light in Appearance and Window Manager, WhiteSur icons in Appearance, and WhiteSur cursors in Mouse and Touchpad. The intended settings are already in the captured XFCE files.

Compare `capture/desktop.png` and `capture/file-manager.png`. The reference uses a 28 px top panel with a Cursor menu icon and a clock; Inter 11 interface text; Inter Bold 11 window titles; and a white terminal with JetBrains Mono 11. Screen resolution, scaling, font rendering, and package versions can change the final pixels.

## Revert

Log out of XFCE. Restore the three backed-up configuration directories from the backup created above. If a directory did not exist before the restore, remove only the corresponding newly installed configuration directory. Remove the Plank autostart entry if you added it. Shared theme assets can remain installed without being active.

This repository contains an appearance capture and a manual restoration procedure. It does not reproduce the remote desktop transport, Cursor agent, hosted VM lifecycle, or Workshop application. Restore behavior has not yet been verified end to end on a fresh Linux machine.
