# construct the set of rules to be applied, level by level
rules_set = []
DATA_EXTENSIONS = ['nix', 'nwb']
METADATA_EXTENSIONS = ['tsv', 'json']
# level 0
currentdepth_rules={}
currentdepth_rules['authorized_folders'] = ['exp-([a-zA-Z0-9]+)']
currentdepth_rules['authorized_data_files'] = []
currentdepth_rules['authorized_metadata_files'] = ['participants','dataset_description', 'tasks']
currentdepth_rules['mandatory_files'] = [['subject',['tsv']],['dataset_description',['json']]]
rules_set.append(currentdepth_rules)
# level 1
currentdepth_rules={}
currentdepth_rules['authorized_folders'] = ['sub-([a-zA-Z0-9]+)']
currentdepth_rules['authorized_data_files'] = []
currentdepth_rules['authorized_metadata_files'] = ['sessions']
currentdepth_rules['mandatory_files'] = []
rules_set.append(currentdepth_rules)
# level 2
currentdepth_rules={}
currentdepth_rules['authorized_folders'] = ['ses-([a-zA-Z0-9]+)']
currentdepth_rules['authorized_data_files'] = []
currentdepth_rules['authorized_metadata_files'] = []
currentdepth_rules['mandatory_files'] = []
rules_set.append(currentdepth_rules)
# level 3
currentdepth_rules={}
currentdepth_rules['authorized_folders'] = ['ephys']
currentdepth_rules['authorized_data_files'] = ['sub-([a-zA-Z0-9]+)_ses-([a-zA-Z0-9]+)([\w\\-]*)_ephys']
currentdepth_rules['authorized_metadata_files'] = [
    ['sub-([a-zA-Z0-9]+)_ses-([a-zA-Z0-9]+)([\w\\-]*)_ephys',['json']],
    ['sub-([a-zA-Z0-9]+)_ses-([a-zA-Z0-9]+)([\w\\-]*)_channels',['tsv']],
    ['sub-([a-zA-Z0-9]+)_ses-([a-zA-Z0-9]+)([\w\\-]*)_contacts',['tsv']],
    ['sub-([a-zA-Z0-9]+)_ses-([a-zA-Z0-9]+)([\w\\-]*)_probes',['tsv']],
    ['sub-([a-zA-Z0-9]+)_ses-([a-zA-Z0-9]+)([\w\\-]*)_runs',['tsv']]
    ]
currentdepth_rules['mandatory_files'] = [
    ['sub-([a-zA-Z0-9]+)_ses-([a-zA-Z0-9]+)([\w\\-]*)_ephys', ['nwb', 'nix']],
    ['sub-([a-zA-Z0-9]+)_ses-([a-zA-Z0-9]+)([\w\\-]*)_ephys',['json']],
    ['sub-([a-zA-Z0-9]+)_ses-([a-zA-Z0-9]+)([\w\\-]*)_channels',['tsv']],
    ['sub-([a-zA-Z0-9]+)_ses-([a-zA-Z0-9]+)([\w\\-]*)_contacts',['tsv']],
    ['sub-([a-zA-Z0-9]+)_ses-([a-zA-Z0-9]+)([\w\\-]*)_probes',['tsv']],
    ['sub-([a-zA-Z0-9]+)_ses-([a-zA-Z0-9]+)([\w\\-]*)_runs',['tsv']]
    ]
rules_set.append(currentdepth_rules)
