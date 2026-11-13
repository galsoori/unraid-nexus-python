# Validation scope

2026-11-13: build 2 passed isolated tests against extracted official Unraid 7.3.2, 7.3.4 and 7.3.5 system files: Python/pip/venv, offline wheel install/import, SSL/OS CA paths, compression/SQLite/ctypes/readline/curses/gdbm, package installation and removal, offline reinstall, ownership/corrupt-cache/unknown-OS rejection, and restoration of the previous Python 3.11.15 package. An existing private consumer safety suite passed under both interpreters. Private server scripts and logs are intentionally excluded from this repository.

Earlier build 1 passed automatic cached plugin restoration during an isolated 7.3.5 QEMU boot, actual status-page rendering, Plugins-page update indication, CLI plugin update and GUI return to up-to-date. Direct kernel boot was used; physical USB firmware boot was not tested. A normal guest shutdown stalled in Unraid service shutdown; syncing and remounting flash read-only followed by guest forced poweroff was used. Full graceful shutdown is not a verified pass.

7.3.4 testing is userland compatibility testing, not a booted 7.3.4 VM. No production storage, UPS, third-party workload or email/push notification delivery is certified by these tests.

## Hosted release 2026.11.13.2

In the isolated Unraid 7.3.5 VM, the real plugin checker downloaded the public GitHub manifest over verified HTTPS and detected build 2 as an update from the earlier test release. The Plugins page showed the available version and Update button. The package was absent from the VM cache before testing; Unraid's CLI plugin manager downloaded it from GitHub Releases, checked MD5/SHA-256 and installed it successfully (exit 0). Its SHA-256 matched `313c8589e3bf9ba82d918479bdd6f62609af4c31e962882ab0c30b00acbf8aac`. The GUI then showed version 2026.11.13.2 up-to-date, with Python 3.15.2 active; pip reported 26.2.2.

The VM uses restricted networking with an allowlisted CONNECT proxy for public GitHub downloads. TLS verification remained enabled. Because the guest PHP process did not inherit a shell proxy variable, the isolated guest's wget configuration supplied the proxy. This is a lab-only arrangement, not a plugin requirement or change to a production server. GUI status/notification rendering and CLI update execution were exercised; the GUI Update button itself was not clicked.

The hosted package also passed the runtime smoke test, including a disposable venv and offline wheel install/import, followed by another successful hosted plugin check. No new full reboot test was performed after this hosted update.

The runtime smoke test is `smoke.py`. Run it only in a disposable test environment with this interpreter installed. It creates temporary venvs and performs an offline wheel installation.

Known scope limits: no Tkinter; decimal uses its Python implementation rather than the optional C accelerator; no optional Samba/libvirt/dbus bindings or PyYAML. NFS diagnostics requiring `/proc` and PyYAML were not full operational passes. Hashed CA directories load lazily; empty initial SSL certificate counts are not themselves a missing-store failure.
