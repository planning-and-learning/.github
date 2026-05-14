## Planning and Learning

Planning and Learning develops native C++ libraries with Python packages for
automated planning, lifted reasoning, and learning-oriented tooling around
planning tasks.

The projects are designed to work both as C++ libraries and as pip-installable
Python packages. The Python packages also ship the native headers, shared
libraries, and CMake package files needed by downstream C++/Python projects.

### Projects

- **[yggdrasil](https://github.com/planning-and-learning/yggdrasil)** provides
  the shared native dependency prefix used by the other projects. Its Python
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
pip install pyyggdrasil
pip install pypddl
pip install pytyr
pip install pyrunir
```

For CMake consumers, each package exposes a `native_prefix()` helper that points
to the installed native prefix:

```python
import pytyr

print(pytyr.native_prefix())
```
