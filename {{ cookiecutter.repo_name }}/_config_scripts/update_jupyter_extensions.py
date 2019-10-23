# Standard library
import os
from pathlib import Path
import subprocess

# Local packages
from read_yml import read_yml


def update_jupyter_extensions(yml_file: Path = Path("jupyter_extensions.yml")):
    # *Get env name from supplied yml_file
    # TODO Raise exception if yml_file name field missing.
    # read_yml() is a convenience wrapper for yaml.load()
    # It catches FileNotFoundError, yaml.YAMLError, yaml.MarkedYAMLError
    jupyter_extensions_yml = read_yml(yml_file)
    env_name = jupyter_extensions_yml['name']
    print(f"Found Jupyter extensions file for {env_name} at {yml_file.resolve()}")

    for extension in jupyter_extensions_yml['extensions']:
        subprocess.run(f"jupyter labextension install {extension}", shell=True)
    subprocess.run("jupyter lab build", shell=True)

