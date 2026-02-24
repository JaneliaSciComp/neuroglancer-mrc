# Open an MRC file (optionally using mmap) and host it using Neuroglancer as a LocalVolume.
# Usage: python neuroglancer_mrc.py --mrcfile <filename> [--mmap] [--bind-address ADDRESS]
#
# When launched by Fileglancer as a service, the viewer URL is written to
# SERVICE_URL_PATH so it appears in the UI.

import argparse
import os
import signal

import neuroglancer
import neuroglancer.cli
import mrcfile


def add_mrc_layer(state, fname, *, mmap=False):
    if mmap:
        d = mrcfile.mmap(fname, permissive=True)
        layer_name = "mrc_mmap"
    else:
        d = mrcfile.open(fname, permissive=True)
        layer_name = "mrc"

    state.layers[layer_name] = neuroglancer.ImageLayer(
        source=neuroglancer.LocalVolume(d.data)
    )


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--mrcfile", type=str, required=True)
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
        add_mrc_layer(s, args.mrcfile, mmap=args.mmap)

    signal.pause()

