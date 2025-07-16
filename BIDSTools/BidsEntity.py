"""
BidsEntity.py

This module loads and manages entities defined by the BIDS (Brain Imaging Data Structure) standard.
It provides utilities to retrieve entity names and details .



"""
import yaml
from BIDSTools.resource_paths import ENTITIES_YAML

class Entity:
    def __init__(self):
        """
        Initialize an Entity object and load entities from a YAML file.
        """
        self.entities = self._load_entities()

    def _load_entities(self, yaml_path=ENTITIES_YAML):
        """
        Load entities from a YAML file.

        Args:
            yaml_path (str): The path to the YAML file containing entity data.

        Returns:
            dict: A dictionary containing entity data.
        """
        with open(yaml_path, 'r') as file:
            entities_data = yaml.safe_load(file)
        return entities_data

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
