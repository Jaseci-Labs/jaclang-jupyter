"""Special Imports for Jac Code."""
import marshal
import traceback
import types
from os import path
from typing import Callable, Optional

from jaclang.jac.constant import Constants as Con
from jaclang.utils.helpers import handle_jac_error

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

    if cachable and path.exists(py_file_path):
        with open(py_file_path, "r") as f:
            code_string = f.read()
        with open(pyc_file_path, "rb") as f:
            codeobj = marshal.load(f)
    else:
        if transpiler_func(cell=target, caller_dir=caller_dir):
            return None
        with open(py_file_path, "r") as f:
            code_string = f.read()
        with open(pyc_file_path, "rb") as f:
            codeobj = marshal.load(f)

    module = types.ModuleType("session")
    module.__file__ = caller_dir
    module.__name__ = override_name if override_name else "session"
    module.__dict__["_jac_pycodestring_"] = code_string

    try:
        exec(codeobj, module.__dict__)
    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)
        err = handle_jac_error(code_string, e, tb)
        raise type(e)(str(e) + "\n" + err)

    return module


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
