# AnDO-Project

The Animal Data Organization (AnDO) is a set of specifications for the organization of a directory containing experimental data recorded in animals. It is very inspired by the BIDS specifications ( https://bids-specification.readthedocs.io  ). The main difference lies in the fact that in experiments conducted with animals, it is very common to have different settings for different sessions, and more importantly for different animals (whereas research on human subjects tends to have exactly the same protocol used for all subjects, as looked after by the BIDS specifications).

This project is composed of three main scrip :

-AnDOChecker script that check if your dataset follows AnDO rules
-AnDOGenerator script that create a dataset based on a CSV files
-AnDOViewer script that display your dataset directory in a convenient way.

Futher information on Specs : https://bids.neuroimaging.io/bep032

[![PyPI license](https://img.shields.io/pypi/l/ansicolortags.svg)](https://pypi.python.org/pypi/ansicolortags/)[![Generic badge](https://travis-ci.org/INT-NIT/BidsValidatorA.svg?branch=master)](https://shields.io/)[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

[![gh actions tests](https://github.com/INT-NIT/AnDO/workflows/run-tests/badge.svg?branch=master)](https://github.com/INT-NIT/AnDO/actions)[![Test coverage](https://coveralls.io/repos/github/INT-NIT/AnDO/badge.svg?branch=master)](https://coveralls.io/github/INT-NIT/AnDO?branch=master)

## Installation

### Dependencies

AnDOChecker requires:

- Python (>= 3.6)
- Pip3

### User installation

```bash
>  pip install AnDOChecker
```

By installing AnDOChecker all three of the scripts will be installed

### General usage for the AnDOChecker script

```term
usage: AnDOChecker.py [-h] [-v] path

positional arguments:
  path           Path to your folder

optional arguments:  -h, --help     show this help message and exit
  -v, --verbose  increase output verbosity

```

### Specific usage

```bash
> python checker/AnDOChecker.py tests/dataset001/Landing
```

OR verbose usage

```bash
> python checker/AnDOChecker.py -v tests/dataset001/Landing

```
OR, in an equivalent manner, you can use the command line interface (CLI) provided with the package:

```bash
> AnDOChecker -v tests/dataset001/Landing

```

-----------
### General usage for the Generator script 

```term
usage: AnDOGenerator.py [-h] pathToCsv pathToDir

positional arguments:
  pathToCsv   Path to your folder
  pathToDir   Path to your csv file

optional arguments:
  -h, --help  show this help message and exit
```

OR, in an equivalent manner, you can use the command line interface (CLI) provided with the package:

```bash
> AnDOGenerator data.csv data/

```
-----------

### General usage for the viewer script

```term
usage: AnDOViewer.py [-h] [-S] [-Se] [-Su] [-Ss] pathToDir

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
> AnDOViewer data/

```

# Development

We welcome new contributors of all experience levels.  The
[Development Guide][] has detailed information about contributing code,
documentation, tests, and more. We've included some basic information in
this README.

Important links
---------------

-   Official source code repo: https://github.com/INT-NIT/AnDOChecker
-   Download releases: https://pypi.org/project/AnDOChecker/
-   Issue tracker:https://github.com/INT-NIT/AnDOChecker/issues

-----------

You can check the latest sources with the command:

    git clone https://github.com/INT-NIT/AnDOChecker.git
    
Contributing
------------

To learn more about making a contribution to AnDoChecker, please see
our [Contributing guide][].
