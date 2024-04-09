
import typing

from pydantic import BaseModel


def flatten_to_nested(data):
    """
    Flatten a dictionary to a nested dictionary based on the keys separated by dots.
    
    :param data: The dictionary to be flattened.
    :return: The nested dictionary.
    """
    nested = {}
    for flat_key, value in data.items():
        keys = flat_key.split('.')
        current = nested
        for key in keys[:-1]:  # Traverse/create keys except for the last one
            if key not in current:
                current[key] = {}
            current = current[key]
        current[keys[-1]] = value  # Set the final key to the value
    return nested

def nested_to_flatten(data: dict, parent_key: str = '', sep: str = '.') -> dict:
    """
    Recursively flattens a nested dictionary and prefixes keys based on their parent keys,
    using a separator to denote nesting levels.

    :param data: The nested dictionary to flatten.
    :param parent_key: The base key to use for prefixing child keys. Used for recursion.
    :param sep: The separator between parent and child keys in the flattened dictionary.
    :return: A flattened dictionary.
    """
    items = []
    for k, v in data.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(nested_to_flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def convert_to_flatten(data, model: typing.Type[BaseModel]) -> dict:
    """
    Converts nested data into a flattened structure based on a Pydantic model.

    :param data: The nested dictionary to convert.
    :param model: The Pydantic model class that the data should conform to.
    :return: A flattened dictionary representation of the nested data.
    """
    # TODO
    return nested_to_flatten(data)
