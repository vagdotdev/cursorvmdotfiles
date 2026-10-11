# From a laptop to the Cursor-style desktop

Give your coding agent this repository twice: once to prepare the USB, and again after Linux installation to finish the desktop. It should start with [AGENTS.md](AGENTS.md).

## First visit: prepare Linux

Suggested prompt:

> Help me install Ubuntu and recreate this desktop. Read AGENTS.md. Check my laptop and USB, download and verify the right ISO, prepare the installation USB, and leave instructions for resuming after installation. Show me the exact disk before erasing it.

### Choose the image

The reference was Ubuntu 24.04.4 with XFCE added separately. For a typical Intel/AMD laptop, use the latest supported **Ubuntu 24.04 LTS Desktop amd64** point release from [Ubuntu's official release index](https://releases.ubuntu.com/releases/24.04/). The regular Ubuntu desktop installer gives you a usable system first; XFCE and this appearance are added afterward. Existing GNOME need not be removed.

Use current supported media and check the laptop's Wi-Fi, graphics, storage, and firmware compatibility. The USB-writing Mac's CPU does not determine the target laptop's ISO architecture. This generic procedure is not an Apple Silicon Mac installation guide; those machines need a separate hardware-specific Linux path.

### Verify and write the USB

Download the ISO plus `SHA256SUMS` and `SHA256SUMS.gpg` from the same official release directory. Follow [Ubuntu's verification guide](https://ubuntu.com/tutorials/how-to-verify-ubuntu): verify the checksum file's signature with the authenticated Ubuntu signing key, then check the downloaded ISO's SHA-256 against its exact filename entry. Do not accept an unverified checksum or continue after a mismatch.

Use a USB drive comfortably larger than the ISO (16 GB or more is a practical choice for these images). Writing it erases that USB. Identify its model and capacity first, and use [Ubuntu's current USB creation instructions](https://ubuntu.com/desktop/docs/en/latest/how-to/create-a-bootable-usb-stick/) for your host: for example, Etcher on macOS or Rufus on Windows. Finish the writer's verification before ejecting.

Keep the repo URL and a short handoff on another device or cloud account, not only on a disk about to be erased. Do not put the ISO in Git.

### Boot and install

Boot the target laptop from the USB using its manufacturer-specific boot menu. Try the live environment first to check Wi-Fi, trackpad, display, sound, and storage detection. Install Ubuntu, choosing the intended disk and whether to erase, dual-boot, and use encryption. Those choices belong to the user. Remove the USB when prompted and boot the installed system.

The agent may lose access during reboot. Firmware screens and the installer may need your keyboard/mouse input. No script in this repo flashes or erases a disk automatically.

## Second visit: finish the desktop

Suggested prompt:

> Ubuntu is installed. Read AGENTS.md and complete the XFCE desktop setup from this repository. Back up existing settings, apply the captured look, and compare the result to the screenshots.

Clone the repo with GitHub access. Because this repository is private, other people/agents need collaborator access or an authorized local copy.

```sh
sudo apt update
sudo apt install git python3 xfce4 xfce4-terminal thunar plank dconf-cli libglib2.0-bin fontconfig procps gtk2-engines-murrine gtk2-engines-pixbuf
# Authenticate to GitHub using your agent's normal credential flow, then:
git clone https://github.com/vagdotdev/cursorvmdotfiles.git
cd cursorvmdotfiles
python3 scripts/apply.py --dry-run
python3 scripts/apply.py
```

Run the appearance installer as your regular Linux user, **not with sudo**, outside an active XFCE session. On a fresh standard Ubuntu install, the existing GNOME session is fine. If already using XFCE, log out and run it from a text console/SSH. Package installation may ask about the display manager; keep a working existing display manager unless there is a specific reason to change it.

The script:

- Verifies the captured files against their manifest.
- Backs up destination files under `~/.local/state/cursorvmdotfiles/backup-*`, recording previously absent paths too.
- Installs captured themes, icons, fonts, backgrounds, and Plank assets in your account's `~/.local/share`.
- Applies the XFCE/GTK settings and adjusts the panel icon to the local asset path.
- Leaves the VM-specific monitor XML alone and schedules wallpaper/dock setup for your actual XFCE session.

Log out, select **Xfce Session** on the login screen, and log in. The finishing script runs once; its log is `~/.local/state/cursorvmdotfiles/session.log`. It sets the wallpaper on detected monitors/workspaces and configures Plank. `session-complete` means those commands succeeded, not that visual verification is finished.

The captured browser dock item expects Chrome. If Chrome is not installed, replace it with your installed browser through Plank; do not assume the bundled launcher installs the app. Check the dock and terminal visually, open Thunar and a browser, and log out/in once to verify persistence. See [RESTORE.md](RESTORE.md) for reference settings and manual options.

## Recovery and limits

Keep the backup directory. Its `paths.json` lists each affected path relative to your home and whether it existed before. While logged out of XFCE, restore the saved version for existing paths and remove only the installer-created paths recorded as previously absent. This rolls back those locations to their pre-install state; preserve any later user changes first. Plank's previous dconf data is in `plank-before.dconf`, and previous wallpaper properties are in `desktop-before.txt` under the state directory. The agent should use those records to revert the finishing stage too.

The installer checks for standard XDG locations and refuses existing install state or symlink destinations that need manual handling. It does not install Cursor, Workshop, remote access, GPU drivers, or cloud services. It does not change partitions or system fonts/themes. Other distributions and XFCE versions may need adaptation.

Validation so far covers capture integrity, script syntax, dry-run behavior, and a mocked installation into a disposable home. USB flashing, a fresh hardware installation, and the first-login desktop behavior still need a real Linux verification run.
