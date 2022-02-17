# BEP032 tools

This repository collects tools supporting the [BEP032 proposal](https://bids.neuroimaging.io/bep032). It originally emerged under the name `AnDO` (Animal Data Organization) and gathers a set of tools facilitating the usage of the proposed structure. For the documentation of BIDS itself, see https://bids-specification.readthedocs.io. The proposal is open to any type of feedback from the community and we are welcoming all types of constructive comments.

The provided tools integrating with BEP032 are :

- BEP032Validator script to check if your dataset follows the current BEP032 rules

- BEP032Generator script to create a BEP032 compatible structure for a given set of data files. These files need to be listed in an input CSV file.

- BEP032Templater script to generate a dummy set of BEP032 compatible files to be extended manually, e.g. using Excel or a text editor

- _BEP032Viewer script to display your dataset directory in a convenient way. (deprecated)_

[![PyPI license](https://img.shields.io/pypi/l/ansicolortags.svg)](https://pypi.python.org/pypi/ansicolortags/)[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)[![gh actions tests](https://github.com/INT-NIT/BEP032tools/actions/workflows/run_tests.yml/badge.svg?branch=master)](https://github.com/INT-NIT/BEP032tools/actions)[![Test coverage](https://coveralls.io/repos/github/INT-NIT/BEP032tools/badge.svg?branch=master)](https://coveralls.io/github/INT-NIT/BEP032tools?branch=master)

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
