#!/bin/bash
# Local candidate. No network downloads and no Python dependency for recovery.
set -euo pipefail
name=nexus-python
prefix=/opt/nexus-python/3.15.2
fail() { echo "nexus-python: $*" >&2; exit 1; }
platform() {
  [[ $EUID == 0 ]] || fail 'root required'
  case "$(cat /etc/unraid-version)" in
    'version="7.3.2"'|'version="7.3.4"'|'version="7.3.5"'|'version="7.4.0"') ;;
    *) fail 'Unraid version not validated' ;;
  esac
}
preflight() {
  platform
  [[ ! -e /boot/config/plugins/dwpython.plg ]] || fail 'dwpython still enabled; follow migration plan'
  [[ ! -e /boot/config/plugins/iSCSIgui.plg && ! -e /boot/config/plugins/iSCSIgui-dev.plg ]] || fail 'competing Python provider'
  for cmd in python python3 pip pip3; do
    for base in /usr/bin /usr/local/bin; do
      p=$base/$cmd
      if [[ -e $p || -L $p ]]; then
        [[ -L $p && $(readlink "$p") == "$prefix/bin/"* ]] || fail "unowned interpreter/tool: $p"
      fi
    done
  done
}
case "${1:-}" in
  preflight) preflight ;;
  activate)
    preflight
    "$prefix/bin/python3.15" -I -B -c 'import ssl,sqlite3,ctypes,bz2,lzma,zlib,venv; assert __import__("sys").version_info[:3] == (3,15,2)'
    for cmd in python python3; do ln -sfn "$prefix/bin/python3.15" "/usr/bin/$cmd"; done
    for cmd in pip pip3; do ln -sfn "$prefix/bin/pip3.15" "/usr/bin/$cmd"; done
    ;;
  deactivate)
    platform
    for cmd in python python3 pip pip3; do
      p=/usr/bin/$cmd
      if [[ -L $p && $(readlink "$p") == "$prefix/bin/"* ]]; then rm -- "$p"; fi
    done
    # Do not remove data, cached packages, virtual environments or other interpreters.
    ;;
  *) fail 'usage: manage.sh preflight|activate|deactivate' ;;
esac
