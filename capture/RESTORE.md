# Cursor desktop appearance reference

Captured 2026-09-26 from Ubuntu 24.04.4, XFCE.

Original archive SHA256: 17274503adf50a3ab3c533b3af1c0d792aa04c92b00df6d53a8f95d483db6aee

## Contents
- Original wallpaper: bundle/system/usr/share/backgrounds/desktop-background-3.png
- WhiteSur GTK/XFWM themes, icons and cursors; custom Cursor panel icon.
- Inter, JetBrains Mono and DejaVu font files.
- XFCE appearance, window manager, panel, desktop, terminal, Thunar and display XML.
- GTK3 settings and custom CSS, Plank configuration, launchers and dconf export.
- Package versions, installed-font inventory and readable XFCE settings in bundle/manifest.
- desktop.png: unobstructed reference desktop. file-manager.png: open Thunar.

## Restore on Ubuntu XFCE
Use a separate account/session first and back up existing configuration. Install xfce4, xfce4-terminal, thunar, plank, dconf-cli, gtk2-engines-murrine and gtk2-engines-pixbuf. Package versions from the reference are recorded in manifest/packages.tsv; repository versions may differ. Chrome is needed only for the browser dock launcher.

1. Copy bundle/system/usr/share contents to /usr/share, preserving symlinks and permissions.
2. While the destination XFCE account is logged out, copy the contents of bundle/home/home/ubuntu/.config into that account's .config. Set ownership to that account.
3. Do not blindly restore displays.xml: it records the reference monitor. Adapt desktop wallpaper monitor/workspace properties for the destination output, keeping the exact supplied wallpaper path.
4. In the destination account run `dconf load /net/launchpad/plank/ < bundle/manifest/plank.dconf`, `fc-cache -f`, and refresh icon caches.
5. Start Plank at XFCE login. The bundle records dock settings and launcher entries; install their target applications.
6. Log in and compare both screenshots. Monitor geometry, DPI, font rendering and software versions affect exact pixels.

This is an appearance export, not a full computer backup. Credentials, history, browser profiles and project contents are excluded. Restoration has not been executed or visually verified on the destination yet. Font/theme licensing files present within copied asset directories are preserved; no additional license audit was performed.
