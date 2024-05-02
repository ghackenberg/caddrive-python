# CADdrive LeoFEA

A graphical user interface for the LeoFEA service with Qt.

## Developer guide

### Install external dependencies

External dependencies can be installed from the requirements file.

```sh
cd <root>/applications/leofea

pip install -r requirements.txt
```

### Install internal dependencies

Internal dependencies must be installed from the source directories.

```sh
cd <root>/packages/caddrive

pip install -e .
```