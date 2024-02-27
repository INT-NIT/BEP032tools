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


def main():
    root_directory = "/home/pourtoi/Bureau/Nouveau dossier/BEP"

    file_manager = ModalityAgnosticFile(root_directory)

    input_data = {
        "Name": "The mother of all experiments",
        "BIDSVersion": "1.6.0",
        "DatasetType": "raw",
        "License": "CC0",
        "Authors": ["Paul Broca", "Carl Wernicke"],
        "Acknowledgements": "Special thanks to Korbinian Brodmann for help in formatting this dataset in BIDS. We thank Alan Lloyd Hodgkin and Andrew Huxley for helpful comments and discussions about the experiment and manuscript; Hermann Ludwig Helmholtz for administrative support; and Claudius Galenus for providing data for the medial-to-lateral index analysis.",
        "HowToAcknowledge": "Please cite this paper: https://www.ncbi.nlm.nih.gov/pubmed/001012092119281",
        "Funding": ["National Institute of Neuroscience Grant F378236MFH1",
                    "National Institute of Neuroscience Grant 5RMZ0023106"],
        "EthicsApprovals": [
            "Army Human Research Protections Office (Protocol ARL-20098-10051, ARL 12-040, and ARL 12-041)"],
        "ReferencesAndLinks": ["https://www.ncbi.nlm.nih.gov/pubmed/001012092119281",
                               "Alzheimer A., & Kraepelin, E. (2015). Neural correlates of presenile dementia in humans. Journal of Neuroscientific Data, 2, 234001. doi:1920.8/jndata.2015.7"],
        "DatasetDOI": "doi:10.0.2.3/dfjj.10",
        "HEDVersion": "8.0.0",
        "GeneratedBy": [{
            "Name": "reproin",
            "Version": "0.6.0",
            "Container": {"Type": "docker", "Tag": "repronim/reproin:0.6.0"}
        }],
        "SourceDatasets": [{"URL": "s3://dicoms/studies/correlates", "Version": "April 11 2011"}]
    }

    file_manager.dataset_structure(input_data)
    file_manager.readme_change_licence()
    file_manager.citation_file()
    file_manager.participant_file()
    file_manager.sample_file()


if __name__ == "__main__":
    main()
