import yaml

def read_yml(yml_file):
    with open(yml_file) as f:
        try:
            return yaml.load(f, Loader=yaml.FullLoader)
        except FileNotFoundError:
            print(f"Can't find file at {yml_file.resolve()}")
        except (yaml.YAMLError, yaml.MarkedYAMLError) as e:
            print("Something's wrong with the yaml in this file!")
            print(e)

# yml = read_yml("environment.yml")
# print(type(yml))
# print(yml['environment_variables']['jupyter_config_dir'])