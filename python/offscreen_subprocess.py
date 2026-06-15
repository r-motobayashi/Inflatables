import os
import pickle
import subprocess
import sys
import tempfile

import numpy as np


_NEWTON_OPTION_ATTRS = [
    "gradTol",
    "beta",
    "hessianScaledBeta",
    "niter",
    "useIdentityMetric",
    "useNegativeCurvatureDirection",
    "feasibilitySolve",
    "verbose",
    "verboseNonPosDef",
    "verboseWorkingSet",
    "stdoutFlushInterval",
    "nbacktrack_iter",
    "ngd_fallback_steps",
]


def record_concentric_circles(
    out="cc_inflate.mp4",
    circles=8,
    points=50,
    tri_area=0.001,
    pressure=20 * 3.75,
    niter=1000,
    width=768,
    height=640,
):
    here = os.path.dirname(os.path.abspath(__file__))
    script = os.path.join(here, "record_concentric_offscreen.py")
    cmd = [
        sys.executable,
        script,
        "--circles", str(circles),
        "--points", str(points),
        "--tri-area", str(tri_area),
        "--pressure", str(pressure),
        "--niter", str(niter),
        "--width", str(width),
        "--height", str(height),
        "--out", out,
    ]
    env = os.environ.copy()
    env.setdefault("MPLCONFIGDIR", "/private/tmp")
    proc = subprocess.run(cmd, cwd=here, env=env, text=True, capture_output=True)
    if proc.returncode != 0:
        raise RuntimeError(
            "Offscreen recording subprocess failed with exit code "
            f"{proc.returncode}\n\nSTDOUT:\n{proc.stdout}\n\nSTDERR:\n{proc.stderr}"
        )
    return proc.stdout


def record_inflation_state(
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
    Record an existing InflatableSheet in a child process.

    This keeps OffscreenRenderer out of the Jupyter kernel. If the macOS OpenGL
    renderer segfaults, only the child process dies and the notebook survives.
    """
    raise RuntimeError(
        "record_inflation_state is disabled because pickling InflatableSheet can "
        "segfault in this environment. Use record_mesh_inflation(mesh, "
        "fuse_markers, opts, ...) instead."
    )
    here = os.path.dirname(os.path.abspath(__file__))
    script = os.path.join(here, "record_inflation_state_offscreen.py")
    with tempfile.TemporaryDirectory(prefix="inflatables-offscreen-") as tmpdir:
        state_path = os.path.join(tmpdir, "state.pkl")
        with open(state_path, "wb") as f:
            pickle.dump(
                {
                    "isheet": isheet,
                    "fixed_vars": list(fixed_vars),
                    "opts": opts,
                    "out": out,
                    "width": width,
                    "height": height,
                    "wireframe": wireframe,
                    "update_every": update_every,
                },
                f,
                protocol=pickle.HIGHEST_PROTOCOL,
            )

        env = os.environ.copy()
        env.setdefault("MPLCONFIGDIR", "/private/tmp")
        proc = subprocess.run(
            [sys.executable, script, state_path],
            cwd=here,
            env=env,
            text=True,
            capture_output=True,
        )

    if proc.returncode != 0:
        raise RuntimeError(
            "Offscreen recording subprocess failed with exit code "
            f"{proc.returncode}\n\nSTDOUT:\n{proc.stdout}\n\nSTDERR:\n{proc.stderr}"
        )
    return proc.stdout


def record_mesh_inflation(
    mesh,
    fuse_markers,
    opts,
    out="cc_inflate.mp4",
    pressure=20 * 3.75,
    width=768,
    height=640,
    wireframe=True,
    update_every=1,
):
    """
    Record inflation for an existing mesh in a child process.

    Unlike record_inflation_state, this does not pickle InflatableSheet objects;
    it only transfers plain NumPy arrays and scalar options.
    """
    here = os.path.dirname(os.path.abspath(__file__))
    script = os.path.join(here, "record_mesh_inflation_offscreen.py")
    opt_values = {name: getattr(opts, name) for name in _NEWTON_OPTION_ATTRS}

    with tempfile.TemporaryDirectory(prefix="inflatables-offscreen-") as tmpdir:
        state_path = os.path.join(tmpdir, "state.npz")
        np.savez(
            state_path,
            vertices=np.asarray(mesh.vertices(), dtype=np.float64),
            triangles=np.asarray(mesh.triangles(), dtype=np.int32),
            fuse_markers=np.asarray(fuse_markers, dtype=np.bool_),
            opt_names=np.asarray(list(opt_values.keys()), dtype=object),
            opt_values=np.asarray(list(opt_values.values()), dtype=object),
            out=np.asarray(out, dtype=object),
            pressure=np.asarray(pressure, dtype=np.float64),
            width=np.asarray(width, dtype=np.int64),
            height=np.asarray(height, dtype=np.int64),
            wireframe=np.asarray(wireframe, dtype=np.bool_),
            update_every=np.asarray(update_every, dtype=np.int64),
        )

        env = os.environ.copy()
        env.setdefault("MPLCONFIGDIR", "/private/tmp")
        proc = subprocess.run(
            [sys.executable, script, state_path],
            cwd=here,
            env=env,
            text=True,
            capture_output=True,
        )

    if proc.returncode != 0:
        raise RuntimeError(
            "Offscreen recording subprocess failed with exit code "
            f"{proc.returncode}\n\nSTDOUT:\n{proc.stdout}\n\nSTDERR:\n{proc.stderr}"
        )
    return proc.stdout
