"""Contains code which can be configured to be called whenever zappa deploys code changes."""
import os

packages_to_remove = ["scipy", "numpy", "black", "rope"]


def pre_deploy():
    print("Removing dependencies which are too big for Lambda package\n")
    uninstall_deps()


def deployment_zip_created(_):
    print(f"Reinstalling dependencies after creating deployment zip\n")
    _reinstall_deps()


def uninstall_deps():
    python_path = get_python_path()
    cmd = f'{python_path}{" ".join([" -m", "pip", "uninstall", "-y"] + packages_to_remove)}'
    os.system(cmd)


def _reinstall_deps():
    python_path = get_python_path()
    cmd = f'{python_path}{" ".join([" -m", "pip", "install"] + packages_to_remove)}'
    os.system(cmd)


def get_python_path():
    python_path = os.path.join(os.environ["VIRTUAL_ENV"], "bin", "python")
    return python_path
