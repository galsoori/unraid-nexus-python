# Migration, boot and rollback

Back up the existing Python provider's manifest, complete flash cache/settings/scripts, installed-package list, interpreter links and any dependent custom startup scripts. Verify the archive and retain a private off-server copy. Never publish server configuration or backups.

Prefer a planned reboot migration: move the old provider's manifest outside `/boot/config/plugins`, preserving its cache/settings. Stage the reviewed new manifest and package. Reboot only during an approved maintenance window. The old RAM installation disappears and the new plugin restores Python before the ordinary boot `go` script. Do not use a vendor removal action without reviewing whether it deletes user scripts or environments.

After boot verify `python3 --version`, `python3 -m pip --version`, creation of a disposable venv, the plugin status page, and every identified host Python consumer. Container applications with their own interpreter are separate. Recreate old virtual environments when needed; do not copy version-specific binary modules into Python 3.15.

For rollback, move the new manifest out of the active plugin directory, restore the old manifest and its verified cache, and perform an approved reboot. Recovery uses shell/tar/checksums and the existing plugin installer, not a working Python interpreter. Keep both providers' manifests from being enabled simultaneously.

Removal deletes package-owned files and only interpreter links still pointing into this plugin's prefix. It preserves user environments and flash backups/cache. A live interpreter replacement requires additional care for running Python processes; the documented preferred migration uses a reboot.

Unraid upgrades outside the exact allowlist require compatibility testing and a new plugin release first. Other custom scripts may have their own independent OS guards.
