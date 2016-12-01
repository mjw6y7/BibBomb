BibBomb
=============
Simple script:

1. Checks all entries in bibtex file for required and optional fields.

2. Creates histogram of papers by year

## Usage
```
$ ./BibBomb.py -h
usage: BibBomb.py [-h] [--plot] [--keys] [--list-missing-fields]
                  [--list-optional-fields] [--list-duplicate-keys]
                  [--list-bad-keys]
                  bib_file [bib_file ...]

Check your BibTeX files

positional arguments:
  bib_file              BibTeX files to check

optional arguments:
  -h, --help            show this help message and exit
  --plot                Plot a histogram of pulication years
  --keys                Check citation keys
  --list-missing-fields
                        List entries with missing required fields
  --list-optional-fields
                        List entries with missing optional fields
  --list-duplicate-keys
                        List entries with duplicate keys
  --list-bad-keys       List entries with badly formatted keys
```

## Installation

Run `sudo pip install -r requirements.txt` to install the dependencies. You may want to put `BibBomb.py` somewhere in your `$PATH`
