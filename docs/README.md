# How to build the documentation

The documentation uses `Sphinx` including some extensions. 

## Install requirements

```
cd docs
pip install -r requirements.txt
```
## Create rst files
If there is no conf.py file, create one with `sphinx-quickstart`.

Then create the rst files with `sphinx-apidoc`:

```
sphinx-apidoc -o .  ../pyccapt
```

## Build

```
make clean html
make html
```

Starting point for output is found at 

```
./_build/html/index.html
```

