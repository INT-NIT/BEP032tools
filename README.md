# AnDOChecker

The Animal Data Organization (AnDO) is a set of specifications for the organization of a directory containing experimental data recorded in animals. It is very inspired by the BIDS specifications ( https://bids-specification.readthedocs.io ). The main difference lies in the fact that in experiments conducted with animals, it is very common to have different settings for different sessions, and more importantly for different animals (whereas research on human subjects tends to have exactly the same protocol used for all subjects, as looked after by the BIDS specifications).

Futher information on Specs : https://int-nit.github.io/AnDOChecker/

[![PyPI license](https://img.shields.io/pypi/l/ansicolortags.svg)](https://pypi.python.org/pypi/ansicolortags/)[![Generic badge](https://travis-ci.org/Slowblitz/BidsValidatorA.svg?branch=master)](https://shields.io/)[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

## Installation
### Dependencies

AnDOChecker requires:

- Python (>= 3.6)
- Pip

### User installation
```bash
> Pip3 install AnDOchecker
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
> Python3 checker/AnDOChecker.py tests/ds001/data/Enya
```

OR verbose usage

```bash
> Python3 checker/AnDOChecker.py -v tests/ds001/data/Enya

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
Source code
-----------

You can check the latest sources with the command:

    git clone https://github.com/INT-NIT/AnDOChecker.git
    
Contributing
------------

To learn more about making a contribution to scikit-learn, please see
our [Contributing guide][].

Testing
-------

After installation, you can launch the test suite from outside the
source directory (you will need to have `pytest` installed):

    pytest ando



Submitting a Pull Request
-------------------------

Before opening a Pull Request, have a look at the full Contributing page
to make sure your code complies with our guidelines.