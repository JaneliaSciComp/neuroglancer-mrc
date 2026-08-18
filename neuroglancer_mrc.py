# Open one or more MRC files (optionally using mmap) and host them using
# Neuroglancer as LocalVolume layers.
# Usage: python neuroglancer_mrc.py --mrcfile <filename> [<filename> ...] [--mmap] [--bind-address ADDRESS]
#
# When launched by Fileglancer as a service, the viewer URL is written to
# SERVICE_URL_PATH so it appears in the UI.

import argparse
import os
import signal
from pathlib import Path

import neuroglancer
import neuroglancer.cli
import mrcfile


def add_mrc_layer(state, fname, *, mmap=False, layer_name=None):
    if mmap:
        d = mrcfile.mmap(fname, permissive=True)
    else:
        d = mrcfile.open(fname, permissive=True)

    if layer_name is None:
        layer_name = os.path.splitext(os.path.basename(fname))[0]

    state.layers[layer_name] = neuroglancer.ImageLayer(
        source=neuroglancer.LocalVolume(d.data)
    )


def unique_layer_names(fnames):
    """Derive a unique layer name per file, falling back to a counter suffix
    for files that share a basename."""
    counts = {}
    names = []
    for fname in fnames:
        base = os.path.splitext(os.path.basename(fname))[0]
        counts[base] = counts.get(base, 0) + 1
        names.append(base if counts[base] == 1 else f"{base}_{counts[base]}")
    return names


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--mrcfile", action='extend', dest='mrcfile',
                    type=Path, default=[], nargs='+',
                    help='Input file. Repeat for multiple files.')
    ap.add_argument("--mmap", action="store_true")

    neuroglancer.cli.add_server_arguments(ap)
    args = ap.parse_args()

    neuroglancer.cli.handle_server_arguments(args)

    viewer = neuroglancer.Viewer()

    url = str(viewer)
    print(url, flush=True)

    # Write URL for Fileglancer service discovery
    service_url_path = os.environ.get("SERVICE_URL_PATH")
    if service_url_path:
        with open(service_url_path, "w") as f:
            f.write(url)

    with viewer.txn() as s:
        for fname, layer_name in zip(args.mrcfile, unique_layer_names(args.mrcfile)):
            add_mrc_layer(s, fname, mmap=args.mmap, layer_name=layer_name)

    signal.pause()

