# AnDOChecker

The Animal Data Organization (AnDO) is a set of specifications for the organization of a directory containing experimental data recorded in animals. It is very inspired by the BIDS specifications ( https://bids-specification.readthedocs.io ). The main difference lies in the fact that in experiments conducted with animals, it is very common to have different settings for different sessions, and more importantly for different animals (whereas research on human subjects tends to have exactly the same protocol used for all subjects, as looked after by the BIDS specifications).

Futher information on Specs : https://int-nit.github.io/AnDOChecker/

[![PyPI license](https://img.shields.io/pypi/l/ansicolortags.svg)](https://pypi.python.org/pypi/ansicolortags/)[![Generic badge](https://travis-ci.org/Slowblitz/BidsValidatorA.svg?branch=master)](https://shields.io/)[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

## Installation
### Dependencies

AnDOChecker requires:

- Python (>= 3.6)
- Pip3

### User installation
```bash
> pip install AnDOchecker
```

## General usage

```term
usage: AnDOChecker.py [-h] [-v] path

positional arguments:
  path           Path to your folder

optional arguments:  -h, --help     show this help message and exit
  -v, --verbose  increase output verbosity

```

## Specific usage

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
# AnDOtools

AnDOtools is a little project that contain two scripts :
- a script to help users generate an AnDO structure based on a csv file 
(You can find in the Creator folder one exemple of a CSV file names "exemple.csv")
- a script to help users to dispay an AnDO structure


## Installation

Those tools will be installed with the AnDOChecker installation
### Dependencies

AnDOChecker requires:

- Python (>= 3.6)
- Pip3
- tree

### General usage for the creator script 

```term
usage: AnDOGenerator.py [-h] pathToCsv pathToDir

positional arguments:
  pathToCsv   Path to your folder
  pathToDir   Path to your csv file

optional arguments:
  -h, --help  show this help message and exit
```


### General usage for the veiwer script 

```term
usage: AnDOViewer.py [-h] [-S] [-Se] [-Su] [-Ss] pathToDir

positional arguments:
  pathToDir             Path to the folder to show
  
optional arguments:
  -h, --help            show this help message and exit
  -S, --show            show dir structure
  -Se, --show_experiments show experiments folder only
  -Su, --show_subjects  show subjects folder only
  -Ss, --show_sessions  show sessions folder onlyt
```

OR, in an equivalent manner, you can use the command line interface (CLI) provided with the package:

```bash
> AnDOCreator data.csv data/

```

OR

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
