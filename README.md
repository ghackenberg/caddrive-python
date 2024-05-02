# CADdrive Python Services

This repository contains the CADdrive Python Services. The services include two applications, namely LeoFEA and LeoVR, for running and visualizating finite element simulations. Furthermore, the repository contains several services for running finite element method (FEM) and computational fluid dynamics (CFD) simulations. Finally, the applications and services are based on a custom Python package providing common functionalities.

## Applications

This repository contains to end-user applications: **LeoFEA** and **LeoVR**.

### LeoFEA ([read more](./applications/leofea/))

This application runs finite element simulations.

*Screenshot coming soon.*

### LeoVR ([read more](./applications/leovr/))

This application visualizes the results of finite element simulation.

![](./screenshots/finite-element-analysis.png)

## Services

The application use services exposing HTTP REST APIs.

![](./diagrams/services.png)

## Packages

The packages provide common functionality for the applications and services.

* [CADdrive Python SDK](./packages/caddrive/)

## Guides

Install **CADdrive Python SDK** on your local computer:

```sh
pip install -e ./packages/caddrive
```

Run the **CADdrive Python Services** with Docker:

```sh
docker-compose up
```

## Documents

* [License](./LICENSE.md)
* [Changelog](./CONTRIBUTING.md)
* [Contributing](./CONTRIBUTING.md)