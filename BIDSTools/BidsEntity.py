"""
BidsEntity.py

This module loads and manages entities defined by the BIDS (Brain Imaging Data Structure) standard.
It provides utilities to retrieve entity names and details .



"""
import yaml
from BIDSTools.resource_paths import ENTITIES_YAML
from BIDSTools.helper import load_yaml_file

class Entity:
    def __init__(self):
        """
        Initialize an Entity object and load entities from a YAML file.
        """
        self.entities = load_yaml_file(ENTITIES_YAML)



    def get_entity_name(self, entity_name):
        """
        Get the name of a specific entity.

        Args:
            entity_name (str): The name of the entity to retrieve.

        Returns:
            str: The name of the entity, or None if the entity does not exist.
        """
        if entity_name in self.entities:
            return self.entities[entity_name].get("name")
        else:
            return None


def main():
    """
    Main function to demonstrate the usage of the Entity class.
    """
    entities = Entity()
    entity_name = "acquisition"  # Example entity name
    entity_name_output = entities.get_entity_name(entity_name)


if __name__ == "__main__":
    main()
