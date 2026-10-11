# Agent instructions: reproduce the Cursor VM desktop

This repository supports two visits: **prepare Linux installation media**, then **finish the desktop after Linux is installed**. Read README.md, FRESH_INSTALL.md, and PROVENANCE.md first. The user handing you this repo may be starting at either stage; inspect the machine before deciding. Do not begin flashing a disk merely because you are reading these instructions.

## Intended result

Ubuntu 24.04 LTS, XFCE/X11, WhiteSur Light windows, WhiteSur icons/cursors, Inter UI font, JetBrains Mono terminal font, the captured wallpaper, a 28 px top panel, and a centered Plank dock. Preserve the captured files unchanged. This is a visual recreation, not the Cursor agent or VM service.

## Before installation

1. Identify the host OS, **target** laptop model/architecture, current OS, and intended install disk. The machine making the USB may differ from the target. Standard amd64 Ubuntu media is for Intel/AMD PCs, not Apple Silicon Macs. Consult hardware-specific guidance for ARM/Apple Silicon/T2 and stop the generic path if incompatible.
2. For the reference baseline, select the latest supported Ubuntu **24.04 LTS Desktop amd64** point release from the official release index. Recheck hardware support and lifecycle at execution time; do not use an obsolete build just because the capture used 24.04.4. If a different release is necessary, explain the compatibility change and verify the theme there.
3. Download the ISO, SHA256SUMS, and SHA256SUMS.gpg; authenticate the signing key against Ubuntu's official instructions, verify the signature, then compare the exact ISO checksum. Record the source URL, version, hash, and verification outcome.
4. Identify the USB by model, serial if available, capacity, and physical connection. Show the concrete target to the user before destructive writing if it has not already been unambiguously authorized. Never infer `/dev/sda`, `disk2`, or Disk 1. Prepare the media with the official host-appropriate tool and verify completion.
5. Save a handoff with ISO details, target hardware, desired install mode, repository URL, and next steps somewhere that survives the installation. Never save passwords or recovery keys in this repo. Explain the target laptop's boot-menu step and the installer handoff.
6. User firmware interactions, encryption passwords, boot selection, and disk-erasure/dual-boot decisions may require direct user action. The coding agent cannot assume it remains connected through reboot. Do not erase an internal disk without authorization identifying that target.

## After installation

1. Verify `/etc/os-release`, architecture, network, free space, and current account. Obtain this repo with an authenticated GitHub clone if private; do not embed tokens in URLs. Read FRESH_INSTALL.md's post-install section.
2. Install the listed dependencies. Do not install every package in the captured inventory, purge GNOME, repartition, or change disk encryption to apply a theme.
3. Run `python3 scripts/apply.py --dry-run`. Then run `python3 scripts/apply.py` as the destination user while that user's XFCE session is logged out. Use a console/SSH or the existing Ubuntu GNOME session. Do not run the script with sudo.
4. Ask the user to choose **Xfce Session** at login when direct UI action is needed. The first XFCE login runs the per-user finishing script. Inspect its log; resolve any errors. Replace a missing Chrome dock launcher with the chosen installed browser instead of leaving a dead shortcut.
5. Verify actual appearance and behavior: wallpaper, panel, dock, window buttons, font, file manager, browser launch, terminal, network, suspend/wake, and persistence after logout/login. Use capture/desktop.png and capture/file-manager.png as visual references. Inspect applied values with xfconf-query and gsettings; do not call it complete based only on package installation.
6. Report what works, what differs, and anything not tested. Retain the backup and state directory for recovery. The scripts are an initial automation aid; an end-to-end laptop install has not yet been validated.

## Existing configuration and failures

The installer uses per-user directories and creates a manifest-backed backup under `~/.local/state/cursorvmdotfiles/`. It refuses an existing installation state rather than overwriting the original backup. On failure, inspect paths.json and the logs, restore affected settings or repair the failed stage, and preserve the backup. Do not blindly delete state to get past this check. Use RESTORE.md for manual alternatives.

Do not add secrets, SSH keys, browser profiles, shell history, or personal project files to the export. Third-party assets have their own terms; this repo does not grant a blanket redistribution license.
