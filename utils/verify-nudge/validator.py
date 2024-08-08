import re
from termcolor import colored

def validate_release_pattern(release):
    """
    Validates if the given release string follows the pattern 'rhoai-X.Y',
    where 'X' and 'Y' are positive integers.

    Args:
        release (str): The release string to validate.

    Returns:
        bool: True if the release string matches the pattern, False otherwise.
    """
    pattern = re.compile(r'^rhoai-\d+\.\d+$')
    return bool(pattern.match(release))
      
    
  
def __validate_field_type(config, field_name, expected_type, filename):
    if not isinstance(config[field_name], expected_type):
        raise TypeError(f"TypeError: Field '{field_name}' in '{config['name']}' should be a '{expected_type.__name__}', got '{type(config[field_name]).__name__}'.")



def validate_config_yaml(config):
    """
    Function to validate config.yaml file.
      - Ensure that the required fields (name, repo-url, and nudged-file-path) are present.
      - Validate the data types of all fields.

    Parameters:
      - config (dict): A dictionary representing a single configuration item in config.yaml.
      
    Returns:
      - bool: True if the validation is successful.

    Raises:
      - ValueError: If a required field is missing.
      - TypeError: If a field has an incorrect data type.
      
      The program will print an error message and exit with a status code of 1.
    """
    
    filename = 'config.yaml'
    required_fields = ['name', 'repo-url', 'nudged-file-path']
    optional_fields= ['onboarded-since', 'verify-components']
    
    try:
      for field in required_fields:
          if field not in config:
              raise ValueError(f"ValueError: Missing required field '{field}' in '{config['name']}'.")
          __validate_field_type(config, field, str, filename)

      for field in optional_fields:
          if field in config:
              if field == 'onboarded-since':
                  __validate_field_type(config, field, str, filename)
                  if not validate_release_pattern(config.get('onboarded-since')):
                    raise ValueError(f"ValueError: Invalid RHOAI release '{config.get('onboarded-since')}' specified in field '{field}'.")
              elif field == 'verify-components':
                  __validate_field_type(config, field, list, filename)
              
      return True
    except (ValueError, TypeError) as e:
        print(colored(f"Validation Failed for '{filename}'.", "light_red"))
        print()
        print(colored(e, "red"))
        exit(1)
          
    



def validate_releases_yaml(rhoai_releases):
    """
    Function to validate releases.yaml file.
      - Ensure that the required field (releases) is present.
      - Validate the data type of the 'releases' field.

    Parameters:
      - rhoai_releases (dict): A dictionary representing the configuration in releases.yaml.
      
    Returns:
      - bool: True if the validation is successful.

    Raises:
      - ValueError: If the required field is missing.
      - TypeError: If the 'releases' field has an incorrect data type.
      
      The program will print an error message and exit with a status code of 1.
    """
    
    filename = 'releases.yaml'
    required_field = 'releases'
    
    try:
      if required_field not in rhoai_releases:
          raise ValueError(f"ValueError: Missing required field '{required_field}'.")
        
      if not isinstance(rhoai_releases, dict):
          raise TypeError(f"TypeError: Field '{required_field}' should be a 'dict', got '{type(rhoai_releases[required_field]).__name__}'.")

      if not isinstance(rhoai_releases[required_field], list):
          raise TypeError(f"TypeError: Field '{required_field}' should be a 'list', got '{type(rhoai_releases[required_field]).__name__}'.")
      
      for release in rhoai_releases['releases']:
          if not validate_release_pattern(release):
            raise ValueError(f"ValueError: Invalid RHOAI release '{release}'.")
      
      return True
    except (ValueError, TypeError) as e:
        print(colored(f"Validation Failed for '{filename}'.", "light_red"))
        print()
        print(colored(e, "red"))
        exit(1)
    
  