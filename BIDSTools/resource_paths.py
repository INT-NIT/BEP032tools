"""
resource_paths.py

Centralized definitions for paths to resources (YAML, JSON, CSV, etc.) used throughout BIDSTools.
Update these constants if you move or rename files in the 'ressources' directory.
"""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESSOURCES_DIR = os.path.join(BASE_DIR, 'ressources')

# YAML schemas
MODALITIES_YAML= os.path.join(RESSOURCES_DIR, 'schema', 'objects', 'modalities.yaml')
DATATYPES_YAML = os.path.join(RESSOURCES_DIR, 'schema', 'objects', 'datatypes.yaml')
ENTITIES_YAML = os.path.join(RESSOURCES_DIR, 'schema', 'objects', 'entities.yaml')
DIRECTORIES_YAML = os.path.join(RESSOURCES_DIR, 'schema', 'rules', 'directories.yaml')
FILES_YAML = os.path.join(RESSOURCES_DIR, 'schema', 'objects', 'files.yaml')
BIDS_VERSION = os.path.join(RESSOURCES_DIR, 'schema', 'BIDS_VERSION')
CORE_FILES_YAML = os.path.join(RESSOURCES_DIR, 'schema', 'rules', 'files', 'common', 'core.yaml')
TABLES_YAML = os.path.join(RESSOURCES_DIR, 'schema', 'rules', 'files', 'common', 'tables.yaml')