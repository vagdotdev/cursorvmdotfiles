#!/bin/sh
# Runs once on XFCE login; data/configuration remain local to this account.
set -eu
state="$HOME/.local/state/cursorvmdotfiles"
mkdir -p "$state"
exec >>"$state/session.log" 2>&1
if [ -e "$state/session-complete" ]; then exit 0; fi
date
if [ ! -e "$state/plank-before.dconf" ]; then
    dconf dump /net/launchpad/plank/ > "$state/plank-before.dconf"
fi
dconf load /net/launchpad/plank/ < "$HOME/.local/share/cursorvmdotfiles/plank.dconf"
schema='net.launchpad.plank.dock.settings:/net/launchpad/plank/docks/dock1/'
gsettings set "$schema" theme 'WhiteSur-Light'
gsettings set "$schema" position 'bottom'
gsettings set "$schema" alignment 'center'
gsettings set "$schema" icon-size 48
gsettings set "$schema" zoom-enabled true
gsettings set "$schema" zoom-percent 150
# Let xfdesktop create properties for the actual laptop's monitor(s).
attempt=0
while :; do
    properties=$(xfconf-query -c xfce4-desktop -l 2>/dev/null | grep '/last-image$' || true)
    if [ -n "$properties" ]; then break; fi
    attempt=$((attempt + 1))
    if [ "$attempt" -ge 30 ]; then
        echo 'Wallpaper properties unavailable. Set wallpaper in Desktop Settings and rerun this script.'
        exit 1
    fi
    sleep 1
done
if [ ! -e "$state/desktop-before.txt" ]; then
    xfconf-query -c xfce4-desktop -lv > "$state/desktop-before.txt"
fi
printf '%s\n' "$properties" | while IFS= read -r prop; do
    xfconf-query -c xfce4-desktop -p "$prop" -s "$HOME/.local/share/backgrounds/desktop-background-3.png"
done
xfconf-query -c xfce4-desktop -p /desktop-icons/style -n -t int -s 0
if ! pgrep -u "$(id -u)" -x plank >/dev/null; then plank >/dev/null 2>&1 & fi
touch "$state/session-complete"
echo 'Session settings applied. Visually check dock, wallpaper, icons, and fonts.'
