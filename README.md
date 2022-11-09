# BEP032 tools

This repository collects tools supporting the [BEP032 proposal](https://bids.neuroimaging.io/bep032). It originally emerged under the name `AnDO` (Animal Data Organization) and gathers a set of tools facilitating the usage of the proposed structure. For the documentation of BIDS itself, see https://bids-specification.readthedocs.io. The proposal is open to any type of feedback from the community and we are welcoming all types of constructive comments.

The provided tools integrating with BEP032 are :

- BEP032Validator script to check if your dataset follows the current BEP032 rules

- BEP032Generator script to create a BEP032 compatible folder structure **without** metadata files for a given set of subjects and sessions. These files need to be listed in an input CSV file.

- BEP032Templater script to generate a BEP032 compatible folder structure **including** dummy files to be extended manually, e.g. using Excel or a text editor

- _BEP032Viewer script to display your dataset directory in a convenient way. (deprecated)_

[![PyPI license](https://img.shields.io/pypi/l/ansicolortags.svg)](https://pypi.python.org/pypi/ansicolortags/)[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)[![gh actions tests](https://github.com/INT-NIT/BEP032tools/actions/workflows/run_tests.yml/badge.svg?branch=master)](https://github.com/INT-NIT/BEP032tools/actions)[![Test coverage](https://coveralls.io/repos/github/INT-NIT/BEP032tools/badge.svg?branch=master)](https://coveralls.io/github/INT-NIT/BEP032tools?branch=master)


The official documentation is hosted on [ReadTheDocs](https://bep032tools.readthedocs.io).

## Installation

### Dependencies

BEP032Validator requires:

- Python (>= 3.7)
- Pip3

### User installation

To include all packages required for the BEP032 tools download the repository from https://github.com/INT-NIT/BEP032tools and run the following in the unpacked version of the repository
```bash
>  pip install BEP032tools[tools]
```

By installing BEP032Validator the following scripts will be installed:

### General usage for the BEP032Validator script

```term
usage: BEP032Validator.py [-h] [-v] path

positional arguments:
  path           Path to your folder

optional arguments:  -h, --help     show this help message and exit
  -v, --verbose  increase output verbosity

```

### Specific usage

The validator can be directly used from the command line interface (CLI)

```bash
> BEP032Validator -v tests/dataset001/Landing

```

or from within Python

```python
> from bep032tools.validator import BEP032Validator
> BEP032Validator.is_valid('tests/dataset001/Landing')
```



-----------
### General usage for the Generator script 

The generator can be used to create a BEP032 compatible folder structure (**without metadata files**) based on a list of sessions and subject. This list of sessions and subject has to be provided in form of a CSV file:

```term
usage: BEP032Generator.py [-h] pathToCsv pathToDir

positional arguments:
  pathToCsv   Path to your folder
  pathToDir   Path to your csv file

optional arguments:
  -h, --help  show this help message and exit
```

The generator can be directly used from the command line interface (CLI)

```bash
> BEP032Generator data.csv data/

```


-----------

### General usage for the Templater script 

```term
usage: BEP032Temlater.py [-h] pathToCsv pathToDir

positional arguments:
  pathToCsv   Path to your folder
  pathToDir   Path to your csv file

optional arguments:
  -h, --help  show this help message and exit
```

The templater can be directly used from the command line interface (CLI)

```bash
> BEP032Templater data.csv data/

```

## How to create a BEP032 structure **including** custom metadata

There are two options to add custom metadata (files) to a BEP032 structure

1) Generation of the structure including dummy metadata files using the `BEP032Templator` and manual entry of the metadata in those files.
2) Programmatic extension of the `BEP032Generator`. For this you need to create a Python class that inherits from `bep032tools.generator.BE032Generator` and implements the missing metadata methods:
    - `generate_metadata_file_sessions`
    - `generate_metadata_file_tasks`
    - `generate_metadata_file_dataset_description`
    - `generate_metadata_file_participants`
    - `generate_metadata_file_probes`
    - `generate_metadata_file_probes`
    - `generate_metadata_file_channels`
    - `generate_metadata_file_contacts`
    - `generate_metadata_file_scans`
    
  These methods should fetch the corresponding metadata information from your project specific location and create the corresponding CSV or JSON file using the `generator.utils.save_json` and `generator.utils.save_tsv` functions correspondingly. When all missing methods are implemented `generator.BEP032Generator.generate_struct()` will not only create the corresponding folder structure, but also all metadata files with the metadata provided.

### Installation issues

In some cases pandas might not be properly installed via pip. In this case we recommend installing pandas via conda.

# Development

We welcome new contributors of all experience levels.

Important links
---------------

- Official source code repo: https://github.com/INT-NIT/BEP032tools
- (In planning) Download releases: https://pypi.org/project/BEP032tools/
- Issue tracker:https://github.com/INT-NIT/BEP032tools/issues

    
Contributing
------------

To contribute to the development of BEP032tools, please open an [issue](https://github.com/INT-NIT/BEP032tools/issues) or [pull request](https://github.com/INT-NIT/BEP032tools/pulls) or directly comment in the [BEP032 proposal](https://bids.neuroimaging.io/bep032).
