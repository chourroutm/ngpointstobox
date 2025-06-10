# ngpointstobox ⏹️
Script to replace a point cloud by their bounding box in a Neuroglancer link or state

## Dependencies

- neuroglancer
- numpy

Install all of them with:

```bash
pip install neuroglancer numpy
```

## Usage

Pass either a Neuroglancer URL (`--url`) between single quotes or the path to a JSON file with a Neuroglancer state (`--json`).

```bash
python points_to_bbox.py --url 'https://neuroglancer-demo.appspot.com/#!...' [--keep-points] [--suffix "_bbox"] [--margin 50]
```

```bash
python points_to_bbox.py --json '/path/to/state.json' [--keep-points] [--suffix "_bbox"] [--margin 50]
```

By default, annotation layers are replaced by a new annotation layer with their bounding box.

With the boolean argument `--keep-points` ¦ `-k`, the annotation layer is not replaced and the new annotation layer is created with "_bbox" (or any string passed with `--suffix` ¦ `-s`) appended to the layer name.

With the integer argument `--margin` ¦ `-m`, the bounding box is expanded by this amount of voxels in every direction.
