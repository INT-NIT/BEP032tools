data_description_json_template = {
  "Name": {
    "Description": "Name of the dataset.",
    "Requirement Level": "REQUIRED",
    "Data type": "string"
  },
  "BIDSVersion": {
    "Description": "The version of the BIDS standard that was used.",
    "Requirement Level": "REQUIRED",
    "Data type": "string"
  },
  "HEDVersion": {
    "Description": "If HED tags are used: The version of the HED schema used to validate HED tags for study. May include a single schema or a base schema and one or more library schema.",
    "Requirement Level": "RECOMMENDED",
    "Data type": "string or array of strings"
  },
  "DatasetLinks": {
    "Description": "Used to map a given <dataset-name> from a BIDS URI of the form bids:<dataset-name>:path/within/dataset to a local or remote location. The <dataset-name>: '' (an empty string) is a reserved keyword that MUST NOT be a key in DatasetLinks (example: bids::path/within/dataset).",
    "Requirement Level": "REQUIRED if BIDS URIs are used",
    "Data type": "object of strings"
  },
  "DatasetType": {
    "Description": "The interpretation of the dataset. For backwards compatibility, the default value is 'raw'. Must be one of: 'raw', 'derivative'.",
    "Requirement Level": "RECOMMENDED",
    "Data type": "string"
  },
  "License": {
    "Description": "The license for the dataset. The use of license name abbreviations is RECOMMENDED for specifying a license (see Licenses). The corresponding full license text MAY be specified in an additional LICENSE file.",
    "Requirement Level": "RECOMMENDED",
    "Data type": "string"
  },
  "Authors": {
    "Description": "List of individuals who contributed to the creation/curation of the dataset.",
    "Requirement Level": "RECOMMENDED",
    "Data type": "array of strings"
  },
  "Acknowledgements": {
    "Description": "Text acknowledging contributions of individuals or institutions beyond those listed in Authors or Funding.",
    "Requirement Level": "OPTIONAL",
    "Data type": "string"
  },
  "HowToAcknowledge": {
    "Description": "Text containing instructions on how researchers using this dataset should acknowledge the original authors. This field can also be used to define a publication that should be cited in publications that use the dataset.",
    "Requirement Level": "OPTIONAL",
    "Data type": "string"
  },
  "Funding": {
    "Description": "List of sources of funding (grant numbers).",
    "Requirement Level": "OPTIONAL",
    "Data type": "array of strings"
  },
  "EthicsApprovals": {
    "Description": "List of ethics committee approvals of the research protocols and/or protocol identifiers.",
    "Requirement Level": "OPTIONAL",
    "Data type": "array of strings"
  },
  "ReferencesAndLinks": {
    "Description": "List of references to publications that contain information on the dataset. A reference may be textual or a URI.",
    "Requirement Level": "OPTIONAL",
    "Data type": "array of strings"
  },
  "DatasetDOI": {
    "Description": "The Digital Object Identifier of the dataset (not the corresponding paper). DOIs SHOULD be expressed as a valid URI; bare DOIs such as 10.0.2.3/dfjj.10 are DEPRECATED.",
    "Requirement Level": "OPTIONAL",
    "Data type": "string"
  },
  "GeneratedBy": {
    "Description": "Used to specify provenance of the dataset.",
    "Requirement Level": "RECOMMENDED",
    "Data type": "array of objects"
  },
  "SourceDatasets": {
    "Description": "Used to specify the locations and relevant attributes of all source datasets. Valid keys in each object include 'URL', 'DOI' (see URI), and 'Version' with str",
    "Requirement Level": "RECOMMENDED",
    "Data type": "array of objects"
  }
}


participant_json_template = {
  "participant_id": {
    "Description": "A participant identifier of the form sub-<label>, matching a participant entity found in the dataset. There MUST be exactly one row for each participant. Values in participant_id MUST be unique. This column must appear first in the file.",
    "Requirement Level": "REQUIRED",
    "Data type": "string"
  },
  "species": {
    "Description": "The species column SHOULD be a binomial species name from the NCBI Taxonomy (for example, homo sapiens, mus musculus, rattus norvegicus). For backwards compatibility, if species is absent, the participant is assumed to be homo sapiens. This column may appear anywhere in the file.",
    "Requirement Level": "RECOMMENDED",
    "Data type": "string"
  },
  "age": {
    "Description": "Numeric value in years (float or integer value). It is RECOMMENDED to tag participant ages that are 89 or higher as 89+, for privacy purposes. This column may appear anywhere in the file.",
    "Requirement Level": "RECOMMENDED",
    "Data type": "number"
  },
  "sex": {
    "Description": "String value indicating phenotypical sex, one of 'male', 'female', 'other'. For a list of valid values, see the associated glossary entry. This column may appear anywhere in the file.",
    "Requirement Level": "RECOMMENDED",
    "Data type": "string"
  },
  "handedness": {
    "Description": "String value indicating one of 'left', 'right', 'ambidextrous'. For a list of valid values, see the associated glossary entry. This column may appear anywhere in the file.",
    "Requirement Level": "RECOMMENDED",
    "Data type": "string"
  },
  "strain": {
    "Description": "For species different from homo sapiens, string value indicating the strain of the species, for example: C57BL/6J. This column may appear anywhere in the file.",
    "Requirement Level": "RECOMMENDED",
    "Data type": "string"
  },
  "strain_rrid": {
    "Description": "For species different from homo sapiens, research resource identifier (RRID) of the strain of the species, for example: RRID:IMSR_JAX:000664. This column may appear anywhere in the file.",
    "Requirement Level": "RECOMMENDED",
    "Data type": "string"
  },
  "Additional Columns": {
    "Description": "",
    "Requirement Level": "",
    "Data type": ""
  }
}
