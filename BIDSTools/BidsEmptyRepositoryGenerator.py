import sys
from BIDSTools.Createfile import CreatFile
from BIDSTools.Createdirectory import Createdirectory


class Generator:
    def __init__(self, output, sub_id=1, session_id=1, modality=None):
        """
        Initialize a Generator object.

        Args:
            output (str): The output folder path.
            sub_id (int): Subject ID.
            session_id (int): Session ID.
            modality (str, optional): The modality name.
        """
        self.output = output
        self.modality = modality.strip() if modality else None
        if self.modality:
            self.directory_builder = Createdirectory(output, sub_id, session_id, self.modality)
            self.file_builder = CreatFile(output)
            self.generate()
        else:
            print("No modality provided. Please specify a modality.")

    def generate(self):
        """Generate files and directories."""
        self.directory_builder.build()
        self.file_builder.build()


if __name__ == "__main__":
    pass
