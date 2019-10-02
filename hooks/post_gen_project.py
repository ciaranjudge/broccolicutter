#%%
import os
from pathlib import Path
import subprocess
import json

# COOKIECUTTER_REPO_FOLDER = Path(".").resolve() 
# env = COOKIECUTTER_REPO_FOLDER / "environment.yml"
# print

#%%
CONDA_PREFIX = os.environ['CONDA_PREFIX']

## Need to check if exist and install only if not?
# jupyter lab clean
# jupyter labextension install @jupyter-widgets/jupyterlab-manager
# jupyter labextension install @jupyter-voila/jupyterlab-preview
# (jupytext not needed?)
# jupyter lab build







# # %%
# ## Install conda packages specified in central environment.yml into base environment
# environment_sourcepath = SOURCE_FOLDER / "environment.yml"
# commands = [
#     "conda update conda",
#     f"conda env update --file {environment_sourcepath}",
# ]
# for command in commands:
#     print(subprocess.run(command, shell=True))

# # %%
# ## Add default configuration for conda to user-level VSCode settings.json
# # Specify paths to relevant miniconda stuff
# miniconda_activate_script = MINICONDA_FOLDER / "Scripts\\activate.bat"
# miniconda_pythonpath = MINICONDA_FOLDER / "python.exe"
# # Write the needed VSCode settings as dictionary
# vscode_settings = {
#     "terminal.integrated.shellArgs.windows": [
#         "/K",
#         str(miniconda_activate_script),
#         str(MINICONDA_FOLDER),
#     ],
#     "python.pythonPath": str(miniconda_pythonpath),
# }
# # Create new VSCode settings file with vscode_settings as content
# # Write out Python dictionary as json
# vscode_settings_targetpath = VSCODE_SETTINGS_FOLDER / "settings.json"
# vscode_settings_json = json.dumps(vscode_settings)
# with open(vscode_settings_targetpath, "wt") as f:
#     f.write(vscode_settings_json)


# # # %%
# # ## Install Visual Studio Code extensions
# # # Sideloading by copying unpacked files from source to target folder
# # source_extensions_folder = SOURCE_FOLDER / "extensions"
# # copy_tree(str(source_extensions_folder), str(VSCODE_EXTENSIONS_FOLDER))

