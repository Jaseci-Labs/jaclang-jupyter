"""Connect Decls and Defs in AST."""
import os

import jaclang.jac.absyntree as ast
from jaclang.jac.constant import Constants as Con
from jaclang.jac.passes.blue import PyOutPass


class CustomPyOutPass(PyOutPass):
    """Custom Python and bytecode file printing pass Developed for JAC kernel."""

    def get_output_targets(self, node: ast.Module) -> tuple[str, str, str]:
        """Get output targets."""
        gen_path = os.path.join(node.mod_path, Con.JAC_GEN_DIR)
        os.makedirs(gen_path, exist_ok=True)
        with open(os.path.join(gen_path, "__init__.py"), "w"):
            pass
        os.makedirs(gen_path, exist_ok=True)
        out_path_py = os.path.join(gen_path, "session.py")
        out_path_pyc = os.path.join(gen_path, "session.pyc")
        return node.mod_path, out_path_py, out_path_pyc
