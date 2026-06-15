import os
import pickle
import sys

os.environ.setdefault("MPLCONFIGDIR", "/private/tmp")
sys.path.append("..")

import MeshFEM  # noqa: F401
import benchmark
import inflation
from tri_mesh_viewer import OffscreenTriMeshViewer


def main(state_path):
    with open(state_path, "rb") as f:
        state = pickle.load(f)

    isheet = state["isheet"]
    fixed_vars = state["fixed_vars"]
    opts = state["opts"]
    out = state["out"]
    width = state["width"]
    height = state["height"]
    wireframe = state["wireframe"]
    update_every = int(state["update_every"])

    if update_every < 1:
        raise ValueError("update_every must be >= 1")

    total_iters = int(opts.niter)
    opts.niter = update_every

    oview = OffscreenTriMeshViewer(isheet, width=width, height=height, wireframe=wireframe)
    benchmark.reset()
    oview.recordStart(out, writeFirstFrame=True)
    try:
        last_report = None
        for _ in range(0, total_iters, update_every):
            last_report = inflation.inflation_newton(
                isheet,
                fixed_vars,
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
        raise SystemExit("usage: record_inflation_state_offscreen.py STATE.pkl")
    main(sys.argv[1])
