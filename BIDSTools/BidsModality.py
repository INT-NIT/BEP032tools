import yaml
import os


class Modality:
    def __init__(self, relative_path=None):
        """
        Initialize a Modality object with a path to a YAML file containing modalities.

        Args:
            relative_path (str, optional): Path to the YAML file containing modalities.
                If not provided, uses the default path in the resources directory.
        """
        if relative_path is None:
            # Get the directory where the current script is located
            script_dir = os.path.dirname(os.path.abspath(__file__))
            # Construct the absolute path to modalities.yaml
            relative_path = os.path.join(script_dir, "ressources", "schema", "objects", "modalities.yaml")
        
        self.relative_path = relative_path
        self.modalities = []
        self.modality_details = {}

        with open(relative_path, "r") as file:
            modalities_yaml = yaml.safe_load(file)
            if modalities_yaml:
               self.modalities = [p['display_name'].upper() for p in modalities_yaml.values()]

               self.modality_details = {p['display_name'].upper(): k for k, p in modalities_yaml.items()}

def main():
    """
    Main function to demonstrate the usage of the Modality class.
    """
    modality = Modality()


if __name__ == "__main__":
    main()
