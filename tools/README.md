# AnDOtools

AnDOtools is a little project that contain two scripts :
- a script to help users generate an AnDO structure based on a csv file 
(You can find in the Creator folder one exemple of a CSV file names "exemple.csv")
- a script to help users to dispay an AnDO structure



## Installation
### Dependencies

AnDOChecker requires:

- Python (>= 3.6)
- Pip3
- tree

### User installation 

```bash
> pip install AnDOcreator
> pip install AnDOviewer
```

### General usage for the creator script 

```term
usage: AnDO_Creator.py [-h] pathToCsv pathToDir

positional arguments:
  pathToCsv   Path to your folder
  pathToDir   Path to your csv file

optional arguments:
  -h, --help  show this help message and exit
```


### General usage for the veiwer script 

```term
usage: AnDO_Viewer.py [-h] [-S] [-Se] [-Su] [-Ss] pathToDir

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
> AnDOcreator data.csv data/

```

OR


```bash
> AnDOviewer data/

```
# Development

We welcome new contributors of all experience levels.  The
[Development Guide][] has detailed information about contributing code,
documentation, tests, and more. We've included some basic information in
this README.
