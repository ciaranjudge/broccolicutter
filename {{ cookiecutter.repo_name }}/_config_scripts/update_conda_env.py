from pathlib import Path
import os
from stat import S_IREAD, S_IWRITE  # File permission flag settings
import subprocess  # Run shell commands (cross-platform)
import yaml

# TODO Limit frequency of base env update (weekly/daily/monthly)
def update_base_env(
    base_environment_yml: Path = Path.home() / ".conda" / "base-environment.yml",
    conda_prefix: Path = Path(os.environ["conda_prefix"]),
    enforce_readonly: bool = True,
) -> None: # TODO Return code based on success/failure
    """Update conda, and base environment if given base_environment_yml file.
    With no base_environment_yml, just update conda itself.
    Make base env temporarily writeable while updating,
    then make read-only again afterwards if enforce_readonly flag is set.
    """
    # *Envs should be read-only to enforce using environment.yml for specifying packages.
    # If "conda-meta/history" is read-only, conda knows the env is read-only.
    # (it's a "canary file" https://github.com/conda/conda/issues/4888#issuecomment-287201331)
    # TODO Exception if there is no conda-meta folder or file can't be created/made writeable
    base_canaryfile = conda_prefix / "conda-meta" / "history"
    # Need to create base_canaryfile if it doesn't exist - that's what Path.touch() is for!
    Path.touch(base_canaryfile)
    # Canaryfile 
    os.chmod(base_canaryfile, S_IWRITE)
    # Update conda itself, then update packages from base-environment.yml, then update --all
    # ?Is this overkill? Does conda env update from file also update all packages?
    print("Updating conda...")
    subprocess.run("conda update conda --yes")
    if base_environment_yml is not None:
        print(f"Updating base environment from {base_environment_yml.resolve()}")
        subprocess.run(f"conda env update --file {base_environment_yml.resolve()} --prune")
        subprocess.run("conda update --all --yes")
    if enforce_readonly:
        os.chmod(base_canaryfile, S_IREAD)


def update_env(
    environment_yml: Path = Path("environment.yml"),
    conda_prefix: Path = Path(os.environ["conda_prefix"]),
    enforce_readonly: bool = True,
) -> None: # TODO Return code based on success/failure
    """Given an environment.yml file that specifies a named conda env,
    update the env based on the yml file packages (or create the env if it doesn't exist).
    Make the env temporarily writeable while updating,
    then make it read-only again afterwards if enforce_readonly flag is set.
    """
    # *Get env name from supplied environment_yml file
    # TODO Raise exception if environment_yml name missing.
    # TODO Raise exception if no dependencies specified. This creates blank env and is bad!
    with open(environment_yml) as f:
        try:
            data = yaml.load(f, Loader=yaml.FullLoader)
            env_name = data["name"]
            print(f"Found environment file for {env_name} at {environment_yml.resolve()}")
        except FileNotFoundError:
            print(f"Can't find environment file at {environment_yml.resolve()}")
        except (yaml.YAMLError, yaml.MarkedYAMLError) as e:
            print("Something's wrong with the yaml in the environment file!")
            print(e)


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

    # Finally, make both the project env and base canaryfile read-only again.
    os.chmod(env_canaryfile, S_IREAD)
    os.chmod(base_canaryfile, S_IREAD)


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
        # TODO Make sure paths are output correctly for OS
        # Need generic per-OS paths
        # Effectively means paths relative to predefined OS environ vars

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

    # TODO Make everything read-only if flag set
    # TODO Make this whole thing neater!


# for var, val in os.environ.items():
#     print("Var: ", var, "Val: ", val)
# update_base_env()
# update_env()

env_vars = {"test_var": "val", "test_path": Path.cwd()}
set_env_vars(env_vars)
