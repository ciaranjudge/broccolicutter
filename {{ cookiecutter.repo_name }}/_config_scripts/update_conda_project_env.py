# Standard library
from pathlib import Path
import os
from stat import S_IREAD, S_IWRITE  # File permission flag settings
import subprocess  # Run shell commands (cross-platform)

# Local packages
from read_yml import read_yml

def set_env_vars(
    env_vars: dict, 
    env_path: Path = Path(os.environ["conda_prefix"]),
    enforce_readonly: bool = True
):
    """Set environment variables for this conda environment.
    Based on "saving-environment-variables" section in 
    https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html
    Easiest to run this from the conda env that env vars are being set for!
    """
    activate_dir = env_path / "etc" / "conda" / "activate.d"
    activate_dir.mkdir(parents=True, exist_ok=True)
    Path.touch(activate_dir / "env_vars.sh") # Unix (Linux/Mac)
    Path.touch(activate_dir / "env_vars.bat") # Windows
    activate_sh = ["#!/bin/sh\n"] # Unix (Linux/Mac)
    activate_bat = [""] # Windows

    deactivate_dir = env_path / "etc" / "conda" / "deactivate.d"
    deactivate_dir.mkdir(parents=True, exist_ok=True)
    Path.touch(deactivate_dir / "env_vars.sh") # Unix (Linux/Mac)
    Path.touch(deactivate_dir / "env_vars.bat") # Windows
    deactivate_sh = ["#!/bin/sh\n"] # Unix (Linux/Mac)
    deactivate_bat = [""] # Windows

    for var, val in env_vars.items():
        # TODO Make sure paths are output correctly for OS, especially env vars ($ %%)
        # Need generic per-OS paths
        # Effectively means paths relative to predefined OS environ vars

        # TODO Make sure that any already set variables are kept when adding new ones!
        # Unix (Linux/Mac)
        activate_sh += f"export {var}={val}\n"
        deactivate_sh += f"unset {var}\n"

        # Windows
        activate_bat += f"set {var}={val}\n"
        deactivate_bat += f"set {var}=\n"

    with open(activate_dir / "env_vars.sh", 'w+') as f:
        f.writelines(activate_sh) 
    with open(activate_dir / "env_vars.bat", 'w+') as f:
        f.writelines(activate_bat)

    with open(deactivate_dir / "env_vars.sh", 'w+') as f:
        f.writelines(deactivate_sh) 
    with open(deactivate_dir / "env_vars.bat", 'w+') as f:
        f.writelines(deactivate_bat)   


def update_project_env(
    yml_file: Path = Path("environment.yml"),
    conda_prefix: Path = Path(os.environ["conda_prefix"]),
    enforce_readonly: bool = True,
) -> None: # TODO Return code based on success/failure (for command line use)
    """Given an environment.yml file that specifies a named conda env,
    update the env based on the yml file packages (or create the env if it doesn't exist).
    Make the env temporarily writeable while updating,
    then make it read-only again afterwards if enforce_readonly flag is set.
    """
    # *Get env name from yml_file
    # TODO Raise exception if yml_file name field missing.
    # TODO Raise exception if no dependencies specified. This creates blank env and is bad!
    # read_yml() is a convenience wrapper for yaml.load()
    # It catches FileNotFoundError, yaml.YAMLError, yaml.MarkedYAMLError
    environment_yml = read_yml(yml_file)
    env_name = environment_yml['name']
    print(f"Found environment file for {env_name} at {yml_file.resolve()}")

    # *Envs should be read-only to enforce using environment.yml for specifying packages.
    # If "conda-meta/history" is read-only, conda knows the env is read-only.
    # (it's a "canary file" https://github.com/conda/conda/issues/4888#issuecomment-287201331)
    # Need to make base canaryfile writeable first (otherwise new env installs itself elsewhere)
    # TODO Exception if there is no conda-meta folder or file can't be created/made writeable
    base_canaryfile = conda_prefix / "conda-meta" / "history"
    # ?Call update_base env if conda-meta/history doesn't exist?
    # Need to create base_canaryfile if it doesn't exist - that's what Path.touch() is for!
    Path.touch(base_canaryfile)
    os.chmod(base_canaryfile, S_IWRITE)

    # *Set up path to expected location of env, and check if it exists already
    env_path = conda_prefix / "envs" / env_name
    # TODO Directly check with "conda info --json", parsing env names with Path.name
    # TODO Enforce .condarc specified folder location for envs
    env_exists = env_path.exists()
    env_canaryfile = env_path / "conda-meta" / "history"


    if env_exists:
        # Project canaryfile also needs to be writeable if the environment exists already.
        os.chmod(env_canaryfile, S_IWRITE)
        subprocess.run("conda env update --file environment.yml --prune")
    else:
        print(f"Environment {env_name} doesn't exist, so create it...")
        subprocess.run("conda env create --file environment.yml")
        # Need to create a blank canaryfile ("conda-meta/history") in the new env
        # Path.touch(filename) creates a blank file if there isn't one already!
        Path.touch(env_canaryfile)

    # TODO Set environment variables (in environment.yml!) after env is updated.
    # TODO Suppress unhelpful "EnvironmentSectionNotValid" warning from conda

    # Finally, make both the project env and base canaryfile read-only again.
    os.chmod(env_canaryfile, S_IREAD)
    os.chmod(base_canaryfile, S_IREAD)




