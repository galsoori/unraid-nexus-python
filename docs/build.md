# Build and release

Use Docker on Linux/x86-64. Download official CPython 3.15.2 to `downloads/Python-3.15.2.tar.xz` and verify SHA-256 `8b5536d280142ecf6cdfe15d12a21ba1c65e300bbf7b28a8d0cdb849575797de`. The source is also included with this release.

```sh
docker build -t nexus-python-local:3.15.2 .
mkdir -p dist
docker run --rm --network none \
  -e RELEASE_BASE=https://raw.githubusercontent.com/galsoori/unraid-nexus-python/main \
  -e PACKAGE_BASE=https://github.com/galsoori/unraid-nexus-python/releases/download/2026.11.14.1 \
  -v "$PWD:/work:ro" -v "$PWD/dist:/out" \
  nexus-python-local:3.15.2 /opt/nexus-python/3.15.2/bin/python3.15 /work/package.py
```

The Debian base image and CPython archive are pinned. Apt dependency versions are recorded, but repository contents and build timestamps can change; a fresh build is not promised to produce identical bytes. Retain the actual build environment privately and publish new checksums for newly tested builds.

`bundle.py` copies non-glibc dependencies into the private runtime, adjusts ELF RUNPATH with patchelf and strips debug symbols. Unraid's libc/loader and OpenSSL 3 remain external. `collect_sources.py`, run in the original build image with an output directory mounted at `/sources`, downloads the exact Debian source versions for bundled libraries, including distribution patches. Release source archives contain these files, the CPython archive and build recipes. The original package includes the corresponding copyright/license notices. Dynamic libraries remain replaceable within the private prefix.

For each release, increase plugin version and package build/version; never replace bytes under an existing package release URL. Test on every allowed OS, publish the package/source/checksum assets, verify anonymous HTTPS downloads, then publish the stable manifest. Test in an isolated VM before production migration. Do not put credentials, VM disks, local backups or server configuration in the repository.
