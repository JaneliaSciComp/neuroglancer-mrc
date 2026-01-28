# open an MRC file (optionally using mmap) and host it using Neuroglancer as a LocalVolume
# usage: python -m mrc_neuroglancer.py --mrcfile <filename> [--mmap] [--bind-address ADDRESS]
#
# requirements may be installed from PyPI:
#    neuroglancer
#    mrcfile


import argparse
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

    state.layers[layer_name] = neuroglancer.ImageLayer(source=neuroglancer.LocalVolume(d.data))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--mrcfile", type=str, required=True)
    ap.add_argument("--mmap", action="store_true")

    neuroglancer.cli.add_server_arguments(ap)
    args = ap.parse_args()

    neuroglancer.cli.handle_server_arguments(args)

    viewer = neuroglancer.Viewer()
    
    url_file_path = "/tmp/neuroglancer_viewer_url.txt"
    with open(url_file_path, "w") as url_file:
        print(viewer, file=url_file)
    print(viewer)

    with viewer.txn() as s:
        add_mrc_layer(s, args.mrcfile, mmap=args.mmap)

    signal.pause()

