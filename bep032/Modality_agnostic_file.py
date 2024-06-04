import json
import os


class ModalityAgnosticFile:
    def __init__(self, output_path):
        self.output_path = output_path

    def create_empty_file(self, filename):
        file_path = os.path.join(self.output_path, filename)
        with open(file_path, 'w'):
            pass

    def write_json_to_file(self, filename, data):
        file_path = os.path.join(self.output_path, filename)
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
        self.create_file('samples.json')

    def dataset_description(self):
        self.create_file('dataset_description.json')

    def creat_all_files(self):
        self.readme_change_licence()
        self.participant_file()
        self.sample_file()
        self.citation_file()
        self.dataset_description()
