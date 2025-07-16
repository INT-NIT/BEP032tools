"""
constants_fields.py

This module defines all field name constants used throughout the BIDSTools application.
Centralizing field names here ensures consistency and simplifies updates across the codebase.

Main Features:
- Defines constants for subject, session, modality, data type, and data path fields.
- Ensures consistency in field naming across all BIDSTools modules.
- Facilitates easy updates to field names as standards evolve.

Typical Usage:
    from BIDSTools.field_mapping import SUBJECT_ID, DATATYPE_EEG
    print(SUBJECT_ID)


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


# Data path (datafile_path) path where the data is stored
DATA_PATH = "datafile_path"
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
