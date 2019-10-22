from pathlib import Path
import os
from stat import S_IREAD, S_IWRITE  # File permission flag settings
import subprocess  # Run shell commands (cross-platform)

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
