## Welcome to the Planning and Learning Organisation

This organisation provides a collection of pip-installable C++ libraries with Python bindings for tackeling various objectives in the automated planning and learning.

The organisation currently consists of the following repositories:

- yggdrasil: the C++ dependency provider
- loki: depends on yggdrasil. It is a C++ library for parsing and normalizing planning tasks and domains specified in the planning domain definition language (PDDL)
- tyr: depends on yggdrasil and loki. It is a C++ library with Python bindings for implementing ground and lifted search algorithms on normalized planning tasks and domains.
