import os
from pathlib import Path


class BEP032:
    """Generates the directory structure for a subject's session data.

    Directory Structure:
    - sub_id
      - sess_id
        - modality

    Parameters
    ----------
    sub_id : str
        Subject identifier, e.g., '0012' or 'j.s.smith'
    sess_id : str
        Session identifier, e.g., '20210101' or '007'
    modality : str
        Modality identifier, e.g., 'ephys'
    """

    def __init__(self, sub_id, sess_id, modality, tasks):
        self.sub_id = sub_id
        self.sess_id = sess_id
        self.modality = modality
        self.tasks = tasks

    def create_directory_structure_by_experience(self, output_path):
        subject_dir = output_path / f'sub_{self.sub_id}'
        session_dir = subject_dir / f'ses_{self.sess_id}'

        if not os.path.exists(subject_dir):
            os.makedirs(subject_dir)

        if not os.path.exists(session_dir):
            os.makedirs(session_dir)

        if not os.path.exists(session_dir / self.modality):
            os.makedirs(session_dir / self.modality)

    def create_files_in_directory(self, output_path):
        subject_dir = output_path / f'sub_{self.sub_id}'
        self.create_directory_structure_by_experience(output_path)
        """creat file within subject_dir and ephys_dir"""

        file_path_json  = os.path.join(subject_dir, f'sub_{self.sub_id}_sessions.json')
        file_path_tsv  = os.path.join(subject_dir, f'sub_{self.sub_id}_sessions.tsv')
        with open (file_path_json, 'w'):
            pass
        with open(file_path_tsv, 'w'):
            pass
        session_dir = subject_dir / f'ses_{self.sess_id}'

        if os.path.exists(session_dir / self.modality):
            modality_dir = session_dir / self.modality
            for task in self.tasks:
                file_path_tsv= os.path.join(modality_dir,f'sub_{self.sub_id}_ses_{self.sess_id}_task_{task}.tsv')
                with open(file_path_tsv, 'w'):
                    pass





    @staticmethod
    def test():
        sub_id = 'fata1'
        sess_id = '1'
        modality = 'ephys'
        output_path = Path('/home/pourtoi/Bureau/Nouveau dossier/BEP')
        bep032_instance = BEP032(sub_id, sess_id, modality, tasks='1')
        bep032_instance.create_files_in_directory(output_path)


if __name__ == '__main__':
    BEP032.test()
