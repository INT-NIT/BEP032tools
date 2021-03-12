# construct the set of rules to be applied, level by level
RULES_SET = []
DATA_EXTENSIONS = [".nix", ".nwb"]
METADATA_EXTENSIONS = [".tsv", ".json"]
ANY_DATA_EXT = [f'({"|".join(DATA_EXTENSIONS)})']
ANY_METADATA_EXT = [f'({"|".join(METADATA_EXTENSIONS)})']

# level 0
currentdepth_rules={}
currentdepth_rules['authorized_folders'] = ['sub-([a-zA-Z0-9]+)']
currentdepth_rules['mandatory_folders'] = [['sub-([a-zA-Z0-9]+)']]
currentdepth_rules['authorized_data_files'] = []
currentdepth_rules['authorized_metadata_files'] = [
    ['participants', ANY_METADATA_EXT],
    ['dataset_description', ANY_METADATA_EXT],
    ['tasks', ANY_METADATA_EXT]  # To be discussed with respect to BEP
    ]
currentdepth_rules['mandatory_files'] = [
    ['participants', ['.tsv']],
    ['dataset_description', ['.json']]
    ]
RULES_SET.append(currentdepth_rules)
# level 1
currentdepth_rules={}
currentdepth_rules['authorized_folders'] = ['ses-([a-zA-Z0-9]+)']
currentdepth_rules['mandatory_folders'] = [['ses-([a-zA-Z0-9]+)']]
currentdepth_rules['authorized_data_files'] = [['^$']]
currentdepth_rules['authorized_metadata_files'] = [['sessions', ANY_METADATA_EXT]]
currentdepth_rules['mandatory_files'] = []
RULES_SET.append(currentdepth_rules)
# level 2
currentdepth_rules={}
currentdepth_rules['authorized_folders'] = ['ephys']
currentdepth_rules['mandatory_folders'] = [['ephys']]
currentdepth_rules['authorized_data_files'] = [['^$']]
currentdepth_rules['authorized_metadata_files'] = [['^$']]
currentdepth_rules['mandatory_files'] = []
RULES_SET.append(currentdepth_rules)
# level 3
currentdepth_rules={}
currentdepth_rules['authorized_folders'] = ['^$']
currentdepth_rules['mandatory_folders'] = []
currentdepth_rules['authorized_data_files'] = [
    ['sub-([a-zA-Z0-9]+)_ses-([a-zA-Z0-9]+)([\\w\\-]*)_ephys', ANY_DATA_EXT]]
currentdepth_rules['authorized_metadata_files'] = [
    ['sub-([a-zA-Z0-9]+)_ses-([a-zA-Z0-9]+)([\\w\\-]*)_ephys', ANY_METADATA_EXT],
    ['sub-([a-zA-Z0-9]+)_ses-([a-zA-Z0-9]+)([\\w\\-]*)_channels', ANY_METADATA_EXT],
    ['sub-([a-zA-Z0-9]+)_ses-([a-zA-Z0-9]+)([\\w\\-]*)_contacts', ANY_METADATA_EXT],
    ['sub-([a-zA-Z0-9]+)_ses-([a-zA-Z0-9]+)([\\w\\-]*)_probes', ANY_METADATA_EXT],
    ['sub-([a-zA-Z0-9]+)_ses-([a-zA-Z0-9]+)([\\w\\-]*)_runs', ANY_METADATA_EXT]
    ]
currentdepth_rules['mandatory_files'] = [
    ['sub-([a-zA-Z0-9]+)_ses-([a-zA-Z0-9]+)([\\w\\-]*)_ephys', ANY_METADATA_EXT],
    ['sub-([a-zA-Z0-9]+)_ses-([a-zA-Z0-9]+)([\\w\\-]*)_ephys', ['.json']],
    ['sub-([a-zA-Z0-9]+)_ses-([a-zA-Z0-9]+)([\\w\\-]*)_channels', ['.tsv']],
    ['sub-([a-zA-Z0-9]+)_ses-([a-zA-Z0-9]+)([\\w\\-]*)_contacts', ['.tsv']],
    ['sub-([a-zA-Z0-9]+)_ses-([a-zA-Z0-9]+)([\\w\\-]*)_probes', ['.tsv']]
    ]
RULES_SET.append(currentdepth_rules)
