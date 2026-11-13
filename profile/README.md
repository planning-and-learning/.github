## Planning and Learning

Planning and Learning is an ecosystem of C++ libraries and Python packages for integrating learning with planning-based systems.

The projects provide efficient C++ implementations, Python bindings, and
pip-installable packages for downstream use. The ecosystem consists of projects
that build upon one another.

### Projects

- **[brokkr](https://github.com/planning-and-learning/brokkr)** provides the
  build tooling for native C++ libraries shipped as Python wheels: CMake helpers
  and a scikit-build-core backend.
  Its Python distribution is published as `pybrokkr`.
- **[urd](https://github.com/planning-and-learning/urd)** provides containers
  described by what the data is, as headers and a CMake package.
  Its Python distribution is published as `pyurd`.
  The same repository publishes `pyurd-native`, the shared third-party native
  dependencies of all projects as one prefix.
- **[vefr](https://github.com/planning-and-learning/vefr)** provides graph
  algorithms over urd's graphs: color refinement, Weisfeiler-Leman, canonical
  forms by nauty, searches, and shortest paths, and Python bindings.
  Its Python distribution is published as `pyvefr`.
- **[yggdrasil](https://github.com/planning-and-learning/yggdrasil)** provides
  shared data structures and a database engine used by the planning projects.
  Its Python distribution is published as `pyyggdrasil`.
- **[loki](https://github.com/planning-and-learning/loki)** provides PDDL
  parsing, normalization, and translation utilities, and Python bindings.
  Its Python distribution is published as `pypddl`.
- **[tyr](https://github.com/planning-and-learning/tyr)** provides planning
  data structures, ground and lifted successor generation, search algorithms,
  and Python bindings. Its Python distribution is published as `pytyr`.
- **[runir](https://github.com/planning-and-learning/runir)** provides
  representations for generalized planning, including task classes, state and
  equivalence graphs, description-logic feature languages, rule-based policy
  tooling, and Python bindings.
  Its Python distribution is published as `pyrunir`.
- **[planning-benchmarks](https://github.com/planning-and-learning/planning-benchmarks)**
  provides classical and numeric benchmark suites for testing and profiling, and PDDL generators.

### Installation

The packages are layered, so installing a downstream package pulls in the native
packages it needs:

```console
pip install pybrokkr pyurd pyvefr pyyggdrasil pypddl pytyr pyrunir
```

### Local Development

For local development, clone the repositories into a shared
`planning-and-learning` workspace so that dependent projects can refer to each
other as sibling checkouts:

```text
planning-and-learning/
  brokkr/
  urd/
  vefr/
  yggdrasil/
  loki/
  tyr/
  runir/
  planning-benchmarks/
```

#### Python

Python projects can depend on a sibling checkout by using a relative path in
`requirements.txt` or `pyproject.toml`. For example, a project that should use
the local `runir` checkout can depend on:

```text
../runir
```

Installing the requirements then builds and installs the local package instead
of downloading the latest released wheel:

```console
python -m pip install -r requirements.txt
```

#### C++

C++ projects can consume the native prefixes provided by the Python packages.
For local development, install the sibling Python packages into the active
environment, then pass their `native_prefix()` locations to CMake through
`CMAKE_PREFIX_PATH`.

For example, a project that consumes `runir` can configure CMake with:

```console
python -m pip install ../brokkr ../urd/python ../urd ../vefr ../yggdrasil ../loki ../tyr ../runir

cmake -S . -B build \
  -DCMAKE_PREFIX_PATH="$(python -c 'import os, pyurd_native, pyurd, pyvefr, pyyggdrasil, pypddl, pytyr, pyrunir; print(os.pathsep.join(str(package.native_prefix()) for package in (pyurd_native, pyurd, pyvefr, pyyggdrasil, pypddl, pytyr, pyrunir)))')"
cmake --build build
```

### Building from Source

Every package builds with a standard PEP 517 frontend. From a package checkout,
build and install it into the active environment with:

```console
python -m pip install .
```

or produce a wheel with:

```console
uv build --wheel
```

The packages are layered, so when building from source install the chain
bottom-up — `pybrokkr` → `pyurd-native` → `pyurd` → `pyvefr` → `pyyggdrasil` →
`pypddl` → `pytyr` → `pyrunir` — so that each package can resolve the native
prefixes of the providers it depends on. Each repository README documents its
package-specific build options and CMake flags.

### CMake Integration

Each Python package exposes a `native_prefix()` helper that points to the
installed C++ headers, shared libraries, and CMake package configuration files.
Downstream CMake projects can use these prefixes through `CMAKE_PREFIX_PATH`.

For example, to consume `runir` from an installed `pyrunir` package, include the
native prefixes of `pyrunir` and its native package dependencies:

```console
python -m pip install pyrunir

cmake -S . -B build \
  -DCMAKE_PREFIX_PATH="$(python -c 'import os, pyurd_native, pyurd, pyvefr, pyyggdrasil, pypddl, pytyr, pyrunir; print(os.pathsep.join(str(package.native_prefix()) for package in (pyurd_native, pyurd, pyvefr, pyyggdrasil, pypddl, pytyr, pyrunir)))')"
cmake --build build
```

A downstream `CMakeLists.txt` can then use the exported targets:

```cmake
cmake_minimum_required(VERSION 3.21)

project(example LANGUAGES CXX)

find_package(runir CONFIG REQUIRED COMPONENTS core)

add_executable(example main.cpp)
target_link_libraries(example PRIVATE runir::core)
```

For package-specific CMake targets, use the corresponding package config:

```cmake
find_package(urd CONFIG REQUIRED)
find_package(vefr CONFIG REQUIRED)
find_package(loki CONFIG REQUIRED)
find_package(tyr CONFIG REQUIRED)
find_package(runir CONFIG REQUIRED COMPONENTS core)
```

`runir` exports `runir::core` as the aggregate target, plus component targets
such as `runir::graphs`, `runir::datasets`, and `runir::kr`.
