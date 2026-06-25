# CryoEM MRC Viewer

Visualize MRC files (cryo-electron microscopy data) using Neuroglancer.

Based on the [neuroglancer_mrc.py gist](https://gist.github.com/kephale/59a255383e9e1f5f096dedf657a5a091) by [@kephale](https://github.com/kephale). This repo adds [pixi](https://pixi.sh) dependency management and a manifest to run as a [Fileglancer](https://github.com/JaneliaSciComp/fileglancer) app.

## Requirements

- [pixi](https://pixi.sh)

## Installation

```bash
pixi install
```

## Usage

```bash
# Basic usage
pixi run python neuroglancer_mrc.py --mrcfile <your-file.mrc>

# With memory-mapped file (for large files)
pixi run python neuroglancer_mrc.py --mrcfile <your-file.mrc> --mmap

# Specify bind address
pixi run python neuroglancer_mrc.py --mrcfile <your-file.mrc> --bind-address 0.0.0.0
```

The viewer URL will be printed to the console and saved to `/tmp/neuroglancer_viewer_url.txt`.
