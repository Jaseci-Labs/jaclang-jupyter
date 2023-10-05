"""
Jac Kernel for Jupyter.

This module provides a installation commands for the jupyter kernel developed for the Jac programming language.
Version: 1.0.0
"""

import argparse
import json
import os
import sys

from IPython.utils.tempdir import TemporaryDirectory

from jupyter_client.kernelspec import KernelSpecManager


kernel_json = {
    "argv": ["python", "-m", "jackernel.kernel", "-f", "{connection_file}"],
    "display_name": "Jac",
    "language_info": {
        "name": "python",
        "mimetype": "text/plain",
        "pygments_lexer": "jac_lexer",
        "file_extension": ".jac",
    },
}


def install_my_kernel_spec(user: bool = True, prefix: str = None) -> None:
    """
    Install the Jac kernel spec.

    Parameters
    ----------
    user : bool
    Whether to do a user install
    prefix : str
    Specify prefix to install to, e.g. an env

    Returns
    -------
    A KernelSpecManager instance.
    """
    with TemporaryDirectory() as td:
        os.chmod(td, 0o755)  # Starts off as 700, not user readable
        with open(os.path.join(td, "kernel.json"), "w") as f:
            json.dump(kernel_json, f, sort_keys=True)
        # shutil.copyfile(_ICON_PATH, pathlib.Path(td) / _ICON_PATH.name)
        KernelSpecManager().install_kernel_spec(td, "Jac", user=user, prefix=prefix)


def _is_root() -> bool:
    """
    Check if the user is root.

    Returns
    -------
    bool
    """
    try:
        return os.geteuid() == 0
    except AttributeError:
        return False  # assume not an admin on non-Unix platforms


def main(argv: list = None) -> None:
    """
    Entry point for the jac kernel install.

    Parameters
    ----------
    argv : list
        If called from the command line, arguments to be processed. If not
        given, sys.argv is used.
    """
    parser = argparse.ArgumentParser(description="Install KernelSpec for Jac Kernel")
    prefix_locations = parser.add_mutually_exclusive_group()

    prefix_locations.add_argument(
        "--user",
        help="Install KernelSpec in user's home directory",
        action="store_true",
    )
    prefix_locations.add_argument(
        "--sys-prefix",
        help="Install KernelSpec in sys.prefix. Useful in conda / virtualenv",
        action="store_true",
        dest="sys_prefix",
    )
    prefix_locations.add_argument(
        "--prefix", help="Install KernelSpec in this prefix", default=None
    )

    args = parser.parse_args(argv)

    user = False
    prefix = None
    if args.sys_prefix:
        prefix = sys.prefix
    elif args.prefix:
        prefix = args.prefix
    elif args.user or not _is_root():
        user = True

    install_my_kernel_spec(user=user, prefix=prefix)


if __name__ == "__main__":
    main()
    print("Installed jaclang kernel spec")
