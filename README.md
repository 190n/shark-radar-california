# shark radar (California edition)
where are the cuddlies at?

## How To

### Install Python

Install Python 3 for your OS: https://www.python.org/downloads/

### Install Dependancies

`pip install requests`

### Run It

Navigate to the folder you've downloaded `cd path/to/shark-radar-california` and run the list.py script with python `python list.py`. This will output fancy HTML because I wanted to make a version of this accessible on the web. If you'd like output suitable for a terminal, checkout commit [bc68ef6](https://github.com/190n/shark-radar-california/tree/bc68ef6) (and maybe backport [the sorting changes](https://github.com/190n/shark-radar-california/commit/b7ea33cd9599f17580feb30d1d0c875de9833f4f#diff-8ff389d9f192b8783e5093ac8c9c5ef34c6e298a115abad116528f0149d8b616R81-R82) I made while adding HTML support if you'd like stores with no stock to be sorted by the restock date).

## Credit

- [Originally](https://git.lavender.software/charlotte/shark-radar) made by [Charlotte Som](https://github.com/videogame-hacker)
- Modified by [Bastian](https://github.com/basti564) to support german IKEA stores.
- Modified by [me](https://github.com/190n) and [@blahajessie](https://github.com/blahajessie) to look at stores in California.
