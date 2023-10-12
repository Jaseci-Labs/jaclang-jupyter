"""Connect Decls and Defs in AST."""
import os

import jaclang.jac.absyntree as ast
from jaclang.jac.constant import Constants as Con
from jaclang.jac.passes.blue import PyOutPass


class CustomPyOutPass(PyOutPass):
    """Custom Python and bytecode file printing pass Developed for JAC kernel."""

    def enter_module(self, node: ast.Module) -> None:
        """Sub objects.

        name: str,
        doc: Token,
        body: Optional['Elements'],
        mod_path: str,
        rel_mod_path: str,
        is_imported: bool,
        sym_tab: Optional[SymbolTable],
        """
        if not (os.path.exists(node.mod_path) and node.meta.get("py_code")):
            return
        mods = [node] + self.get_all_sub_nodes(node, ast.Module)
        for mod in mods:
            mod_path, out_path_py, out_path_pyc = self.get_output_targets(mod)
            self.gen_python(mod, out_path=out_path_py)
            self.compile_bytecode(mod, mod_path=mod_path, out_path=out_path_pyc)
        self.terminate()

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
