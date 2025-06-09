
import argparse

import neuroglancer
import neuroglancer.cli
import neuroglancer.random_token
import numpy as np

def _bounding_box_with_margin(points, margin=0):
    x_coordinates, y_coordinates, z_coordinates = zip(*points)
    return [(min(x_coordinates) - margin, min(y_coordinates) - margin, min(z_coordinates) - margin), (max(x_coordinates) + margin, max(y_coordinates) + margin, max(z_coordinates) + margin)]

def convert_points_to_bbox(state: neuroglancer.ViewerState, keep_points_layer: bool = False, annotation_layer_suffix: str = "_bbox", margin = 0):
    for current_layer in state.layers:
        if not current_layer.visible:
            continue
        if not isinstance(current_layer.layer, neuroglancer.AnnotationLayer):
            continue
        default_transform = neuroglancer.CoordinateSpaceTransform({"matrix": np.eye(4)[:3,:4].tolist(), "outputDimensions": state.dimensions.to_json()})
        new_layer = neuroglancer.LocalAnnotationLayer(
                dimensions=state.dimensions
            )
        all_points = []
        for current_annotation in current_layer.annotations:
            if isinstance(current_annotation, neuroglancer.PointAnnotation):
                all_points.append(current_annotation.point)
            elif isinstance(current_annotation, neuroglancer.LineAnnotation) or isinstance(current_annotation, neuroglancer.AxisAlignedBoundingBoxAnnotation):
                all_points.append(current_annotation.point_a)
                all_points.append(current_annotation.point_b)
        if current_layer.layer.source[0].transform is None:
            new_layer.source[0].transform = default_transform
        else:
            new_layer.source[0].transform = current_layer.layer.source[0].transform
        
        new_layer.annotations.append(
            neuroglancer.AxisAlignedBoundingBoxAnnotation(
                    id=neuroglancer.random_token.make_random_token(),
                    point_a= _bounding_box_with_margin(all_points,margin=margin)[0],
                    point_b= _bounding_box_with_margin(all_points)[1],
                )
        )
        if keep_points_layer:
            state.layers.append(
                name=current_layer.name+annotation_layer_suffix,
                layer=new_layer
            )
            current_layer.visible = False
            break
        else:
            state.layers[current_layer.name] = new_layer
    return state

def main(args=None):
    ap = argparse.ArgumentParser()
    neuroglancer.cli.add_state_arguments(ap, required=True)
    ap.add_argument("--keep_points", "-k", "--keep-points", action="store_true", help="Keep points layer instead of replacing it")
    ap.add_argument("--suffix", "-s", type=str, default="_bbox", help="Suffix for the new annotation layer")
    ap.add_argument("--margin", "-m", type=int, default=0, help="Add margin around the bounding box")
    parsed_args = ap.parse_args()
    new_state = convert_points_to_bbox(state=parsed_args.state, 
                                       keep_points_layer=parsed_args.keep_points, 
                                       annotation_layer_suffix=parsed_args.suffix,
                                       margin=parsed_args.margin,
                                    )
    print(neuroglancer.to_url(new_state))

if __name__ == "__main__":
    main()
