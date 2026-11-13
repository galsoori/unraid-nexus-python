"""Bundle non-glibc shared dependencies privately; never replace Unraid libraries."""
import pathlib, subprocess, shutil, json, hashlib
root = pathlib.Path('/opt/nexus-python/3.15.2')
private = root / 'lib/private'
private.mkdir(parents=True, exist_ok=True)
system = {'libc.so.6', 'libm.so.6', 'libpthread.so.0', 'libdl.so.2', 'librt.so.1', 'libutil.so.1', 'libresolv.so.2', 'libssl.so.3', 'libcrypto.so.3'}
def dynamic_elf(p):
    if not p.is_file() or p.is_symlink(): return False
    with p.open('rb') as f: h = f.read(18)
    return h[:4] == b'\x7fELF' and int.from_bytes(h[16:18], 'little') in (2,3)
elfs = [p for p in root.rglob('*') if dynamic_elf(p)]
pending = list(elfs)
while pending:
    p = pending.pop()
    for line in subprocess.check_output(['ldd', str(p)], text=True).splitlines():
        if '=>' not in line: continue
        name, rest = line.strip().split(' => ', 1)
        if name in system: continue
        source = pathlib.Path(rest.split()[0])
        if not source.is_absolute(): raise RuntimeError(line)
        dest = private / name
        if not dest.exists():
            shutil.copy2(source.resolve(), dest)
            pending.append(dest)
for p in elfs + list(private.iterdir()):
    temp = p.with_name(p.name+'.patched')
    shutil.copy2(p, temp)
    subprocess.run(['patchelf', '--set-rpath', str(private), str(temp)], check=True)
    subprocess.run(['strip', '--strip-debug', str(temp)], check=True)
    temp.replace(p)
for p in root.rglob('*.a'):
    subprocess.run(['strip','--strip-debug',str(p)],check=True)
subprocess.run(['dpkg-query', '-W'], stdout=open('/build/build-packages.txt','w'), check=True)
manifest = {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest() for p in private.iterdir()}
(root/'private-libraries.json').write_text(json.dumps(manifest, indent=2)+'\n')
