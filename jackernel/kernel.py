"""
Jac Kernel for Jupyter.

This module provides a Jupyter kernel for the Jac programming language. It allows you to execute Jac code
in Jupyter notebooks and captures and displays the output.

Version: 1.0.0
"""

import contextlib
import os.path as op
import tempfile
from io import StringIO

from ipykernel.kernelapp import IPKernelApp
from ipykernel.kernelbase import Kernel

from jackernel.syntax_hilighter import JacLexer

from jaclang import jac_blue_import as jac_import

jac_lexer = JacLexer()


def exec_jac(code: str) -> str:
    """Compile, jac code, and execute and return the output."""
    with tempfile.TemporaryDirectory() as tmpdir:
        source_path = op.join(tmpdir, "temp.jac")

        # Write the code to the jac file.
        with open(source_path, "w") as f:
            f.write(code)

        try:
            jac_import(target=op.join(tmpdir, "temp"), base_path=tmpdir)
            # Import the jac file, this generates the __jac_gen__ folder at the same level as the jac file,
            # This folder contains the python file that we want to execute.
            script_path = op.join(tmpdir, "__jac_gen__/temp.py")

            with open(script_path, "r") as script_file:
                script_code = script_file.read()
                stdout_capture = (
                    StringIO()
                )  # You need to import StringIO from io module

                with contextlib.redirect_stdout(stdout_capture):
                    exec(script_code)

                captured_output = stdout_capture.getvalue()

        except Exception as e:
            captured_output = "Exception: " + str(e)
            return captured_output

        finally:
            pass

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
                stream_content = {"name": "stdout", "text": output}
                self.send_response(self.iopub_socket, "stream", stream_content)

            except Exception as e:
                error_content = {
                    "ename": type(e).__name__,
                    "evalue": str(e),
                    "traceback": [],
                }
                self.send_response(self.iopub_socket, "error", error_content)

                return {
                    "status": "error",
                    "execution_count": self.execution_count,
                }

            finally:
                pass

        execution_result = {
            "status": "ok",
            "execution_count": self.execution_count,
            "payload": [],
            "user_expressions": {},
        }
        return execution_result


if __name__ == "__main__":
    IPKernelApp.launch_instance(kernel_class=JacKernel)
