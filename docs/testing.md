# Validation scope

2026-11-13: build 2 passed isolated tests against extracted official Unraid 7.3.2, 7.3.4 and 7.3.5 system files: Python/pip/venv, offline wheel install/import, SSL/OS CA paths, compression/SQLite/ctypes/readline/curses/gdbm, package installation and removal, offline reinstall, ownership/corrupt-cache/unknown-OS rejection, and restoration of the previous Python 3.11.15 package. An existing private consumer safety suite passed under both interpreters. Private server scripts and logs are intentionally excluded from this repository.

Earlier build 1 passed automatic cached plugin restoration during an isolated 7.3.5 QEMU boot, actual status-page rendering, Plugins-page update indication, CLI plugin update and GUI return to up-to-date. Direct kernel boot was used; physical USB firmware boot was not tested. A normal guest shutdown stalled in Unraid service shutdown; syncing and remounting flash read-only followed by guest forced poweroff was used. Full graceful shutdown is not a verified pass.

7.3.4 testing is userland compatibility testing, not a booted 7.3.4 VM. No production storage, UPS, third-party workload or email/push notification delivery is certified by these tests. Hosted release testing is recorded separately after publication.

The runtime smoke test is `smoke.py`. Run it only in a disposable test environment with this interpreter installed. It creates temporary venvs and performs an offline wheel installation.

Known scope limits: no Tkinter; decimal uses its Python implementation rather than the optional C accelerator; no optional Samba/libvirt/dbus bindings or PyYAML. NFS diagnostics requiring `/proc` and PyYAML were not full operational passes. Hashed CA directories load lazily; empty initial SSL certificate counts are not themselves a missing-store failure.
