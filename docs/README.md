# How to build the documentation

The documentation uses `Sphinx` including some extensions. 

## Install requirements

```
pip install -r requirements.txt
```
## Create rst files
```
sphinx-quickstart
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

