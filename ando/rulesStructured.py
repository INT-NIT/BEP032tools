# construct the set of rules to be applied, level by level
rules_set = []
AUTHORIZED_DATA_EXTENSIONS = [f'({"|".join([".nix",".nwb"])})']
AUTHORIZED_METADATA_EXTENSIONS = [f'({"|".join([".tsv",".json"])})']
# level 0
currentdepth_rules={}
currentdepth_rules['authorized_folders'] = ['exp-([a-zA-Z0-9]+)']
currentdepth_rules['mandatory_folders'] = [['sub-([a-zA-Z0-9]+)']]
currentdepth_rules['authorized_data_files'] = []
currentdepth_rules['authorized_metadata_files'] = [
    ['participants',AUTHORIZED_METADATA_EXTENSIONS],
    ['dataset_descriptions',AUTHORIZED_METADATA_EXTENSIONS],
    ['tasks',AUTHORIZED_METADATA_EXTENSIONS] # To be discussed with respect to BEP
    ]
currentdepth_rules['mandatory_files'] = [
    ['participants', ['.tsv']],
    ['dataset_descriptions', ['.json']]
    ]
rules_set.append(currentdepth_rules)
# level 1
currentdepth_rules={}
currentdepth_rules['authorized_folders'] = ['sub-([a-zA-Z0-9]+)']
currentdepth_rules['mandatory_folders'] = [['ses-([a-zA-Z0-9]+)']]
currentdepth_rules['authorized_data_files'] = [['^$']]
currentdepth_rules['authorized_metadata_files'] = ['sessions']
currentdepth_rules['mandatory_files'] = []
rules_set.append(currentdepth_rules)
# level 2
currentdepth_rules={}
currentdepth_rules['authorized_folders'] = ['ses-([a-zA-Z0-9]+)']
currentdepth_rules['mandatory_folders'] = [['ephys']]
currentdepth_rules['authorized_data_files'] = [['^$']]
currentdepth_rules['authorized_metadata_files'] = [['^$']]
currentdepth_rules['mandatory_files'] = []
rules_set.append(currentdepth_rules)
# level 3
currentdepth_rules={}
currentdepth_rules['authorized_folders'] = ['ephys']
currentdepth_rules['mandatory_folders'] = []
currentdepth_rules['authorized_data_files'] = [['sub-([a-zA-Z0-9]+)_ses-([a-zA-Z0-9]+)([\\w\\-]*)_ephys',AUTHORIZED_DATA_EXTENSIONS]]
currentdepth_rules['authorized_metadata_files'] = [
    ['sub-([a-zA-Z0-9]+)_ses-([a-zA-Z0-9]+)([\\w\\-]*)_ephys',AUTHORIZED_METADATA_EXTENSIONS],
    ['sub-([a-zA-Z0-9]+)_ses-([a-zA-Z0-9]+)([\\w\\-]*)_channels',AUTHORIZED_METADATA_EXTENSIONS],
    ['sub-([a-zA-Z0-9]+)_ses-([a-zA-Z0-9]+)([\\w\\-]*)_contacts',AUTHORIZED_METADATA_EXTENSIONS],
    ['sub-([a-zA-Z0-9]+)_ses-([a-zA-Z0-9]+)([\\w\\-]*)_probes',AUTHORIZED_METADATA_EXTENSIONS],
    ['sub-([a-zA-Z0-9]+)_ses-([a-zA-Z0-9]+)([\\w\\-]*)_runs',AUTHORIZED_METADATA_EXTENSIONS]
    ]
currentdepth_rules['mandatory_files'] = [
    ['sub-([a-zA-Z0-9]+)_ses-([a-zA-Z0-9]+)([\\w\\-]*)_ephys', AUTHORIZED_METADATA_EXTENSIONS],
    ['sub-([a-zA-Z0-9]+)_ses-([a-zA-Z0-9]+)([\\w\\-]*)_ephys',['.json']],
    ['sub-([a-zA-Z0-9]+)_ses-([a-zA-Z0-9]+)([\\w\\-]*)_channels',['.tsv']],
    ['sub-([a-zA-Z0-9]+)_ses-([a-zA-Z0-9]+)([\\w\\-]*)_contacts',['.tsv']],
    ['sub-([a-zA-Z0-9]+)_ses-([a-zA-Z0-9]+)([\\w\\-]*)_probes',['.tsv']],
    ['sub-([a-zA-Z0-9]+)_ses-([a-zA-Z0-9]+)([\\w\\-]*)_runs',['.tsv']]
    ]
rules_set.append(currentdepth_rules)
