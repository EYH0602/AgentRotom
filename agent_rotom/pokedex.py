import json
from pokebase.api import get_data
from pokebase.interface import name_id_convert
import fire


def remove_key_recursively(d, key_to_remove):
    if isinstance(d, dict):
        # remove the key if present
        d.pop(key_to_remove, None)

        for _, value in d.items():
            remove_key_recursively(value, key_to_remove)
    elif isinstance(d, list):
        # if the value is a list, iterate through its elements
        for item in d:
            remove_key_recursively(item, key_to_remove)


def get_pokemon_data(pokemon_name: str):
    _, pm_id = name_id_convert("pokemon", pokemon_name.lower())
    pm_data = get_data("pokemon", pm_id)
    remove_key_recursively(pm_data, "url")
    remove_key_recursively(pm_data, "version_group_details")  # to save context window
    pm_data.pop("sprites")
    return pm_data


def main(name: str = "Ceruledge"):
    pm_data = get_pokemon_data(name)
    print(json.dumps(pm_data))


if __name__ == "__main__":
    fire.Fire(main)
