import json
import os


class ModalityAgnosticFile:
    def __init__(self, root_to_save):
        self.root_to_save = root_to_save

    def create_empty_file(self, filename):
        file_path = os.path.join(self.root_to_save, filename)
        with open(file_path, 'w'):
            pass

    def write_json_to_file(self, filename, data):
        file_path = os.path.join(self.root_to_save, filename)
        with open(file_path, 'w') as file:
            json.dump(data, file)

    def dataset_structure(self, input_data):
        self.write_json_to_file('dataset_description.json', input_data)

    def readme_change_licence(self):
        for filename in ['README', 'CHANGES', 'LICENSES']:
            self.create_empty_file(filename)

    def create_file(self, filename):
        self.create_empty_file(filename)

    def citation_file(self):
        self.create_file('CITATION.cff')

    def participant_file(self):
        self.create_file('participants.tsv')
        self.create_file('participants.json')

    def sample_file(self):
        self.create_file('sample.tsv')
        self.create_file('sample.json')


