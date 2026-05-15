## Planning and Learning

Planning and Learning is an ecosystem of C++ libraries and Python packages for integrating learning with planning-based systems.

The projects provide efficient C++ implementations, Python bindings, and pip-installable packages for downstream use. Currently, the ecosystem consists of four projects that build upon
one another.
  
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

### Python Integration

Each Python package can be imported directly and exposes a `native_prefix()`
helper that points to the installed C++ headers, shared libraries, and CMake
package configuration files:

```python
import pytyr

print(pytyr.native_prefix())
```

### CMake Integration

The Python packages install C++ headers, shared libraries, and CMake package
configuration files under their `native_prefix()`. Downstream CMake projects can
use these prefixes through `CMAKE_PREFIX_PATH`.

For example, to consume `runir` from an installed `pyrunir` package:

```console
python -m pip install pyrunir

cmake -S . -B build \
  -DCMAKE_PREFIX_PATH="$(python -c 'import os, pyrunir, pyyggdrasil; print(os.pathsep.join(map(str, [pyrunir.native_prefix(), pyyggdrasil.native_prefix()])))')"
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

