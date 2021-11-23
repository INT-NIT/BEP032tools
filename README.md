# BEP032 tools

This repository collects tools supporting the BEP032 proposal. It emerged under the name `AnDO` (Animal Data Organization) and gathers a set of tools dedicated to the ongoing process of extending the BIDS standard ( https://bids-specification.readthedocs.io  ) so that it supports electrophysiological data recorded in animal models.  The proposed specifications are described in the following document: https://bids.neuroimaging.io/bep032 . This document is open to any type of feedback from the community and we are welcoming all types of constructive comments.

This project is composed of three main scrip :

-BEP032Validator script that check if your dataset follows BEP032 rules

-BEP032Generator script that create a dataset based on a CSV files

-BEP032Viewer script that displays your dataset directory in a convenient way. (deprecated)

[![PyPI license](https://img.shields.io/pypi/l/ansicolortags.svg)](https://pypi.python.org/pypi/ansicolortags/)[![Generic badge](https://travis-ci.org/INT-NIT/BidsValidatorA.svg?branch=master)](https://shields.io/)[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

[![gh actions tests](https://github.com/INT-NIT/BEP032tools/workflows/run-tests/badge.svg?branch=master)](https://github.com/INT-NIT/BEP032tools/actions)[![Test coverage](https://coveralls.io/repos/github/INT-NIT/BEP032tools/badge.svg?branch=master)](https://coveralls.io/github/INT-NIT/BEP032tools?branch=master)

## Installation

### Dependencies

BEP032Validator requires:

- Python (>= 3.6)
- Pip3

### User installation

To include all packages required for the BEP032 & AnDO tools download the repository from https://github.com/INT-NIT/AnDO and run the following in the unpacked version of the repository
```bash
>  pip install BEP032Validator
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

```bash
> python checker/BEP032Validator.py tests/dataset001/Landing
```

OR verbose usage

```bash
> python checker/BEP032Validator.py -v tests/dataset001/Landing

```
OR, in an equivalent manner, you can use the command line interface (CLI) provided with the package:

```bash
> BEP032Validator -v tests/dataset001/Landing

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

OR, in an equivalent manner, you can use the command line interface (CLI) provided with the package:

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

OR, in an equivalent manner, you can use the command line interface (CLI) provided with the package:

```bash
> BEP032Templater data.csv data/

```
-----------

### General usage for the viewer script (deprecated)

```term
usage: BEP032Viewer.py [-h] [-S] [-Se] [-Su] [-Ss] pathToDir

positional arguments:
  pathToDir             Path to the folder to show
  
optional arguments:
  -h, --help            show this help message and exit
  -S, --show            show dir structure
  -Se, --show_experiments show experiments folder only
  -Su, --show_subjects  show subjects folder only
  -Ss, --show_sessions  show sessions folder only
```


OR, in an equivalent manner, you can use the command line interface (CLI) provided with the package:

```bash
> BEP032Viewer data/

```

### Installation issues

In some cases pandas might not be properly installed via pip. In this case we recommend installing pandas via conda.

# Development

We welcome new contributors of all experience levels.  The
[Development Guide][] has detailed information about contributing code,
documentation, tests, and more. We've included some basic information in
this README.

Important links
---------------

-   Official source code repo: https://github.com/INT-NIT/BEP032tools
-   Download releases: https://pypi.org/project/BEP032tools/
-   Issue tracker:https://github.com/INT-NIT/BEP032tools/issues

-----------

You can check the latest sources with the command:

    git clone https://github.com/INT-NIT/BEP032tools.git
    
Contributing
------------

To learn more about making a contribution to BEP032Validator, please see
our [Contributing guide][].
