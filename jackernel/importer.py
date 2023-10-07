"""Special Imports for Jac Code."""
import types
from os import path
from typing import Callable, Optional

from jaclang.jac.constant import Constants as Con

from transpiler import read_file
from transpiler import transpile_jac_blue


def import_jac_module(
    transpiler_func: Callable,
    target: str,
    caller_dir: Optional[str] = None,
    cachable: bool = False,
    override_name: Optional[str] = None,
) -> Optional[types.ModuleType]:
    """Core Import Process."""
    gen_dir = path.join(caller_dir, Con.JAC_GEN_DIR)
    py_file_path = path.join(gen_dir, "session.py")
    pyc_file_path = path.join(gen_dir, "session.pyc")

    transpiler_func(cell=target, caller_dir=caller_dir)

    return py_file_path, pyc_file_path


def jac_blue_import(
    target: str,
    caller_dir: Optional[str] = None,
    cachable: bool = True,
    override_name: Optional[str] = None,
) -> Optional[types.ModuleType]:
    """Jac Blue Imports."""
    return import_jac_module(
        transpile_jac_blue, target, caller_dir, cachable, override_name
    )


# jac_blue_import("sample")
current_dir = path.dirname(path.abspath(__file__))
jac_blue_import(read_file("sample.jac"), current_dir)
