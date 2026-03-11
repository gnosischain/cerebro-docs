# cryo-base

cryo-base is a Docker base image containing a pre-compiled [Cryo](https://github.com/paradigmxyz/cryo) binary with custom patches. It serves as the foundation for the cryo-indexer and any other tools that need Cryo functionality.

## Purpose

Compiling the Cryo Rust binary from source takes several hours, especially on ARM64 architecture. cryo-base provides a ready-to-use image that is built weekly (or on-demand) so downstream projects can start quickly without a lengthy build step.

## Contents

The base image includes:

- **Debian bullseye-slim** base OS
- **Cryo binary** at `/usr/local/bin/cryo` (compiled from a pinned commit with custom patches applied)
- **Python 3.x** with pip
- **Build essentials** (gcc, g++)
- **OpenSSL libraries** and CA certificates

## Custom Patches

The image includes a modular patching system that modifies the Cryo source code before compilation. Current patches:

| Patch | File | Description |
|-------|------|-------------|
| `01_null_traces.py` | Trace-related Rust source | Makes trace functions null-safe for RPCs that return `null` instead of `[]` |
| `02_withdrawals.py` | Blocks dataset source | Adds `withdrawals` column support to the blocks dataset |

Patches are applied in alphabetical order by the `apply_patches.py` runner during the Docker build.

### Adding New Patches

To add a new patch, create a Python file in the `patches/` directory following the naming convention `NN_description.py`:

```python
#!/usr/bin/env python3
from pathlib import Path

DESCRIPTION = "Short description of what this patch does"
TARGET_FILE = Path("crates/freeze/src/path/to/file.rs")

def main():
    # Return True (success), False (failure), or "skipped" (already applied)
    ...
```

## Architecture Support

| Architecture | Support |
|-------------|---------|
| `linux/amd64` | Yes |
| `linux/arm64` | Yes |

Both architectures are built in parallel during CI.

## Usage

Reference cryo-base as the base image in your Dockerfile:

```dockerfile
FROM ghcr.io/gnosischain/cryo-base:latest

WORKDIR /app
COPY . .
# Your application setup...
```

Or run Cryo directly:

```bash
docker run --rm -v "$(pwd)":/data cryo-base:latest \
  cryo blocks \
  --blocks 39828831:39828831 \
  --rpc 'https://your-rpc-url' \
  --include-columns block_number timestamp withdrawals_root withdrawals \
  -o /data
```

## Build Schedule

- **Automatic builds** -- Every Sunday at 2 AM UTC via CI
- **Manual builds** -- Triggered on push to main branch or via workflow dispatch

## Versioning

| Tag | Description |
|-----|-------------|
| `latest` | Most recent build |
| `YYYYMMDD` | Date-based tags for pinning specific versions |

## Update Process

When Cryo releases a new version:

1. Update the commit hash in the `Dockerfile`
2. Push to main branch or trigger a manual build
3. Wait for build completion (typically 2-3 hours)
4. Update downstream images (cryo-indexer) to use the new base
