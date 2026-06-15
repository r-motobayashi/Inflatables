import copy
import os

os.environ.setdefault("MPLCONFIGDIR", "/private/tmp")

import MeshFEM  # noqa: F401
import benchmark
import inflation
from tri_mesh_viewer import OffscreenTriMeshViewer


def record_inflation(
    isheet,
    fixed_vars,
    opts,
    out="cc_inflate.mp4",
    width=768,
    height=640,
    wireframe=True,
    update_every=1,
):
    """
    Record inflation without calling the offscreen renderer from a C++ callback.

    The original demo records from inside Newton's iteration callback. On some
    macOS/Python/pybind11 combinations that can crash the kernel because OpenGL
    and video encoding run while C++ still owns the optimizer stack. This helper
    advances Newton in small chunks and renders after control returns to Python.
    """
    if update_every < 1:
        raise ValueError("update_every must be >= 1")

    total_iters = int(opts.niter)
    chunk_opts = copy.copy(opts)
    chunk_opts.niter = update_every

    oview = OffscreenTriMeshViewer(isheet, width=width, height=height, wireframe=wireframe)
    benchmark.reset()
    oview.recordStart(out, writeFirstFrame=True)
    try:
        last_report = None
        for _ in range(0, total_iters, update_every):
            last_report = inflation.inflation_newton(
                isheet,
                fixed_vars,
                chunk_opts,
                callback=None,
            )
            oview.update()
            if getattr(last_report, "success", False):
                break
        benchmark.report()
        return last_report
    finally:
        oview.recordStop()
