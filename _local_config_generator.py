import os


def get_var(key: str, default=None) -> str:
    """
    Function for getting variable value from environment.
    :param key: str
        variable name.
    :param default
        default value
    :return: str
        variable value.
    """
    result = os.environ.get(key)

    if result is None:
        if default:
            return default
        raise Exception(f'In your environment no {key} find.')
    else:
        return result


def print_template():
    """
    function for printing template to the local_config.py file
    :return: None
    """
    with open("./backend/local_config.py", 'w') as f:
        f.write(f"""
import os


class Development(object):
    \"\"\"
    Development environment configuration
    \"\"\"
    DEBUG = {get_var("DEBUG_DEV",'True')}
    TESTING = {get_var("TESTING_DEV", 'False')}
    MONGO_URI = "{get_var("MONGO_URI_DEV")}"


class Production(object):
    \"\"\"
    Production environment configurations
    \"\"\"
    DEBUG = {get_var("DEBUG_PROD", 'False')}
    TESTING = {get_var("TESTING_PROD", 'False')}
    MONGO_URI = "{get_var("MONGO_URI_PROD")}"
""")


if __name__ == "__main__":
    print_template()
