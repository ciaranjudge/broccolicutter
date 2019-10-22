import json
from pathlib import Path
import os

def update_json_settings(
    template_settings_path: Path = Path(".scripts/.user_config_templates/settings.json"),
    target_settings_path: Path = Path(os.environ["APPDATA"]) / "Code/User" / "settings.json"
):
    """Given a template and target settings path, 
    update the target with whatever settings are defined in the template.
    """
    # *Get the template settings that need to be included in user target settings
    with open(template_settings_path, 'r') as f:
        template_settings = json.load(f)
    
    # *Get the existing user settings
    with open(target_settings_path, "r") as f:
        target_settings = json.load(f)
    
    # *Update target settings with all keys and values in template settings
    for k, v in template_settings.items():
        target_settings[k] = v

    # *Write the updated settings to the user settings file
    with open(target_settings_path, "w") as f:
        json.dump(target_settings, f)

    # TODO Catch exceptions
    # TODO Return code based on success or failure

def update_vscode_user_settings(
    template_settings_path = Path(".scripts/.user_config_templates/vscode_user_settings_template.json"),
    target_settings_path = Path(os.environ["APPDATA"]) / "Code/User" / "settings.json"
):
    """Convenience wrapper for update_json_settings() with useful defaults for vscode settings
    """
    # TODO Return code based on success or failure
    update_json_settings(template_settings_path, target_settings_path)