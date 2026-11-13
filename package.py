"""Run inside build container; create locally testable Slackware archive and PLG.
The default URL is deliberately nonfunctional. Publishing requires separate approval.
"""
import pathlib, shutil, subprocess, hashlib, json, os
from xml.sax.saxutils import escape
work=pathlib.Path('/work'); out=pathlib.Path('/out'); stage=pathlib.Path('/tmp/python-package')
stage.mkdir()
shutil.copytree('/opt/nexus-python', stage/'opt/nexus-python', symlinks=True)
plugin=stage/'usr/local/emhttp/plugins/nexus-python'; plugin.mkdir(parents=True)
for name in ('manage.sh','nexus-python.page'):
    shutil.copy2(work/name,plugin/name)
(plugin/'manage.sh').chmod(0o755)
licenses=stage/'opt/nexus-python/3.15.2/licenses'; licenses.mkdir()
shutil.copy2('/build/Python-3.15.2/LICENSE',licenses/'CPython-LICENSE')
for p in pathlib.Path('/usr/share/doc').glob('*/copyright'):
    # Retain build dependency copyright notices, including all bundled libraries.
    shutil.copy2(p, licenses/(p.parent.name+'.copyright'))
(stage/'install').mkdir()
(stage/'install/slack-desc').write_text('nexus-python: Nexus Python 3.15.2\nnexus-python: Private runtime, pip and virtual environments.\n')
package='nexus-python-3.15.2-x86_64-3.txz'
subprocess.run(['tar','--sort=name','--mtime=@1794528000','--owner=0','--group=0','--numeric-owner','-cJf',str(out/package),'-C',str(stage),'.'],check=True)
sha=hashlib.sha256((out/package).read_bytes()).hexdigest()
md5=hashlib.md5((out/package).read_bytes()).hexdigest()
(out/(package+'.sha256')).write_text(sha+'  '+package+'\n')
base=os.environ.get('RELEASE_BASE','https://example.invalid/nexus-python')
if not base.startswith('https://'): raise ValueError('release base must be HTTPS')
package_base=os.environ.get('PACKAGE_BASE',base)
if not package_base.startswith('https://'): raise ValueError('package base must be HTTPS')
cache='/boot/config/plugins/nexus-python/'+package
guard=(work/'manage.sh').read_text().replace('case "${1:-}" in','set -- preflight\ncase "${1:-}" in')
install=f'''set -eu
echo '{sha}  {cache}' | sha256sum -c -
/sbin/installpkg {cache}
/bin/bash /usr/local/emhttp/plugins/nexus-python/manage.sh activate
'''
remove='''set -eu
/bin/bash /usr/local/emhttp/plugins/nexus-python/manage.sh deactivate
/sbin/removepkg nexus-python
'''
plg=f'''<?xml version="1.0"?>
<PLUGIN name="nexus-python" author="Nexus" version="2026.11.14.1" min="7.3.2" max="7.4.0" launch="Settings/nexus-python" pluginURL="{escape(base)}/nexus-python.plg">
<CHANGES>Local candidate: Python 3.15.2, pip and venv. Exact supported OS guard: 7.3.2, 7.3.4, 7.3.5 and 7.4.0. No uv or script editor.</CHANGES>
<FILE Run="/bin/bash"><INLINE>{escape(guard)}</INLINE></FILE>
<FILE Name="{cache}"><URL>{escape(package_base)}/{package}</URL><MD5>{md5}</MD5></FILE>
<FILE Run="/bin/bash"><INLINE>{escape(install)}</INLINE></FILE>
<FILE Run="/bin/bash" Method="remove"><INLINE>{escape(remove)}</INLINE></FILE>
</PLUGIN>
'''
(out/'nexus-python.plg').write_text(plg)
(out/'manifest.json').write_text(json.dumps({'python':'3.15.2','source_sha256':'8b5536d280142ecf6cdfe15d12a21ba1c65e300bbf7b28a8d0cdb849575797de','package':package,'package_sha256':sha,'release_base':base,'package_base':package_base,'deployment_status':'RELEASE PREPARED - Nexus installation requires separate approval'},indent=2)+'\n')
for name in ('configure.log','make.log','install.log','build-packages.txt'):
    shutil.copy2('/build/'+name,out/name)
print(json.dumps({'package':package,'bytes':(out/package).stat().st_size,'sha256':sha}))
