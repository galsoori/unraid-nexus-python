"""Collect exact Debian source versions for privately bundled shared libraries."""
import pathlib, subprocess, json, shutil
root=pathlib.Path('/opt/nexus-python/3.15.2')
out=pathlib.Path('/sources'); out.mkdir(exist_ok=True)
source_list=pathlib.Path('/etc/apt/sources.list.d/debian.sources')
source_list.write_text(source_list.read_text().replace('Types: deb\n','Types: deb deb-src\n'))
subprocess.run(['apt-get','update'],check=True)
packages=set()
for name in json.loads((root/'private-libraries.json').read_text()):
    library=pathlib.Path(name).name
    owner=subprocess.check_output(['dpkg-query','-S','*/'+library],text=True).splitlines()[0].rsplit(': ',1)[0]
    source=subprocess.check_output(['dpkg-query','-W','-f=${source:Package}=${source:Version}',owner],text=True)
    packages.add(source)
for package in sorted(packages):
    subprocess.run(['apt-get','source','--download-only',package],cwd=out,check=True)
(out/'debian-source-versions.txt').write_text('\n'.join(sorted(packages))+'\n')
shutil.copy2('/build/build-packages.txt',out/'build-packages.txt')
