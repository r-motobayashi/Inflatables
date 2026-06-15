import os
import sys

os.environ.setdefault("MPLCONFIGDIR", "/private/tmp")
sys.path.append("..")

import MeshFEM  # noqa: F401
import benchmark
import inflation
import mesh
import numpy as np
from py_newton_optimizer import NewtonOptimizerOptions
from tri_mesh_viewer import OffscreenTriMeshViewer


def main(state_path):
    state = np.load(state_path, allow_pickle=True)

    m = mesh.Mesh(state["vertices"], state["triangles"])
    fuse_markers = state["fuse_markers"].astype(bool)
    isheet = inflation.InflatableSheet(m, fuse_markers)
    isheet.pressure = float(state["pressure"])

    opts = NewtonOptimizerOptions()
    for name, value in zip(state["opt_names"], state["opt_values"]):
        setattr(opts, str(name), value.item() if hasattr(value, "item") else value)

    total_iters = int(opts.niter)
    update_every = int(state["update_every"])
    if update_every < 1:
        raise ValueError("update_every must be >= 1")
    opts.niter = update_every

    out = str(state["out"].item())
    width = int(state["width"])
    height = int(state["height"])
    wireframe = bool(state["wireframe"])

    oview = OffscreenTriMeshViewer(isheet, width=width, height=height, wireframe=wireframe)
    benchmark.reset()
    oview.recordStart(out, writeFirstFrame=True)
    try:
        last_report = None
        for _ in range(0, total_iters, update_every):
            last_report = inflation.inflation_newton(
                isheet,
                isheet.rigidMotionPinVars,
                opts,
                callback=None,
            )
            oview.update()
            if getattr(last_report, "success", False):
                break
        benchmark.report()
        return last_report
    finally:
        oview.recordStop()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: record_mesh_inflation_offscreen.py STATE.npz")
    main(sys.argv[1])
