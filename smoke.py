"""Safe runtime checks; no Nexus, device or network access."""
import sys, ssl, sqlite3, ctypes, bz2, lzma, zlib, hashlib, json, pathlib, subprocess, tempfile, venv, zipfile
from compression import zstd
assert sys.version_info[:3] == (3,15,2), sys.version
for module in ('readline','curses','dbm.gnu','decimal','multiprocessing','uuid','xml.parsers.expat'):
    __import__(module)
payload=b'nexus-python-check'*100
for module in (bz2,lzma,zlib,zstd): assert module.decompress(module.compress(payload)) == payload
assert hashlib.sha256(payload).digest()
db=sqlite3.connect(':memory:'); assert db.execute('select 42').fetchone()==(42,)
assert ctypes.CDLL(None)
context=ssl.create_default_context()
paths=ssl.get_default_verify_paths()
# OpenSSL loads hashed-directory certificates lazily during verification.
# A zero eager-load count alone does not mean the store is absent.
hashed=list(pathlib.Path(paths.capath).glob('*.0')) if paths.capath else []
assert context.cert_store_stats()['x509_ca'] > 0 or any(p.is_file() for p in hashed), ('OS CA store not found',paths)
if not context.cert_store_stats()['x509_ca']:
    probe=ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    probe.load_verify_locations(cafile=str(next(p for p in hashed if p.is_file())))
    assert probe.cert_store_stats()['x509_ca'] > 0
with tempfile.TemporaryDirectory() as d:
    venv.create(d,with_pip=True)
    p=pathlib.Path(d)/'bin/python'
    subprocess.run([str(p),'-I','-c','import sys; assert sys.prefix != sys.base_prefix'],check=True)
    subprocess.run([str(p),'-m','pip','--version'],check=True)
    wheel=pathlib.Path(d)/'nexus_probe-1.0-py3-none-any.whl'
    with zipfile.ZipFile(wheel,'w') as z:
        z.writestr('nexus_probe.py','VALUE = 42\n')
        z.writestr('nexus_probe-1.0.dist-info/METADATA','Metadata-Version: 2.1\nName: nexus-probe\nVersion: 1.0\n')
        z.writestr('nexus_probe-1.0.dist-info/WHEEL','Wheel-Version: 1.0\nGenerator: local-test\nRoot-Is-Purelib: true\nTag: py3-none-any\n')
        z.writestr('nexus_probe-1.0.dist-info/RECORD','')
    subprocess.run([str(p),'-m','pip','install','--no-index','--disable-pip-version-check',str(wheel)],check=True)
    subprocess.run([str(p),'-I','-c','import nexus_probe; assert nexus_probe.VALUE == 42'],check=True)
print(json.dumps({'result':'PASS','python':sys.version,'ssl':ssl.OPENSSL_VERSION,'ca_store':context.cert_store_stats(),'default_ca_paths':paths._asdict(),'hashed_ca_count':len(hashed),'sqlite':sqlite3.sqlite_version}))
