"""
Jac Kernel for Jupyter.

This module provides a Jupyter kernel for the Jac programming language. It allows you to execute Jac code
in Jupyter notebooks and captures and displays the output.

Version: 1.0.0
"""

import contextlib
import os.path as op
from io import StringIO

from ipykernel.kernelapp import IPKernelApp
from ipykernel.kernelbase import Kernel

from jackernel.importer import jac_blue_import as jac_import
from jackernel.syntax_hilighter import JacLexer

jac_lexer = JacLexer()


def exec_jac(code: str) -> str:
    """
    Compile, jac code, and execute and return the output.

    Parameters
    ----------
    code : str
        The jac code to execute.

    Returns
    -------
    str
        The output of the execution.
    """
    current_dir = op.dirname(op.abspath(__file__))
    try:
        jac_import(target=code, caller_dir=current_dir)

    except Exception as e:
        captured_output = "Exception: " + str(e)
        return captured_output

    script_file_path = op.join(current_dir, "__jac_gen__/session.py")
    try:
        with open(script_file_path, "r") as script_file:
            script_code = script_file.read()
            stdout_capture = StringIO()  # You need to import StringIO from io module

            with contextlib.redirect_stdout(stdout_capture):
                exec(script_code)

            captured_output = stdout_capture.getvalue()
    except Exception as e:
        captured_output = "Exception: " + str(e)
        return captured_output

    return captured_output


class JacKernel(Kernel):
    """Jac wrapper kernel."""

    implementation = "jac"
    implementation_version = "0.0"
    language = "python"  # For syntax hilighting
    language_version = "1.0"
    language_info = {
        "name": "python",
        "mimetype": "text/plain",
        "pygments_lexer": "jac_lexer",
        "file_extension": ".jac",
    }

    banner = "Jac kernel for Jupyter (main), version 1.0.0a4\n\n"

    def do_execute(
        self,
        code: str,
        silent: bool,
        store_history: bool = True,
        user_expressions: dict = None,
        allow_stdin: bool = False,
        stop_on_error: bool = False,
    ) -> dict:
        """Execute the code and return the result."""
        if not silent:
            try:
                output = exec_jac(code)
                self.send_response(
                    self.iopub_socket, "stream", {"name": "stdout", "text": output}
                )

            except Exception as e:
                self.send_response(
                    self.iopub_socket,
                    "error",
                    {
                        "ename": type(e).__name__,
                        "evalue": str(e),
                        "traceback": [],
                    },
                )

                return {
                    "status": "error",
                    "execution_count": self.execution_count,
                }

        return {
            "status": "ok",
            "execution_count": self.execution_count,
            "payload": [],
            "user_expressions": {},
        }


if __name__ == "__main__":
    IPKernelApp.launch_instance(kernel_class=JacKernel)
