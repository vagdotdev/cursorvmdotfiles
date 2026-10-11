# Validation status

Checked October 11, 2026:

- Original capture matches its basket source byte-for-byte, including symbolic link targets.
- Original compressed archive SHA-256 matches the recorded capture hash.
- `python3 scripts/apply.py --dry-run` verifies all 43,747 captured files/symlinks without applying settings.
- Python parsing and `sh -n scripts/finish-session.sh` pass.
- A mocked Linux installation into a disposable home checks existing-config backup, per-user assets, omission of VM monitor configuration, autostart command paths, and refusal to overwrite an existing installation/backup.

Not yet tested: actual ISO flashing, installation on laptop hardware, a real Linux first-login run, live XFCE/Plank behavior, or pixel-for-pixel reproduction. The agent following this repository must perform those checks on the destination machine and report any differences.
