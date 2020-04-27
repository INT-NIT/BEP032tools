# AnDOChecker
Checks the validity of a directory with respect to the ANimal Data Organization (AnDO) specifications 

![version](https://img.shields.io/badge/version-2-informational)

[![PyPI license](https://img.shields.io/pypi/l/ansicolortags.svg)](https://pypi.python.org/pypi/ansicolortags/)[![Generic badge](https://travis-ci.org/Slowblitz/BidsValidatorA.svg?branch=master)](https://shields.io/)[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

# Table of Contents
1. [ General usage](#General-usage)
2. [Specific usage](#Specific-usage)
3. [Testing usage](#Testing-usage )
4. [Details](#Details)
# Use
### Clone

- Clone this repo to your local machine using `https://github.com/INT-NIT/AnDOChecker.git`
## General usage :
```
usage: AnDOChecker.py [-h] [-v] path

positional arguments:
  path           Path to your folder

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  increase output verbosity

```

## Specific usage :

```
$Python3 checker/AnDOChecker.py tests/ds001/data/Enya
```
<p align="center"><img src="Documents/vids/Exemple_no_verbose.gif" /></p>





OR verbose usage  :
```
$Python3 checker/AnDOChecker.py -v tests/ds001/data/Enya

```

<p align="center"><img src="Documents/vids/Exemple_w_verbose.gif" /></p>


# Development 
## Testing usage :

```
$cd checker/
$python3.5 -m unittest discover -v
```
## Details :

In resources folder  :

 - file AnDOChecker.py is the main file 
 - file AnDO_Error.py is the custom error exception file
 - file AnDO_Engine.py is the file that verify  with the rules 

In the Rules folder :

 - session_rules.json regex for session rules
 - subject_rules.json regex for subject rules
 - source_rules.json  regex for source rules

