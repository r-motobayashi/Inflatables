import argparse
import os
import sys

sys.path.append("..")

import MeshFEM  # noqa: F401
import benchmark
import inflation
import numpy as np
import parametric_pillows
import wall_generation
from py_newton_optimizer import NewtonOptimizerOptions
from tri_mesh_viewer import OffscreenTriMeshViewer


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--circles", type=int, default=8)
    parser.add_argument("--points", type=int, default=50)
    parser.add_argument("--tri-area", type=float, default=0.001)
    parser.add_argument("--pressure", type=float, default=20 * 3.75)
    parser.add_argument("--niter", type=int, default=1000)
    parser.add_argument("--width", type=int, default=768)
    parser.add_argument("--height", type=int, default=640)
    parser.add_argument("--out", default="cc_inflate.mp4")
    args = parser.parse_args()

    m, fuse_markers, _ = wall_generation.triangulate_channel_walls(
        *parametric_pillows.concentricCircles(args.circles, args.points),
        args.tri_area,
    )
    isheet = inflation.InflatableSheet(m, np.array(fuse_markers) != 0)
    isheet.pressure = args.pressure

    opts = NewtonOptimizerOptions()
    opts.niter = args.niter

    oview = OffscreenTriMeshViewer(isheet, width=args.width, height=args.height, wireframe=True)

    benchmark.reset()
    try:
        oview.recordStart(args.out)
        cr = inflation.inflation_newton(
            isheet,
            isheet.rigidMotionPinVars,
            opts,
            callback=lambda it: oview.update(),
        )
        benchmark.report()
        return cr
    finally:
        oview.recordStop()


if __name__ == "__main__":
    os.environ.setdefault("MPLCONFIGDIR", "/private/tmp")
    main()
