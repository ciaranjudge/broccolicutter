# This is the example 'validating template variables' script from 
# https://cookiecutter.readthedocs.io/en/latest/advanced/hooks.html

import re
import sys
# from pathlib import Path
# import json


MODULE_REGEX = r'^[_a-zA-Z][_a-zA-Z0-9]+$'

module_name = '{{ cookiecutter.repo_name }}'

if not re.match(MODULE_REGEX, module_name):
    print('ERROR: %s is not a valid Python module name!' % module_name)

    # exits with status 1 to indicate failure
    sys.exit(1)

# TODO Check user-level settings for conda and VSCode, and update if needed
# Should fail if can't do update
