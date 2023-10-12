"""Transpilation functions for Jupyter Cells."""
from typing import Type, TypeVar

from jackernel.pyoutpass import CustomPyOutPass
from jackernel.syntax_hilighter import JacLexer as Lexer
from jackernel.transform import Alert, Transform

import jaclang.jac.absyntree as ast
from jaclang.jac.parser import JacLexer, JacParser
from jaclang.jac.passes import Pass
from jaclang.jac.passes.blue import BluePygenPass
from jaclang.jac.passes.blue import pass_schedule

jac_lexer = Lexer()

T = TypeVar("T", bound=Pass)


def read_file(file_path: str) -> str:
    """
    Read the content of a file and return it as a string.

    Parameters
    ----------
    file_path : str
        The path to the file to read.

    Returns
    ----------
    str
        The content of the file.
    """
    try:
        with open(file_path, "r") as file:
            file_content = file.read()

    except FileNotFoundError:
        print(f"The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return file_content


def jac_cell_to_pass_tree(cell: str) -> Transform:
    """
    Convert a jac cell to an AST.

    Parameters
    ----------
    cell : str
        The jac cell to convert.

    Returns
    -------
    Transform
        The AST.
    """
    lex = JacLexer(mod_path="", input_ir=cell, base_path="")
    prse = JacParser(mod_path="", input_ir=lex.ir, base_path="", prior=lex)

    return prse


def jac_cell_to_pass(
    cell: str,
    caller_dir: str,
    target: Type[T] = BluePygenPass,
    schedule: str = pass_schedule,
) -> str:
    """
    Convert a jac cell to a python cell.

    Parameters
    ----------
    cell : str
        The jac cell to convert.
    caller_dir : str
        The directory of the caller.
    target : Type[T], optional
    The pass to convert to, by default BluePygenPass

    Returns
    -------
    str
        The python cell.
    """
    ast_ret = jac_cell_to_pass_tree(cell)

    for i in schedule:
        if i == target:
            break
        ast_ret = i(
            mod_path=caller_dir, input_ir=ast_ret.ir, base_path="", prior=ast_ret
        )

    ast_ret = target(
        mod_path=caller_dir, input_ir=ast_ret.ir, base_path="", prior=ast_ret
    )

    return ast_ret


def transpile_jac_blue(cell: str, caller_dir: str) -> list[Alert]:
    """Transpiler Jac file and return python code as string.

    Parameters
    ----------
    cell : str
        The jac cell to convert.

    Returns
    -------
    list[Alert]
        The list of alerts.
    """
    code = jac_cell_to_pass(
        cell=cell,
        caller_dir=caller_dir,
        target=BluePygenPass,
        schedule=pass_schedule,
    )
    if isinstance(code.ir, ast.Module) and not code.errors_had:
        print_pass = CustomPyOutPass(
            mod_path=caller_dir, input_ir=code.ir, base_path="", prior=code
        )
    else:
        return code.errors_had

    return print_pass.errors_had


def transpile_jac_purple(cell: str) -> list[Alert]:
    """Transpiler Jac file and return python code as string.

    Parameters
    ----------
    cell : str
        The jac cell to convert.

    Returns
    -------
    list[Alert]
        The list of alerts.
    """
    from jaclang.jac.passes.purple import pass_schedule, PurplePygenPass

    code = jac_cell_to_pass(
        cell=cell,
        target=PurplePygenPass,
        schedule=pass_schedule,
    )

    if isinstance(code.ir, ast.Module) and not code.errors_had:
        print_pass = CustomPyOutPass(
            mod_path="", input_ir=code.ir, base_path="", prior=code
        )
    else:
        return code.errors_had

    return print_pass.errors_had
