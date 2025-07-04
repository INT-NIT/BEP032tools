"""
This file defines all field names used in the application.

To modify a field name, simply change it here.
All code references should use these constants.
"""

# Subject fields
SUBJECT_ID = "participant_id"
SUBJECT_AGE = "age"
SUBJECT_SEX = "sex"
SUBJECT_GROUP = "group"
SUBJECT_HANDEDNESS = "handedness"

# Session fields
SESSION_ID = "session_id"
SESSION_DATE = "session_date"
SESSION_TASK = "task"
SESSION_RUN = "run"
MODALITY = "modality"
# Data type fields
DATATYPE_EEG = "eeg"
DATATYPE_MEG = "meg"
DATATYPE_MRI = "anat"
DATATYPE_FMRI = "func"
DATATYPE_BEH = "beh"
DATATYPE_MICR= "micr"

# BIDS specific fields
BIDS_VERSION = "BIDSVersion"
DATASET_NAME = "Name"
DATASET_DESCRIPTION = "DatasetDescription"
AUTHORS = "Authors"
DATASET_TYPE = "DatasetType"
LICENSE = "License"

# File naming
FILENAME_PATTERN = "{subject}_{session}_{task}_{run}_{suffix}.{extension}"
RAW_DATA_PATH ="datafile_path"
# Common fields
TASK_NAME = "task_name"
RUN_NUMBER = "run_number"
ACQ_TIME = "acq_time"

# Metadata fields
SAMPLE_FREQUENCY = "SamplingFrequency"
POWER_LINE_FREQUENCY = "PowerLineFrequency"
SOFTWARE_FILTERS = "SoftwareFilters"
DEVICE_SERIAL_NUMBER = "DeviceSerialNumber"

# EEG/MEG specific
EEG_REFERENCE = "EEGReference"
EEG_GROUND = "EEGGround"
EEG_PLACEMENT_SCHEME = "EEGPlacementScheme"
MEG_CHANNEL_COUNT = "MEGChannelCount"
EEG_CHANNEL_COUNT = "EEGChannelCount"
EOG_CHANNEL_COUNT = "EOGChannelCount"
ECG_CHANNEL_COUNT = "ECGChannelCount"
EMG_CHANNEL_COUNT = "EMGChannelCount"
MISC_CHANNEL_COUNT = "MiscChannelCount"
TRIGGER_CHANNEL_COUNT = "TriggerChannelCount"
RECORDING_DURATION = "RecordingDuration"
RECORDING_TYPE = "RecordingType"

# MRI specific
MAGNETIC_FIELD_STRENGTH = "MagneticFieldStrength"
MANUFACTURER = "Manufacturer"
MANUFACTURERS_MODEL_NAME = "ManufacturersModelName"
INSTITUTION_NAME = "InstitutionName"
INSTITUTION_ADDRESS = "InstitutionAddress"
DEVICE_SERIAL_NUMBER = "DeviceSerialNumber"
STATION_NAME = "StationName"
