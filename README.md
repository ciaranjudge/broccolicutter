# Broccolicutter

Opinionated data science cookiecutter that enforces good practices with conda, VSCode, Jupyter, and git.

Experimental fork of [cookiecutter-data-science](http://drivendata.github.io/cookiecutter-data-science/)


### To start a new project, run:
------------

    cookiecutter https://github.com/ciaranjudge/broccolicutter


# opinionated-data-science-setup

Sensible setup for doing data science stuff with python, conda, and Visual Studio Code

## A. User dektop setup

### 1. Set some useful environment variables

- Miniconda install location
- Easy way to say "cookiecutter [opinionated-cookiecutter]'
  - Cookiecutter config!
  - Create in repos folder (c:\repos)
  - Open VSCode once created

### 2. Conda user-level settings

- Are you in a corporate environment? If so, fix SSL issue in .condarc
- Make base conda environment read-only by setting 'conda-meta/history' to read-only
- Add *essential* extra packages to base env cookiecutter

### 3. Visual Studio Code user-level settings

- Terminal should launch base env
- base env is default python kernel?
  - Maybe no default is better option?
  - NB Jupyter is deliberately not included so can't do interactive window!

### 4. Visual Studio Code extensions

- Create extensions.yml file and then iterate over it using code --install
- Extensions working list
  - eamodio.gitlens
  - ms-python.python
  - ms-vscode-remote.vscode-remote-extensionpack
  - ms-vsts.team
  - redhat.vscode-yaml
  - 

- Other possible stuff
  - Font ligatures

## B. Project update stuff

### 1. Conda update

- Activate base environment

- Make base environment writeable using 'conda-meta/history'
- conda update conda
- Update --all from ".conda/base-environment.yml"
- Make base environment read-only

- If "envs/[project-env]" exists:
  - Remove read-only flag from "envs/[project-env]/conda-meta/history"
  - Update using environment.yml
- Else conda install from environment.yml
  - Export exact environment as environment-pinned.yml
  - Set read-only flag on "envs/[project-env]/conda-meta/history"

### Jupyter update

- Activate project environment

- If Jupyter environment exists:
  - Remove read-only flag (*what to use for flag?*)
  - clean
  - Update all from jupyter-env.yml (*whatever this is exactly?!*)
  - *Need to check for each extension if it's update or install that's needed?*
  - build
- Else install from jupyter-env.yml
  - *Maybe this branching isn't needed if extensions are just dealt with one-by-one?*

- *Where to install Jupyter environment?!*

### Visual Studio Code task(s)

- conda update
- Jupyter update

## D. Project cookiecutter stuff

### Misc

- Make sure a new git repo is automatically initiated when creating new project
- Add good default settings for things like matplotlib

### Conda environment

- Jupyter config and environment file locations
  - <https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#saving-environment-variables>

### Jupyter lab environment

<!-- - Want to think about  -->

### Visual Studio Code project-level settings

- Terminal should launch project conda env
- Project env is project python kernel
