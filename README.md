# Nexus Python for Unraid

A small, independently maintained host Python plugin for Unraid. Provides Python 3.15.2, pip 26.2.2, virtual environments and a read-only status page. No script editor, uv, automatic Python-version upgrades or changes to Unraid system libraries.

Supported exact Unraid versions: **7.3.2, 7.3.4, 7.3.5 and 7.4.0**, x86-64. Other versions are rejected. Unraid 7.4.0 compatibility was tested in an isolated VM; physical hardware behavior still requires verification after upgrading. It is not an official Unraid or Python project.

## Installation

Install through Unraid's Plugins / Install Plugin page using:

```text
https://raw.githubusercontent.com/galsoori/unraid-nexus-python/main/nexus-python.plg
```

Installation refuses an enabled dwpython or iSCSI Python provider and refuses unowned Python/pip commands. Do not install over an existing host Python provider without a backup and a planned migration.

The package lives in `/opt/nexus-python/3.15.2`. Activation creates owned `/usr/bin/python`, `python3`, `pip` and `pip3` links. The cached package is restored by the Unraid plugin boot process. Status is shown under Settings / Nexus Python. Normal plugin checks compare the published manifest version; updates are installed through Unraid's plugin manager.

## Maintenance

Updates are built, tested and explicitly published by the maintainer. New upstream Python releases do not automatically become plugin updates. Packages use release-specific URLs, with MD5 for Unraid compatibility and an additional SHA-256 check before installation.

See [build instructions](docs/build.md). Runtime licenses are included under `/opt/nexus-python/3.15.2/licenses`; source archives accompany releases. Original plugin/build code is MIT licensed; bundled components retain their own licenses.
