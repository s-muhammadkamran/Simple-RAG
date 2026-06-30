from dotenv import load_dotenv
import json
import os

load_dotenv()

class EnvVarHelper:

    @classmethod
    def read_env_variable(cls, var_name, default=None, json_decode=False):
        value = os.getenv(var_name)
        if value is None and default is not None:
            return default
        elif value is None:
            raise ValueError(f"Environment variable '{var_name}' is not set and no default value was provided.")

        if json_decode:
            try:
                return json.loads(value)
            except json.JSONDecodeError as e:
                raise ValueError(f"Error decoding JSON for environment variable '{var_name}': {e}")
        
        return value