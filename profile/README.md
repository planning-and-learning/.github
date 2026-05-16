## Planning and Learning

Planning and Learning is an ecosystem of C++ libraries and Python packages for integrating learning with planning-based systems.

The projects provide efficient C++ implementations, Python bindings, and
pip-installable packages for downstream use. Currently, the ecosystem consists
of four projects that build upon one another.
  
### Projects

- **[yggdrasil](https://github.com/planning-and-learning/yggdrasil)** provides
  shared third-party native dependencies used by the other projects. Its Python
  distribution is published as `pyyggdrasil`.
- **[loki](https://github.com/planning-and-learning/loki)** provides PDDL
  parsing, normalization, and translation utilities. Its Python distribution is
  published as `pypddl`.
- **[tyr](https://github.com/planning-and-learning/tyr)** provides planning
  data structures, ground and lifted successor generation, search algorithms,
  and Python bindings. Its Python distribution is published as `pytyr`.
- **[runir](https://github.com/planning-and-learning/runir)** provides
  representations for generalized planning, including task classes, state and
  equivalence graphs, description-logic feature languages, and rule-based policy
  tooling. Its Python distribution is published as `pyrunir`.
  
### Installation

The packages are layered, so installing a downstream package pulls in the native
packages it needs:

```console
pip install pyyggdrasil pypddl pytyr pyrunir
```

### Local Development

For local development, clone the repositories into a shared
`planning-and-learning` workspace so that dependent projects can refer to each
other as sibling checkouts:

```text
planning-and-learning/
  yggdrasil/
  loki/
  tyr/
  runir/
  learning-general-policies/
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
python -m pip install ../yggdrasil ../loki ../tyr ../runir

cmake -S . -B build \
  -DCMAKE_PREFIX_PATH="$(python -c 'import os, pyyggdrasil, pypddl, pytyr, pyrunir; print(os.pathsep.join(map(str, [pyyggdrasil.native_prefix(), pypddl.native_prefix(), pytyr.native_prefix(), pyrunir.native_prefix()])))')"
cmake --build build
```

### CMake Integration

Each Python package exposes a `native_prefix()` helper that points to the
installed C++ headers, shared libraries, and CMake package configuration files.
Downstream CMake projects can use these prefixes through `CMAKE_PREFIX_PATH`.

For example, to consume `runir` from an installed `pyrunir` package, include the
native prefixes of `pyrunir` and its native package dependencies:

```console
python -m pip install pyrunir

cmake -S . -B build \
  -DCMAKE_PREFIX_PATH="$(python -c 'import os, pyyggdrasil, pypddl, pytyr, pyrunir; print(os.pathsep.join(map(str, [pyyggdrasil.native_prefix(), pypddl.native_prefix(), pytyr.native_prefix(), pyrunir.native_prefix()])))')"
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
find_package(loki CONFIG REQUIRED)
find_package(tyr CONFIG REQUIRED)
find_package(runir CONFIG REQUIRED COMPONENTS core)
```

`runir` exports `runir::core` as the aggregate target, plus component targets
such as `runir::graphs`, `runir::datasets`, and `runir::kr`.
