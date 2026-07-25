import unittest

from stage_version import replace_cmake_dependency


class ReplaceCMakeDependencyTest(unittest.TestCase):
    def test_updates_referenced_version_variable(self):
        source = """\
set(LOKI_YGGDRASIL_REQUIRED_VERSION 0.0.25)
find_package(
    yggdrasil ${LOKI_YGGDRASIL_REQUIRED_VERSION}
    CONFIG REQUIRED
)
"""
        expected = source.replace("0.0.25", "999.0.5")

        self.assertEqual(replace_cmake_dependency(source, "yggdrasil", "999.0.5"), expected)

    def test_keeps_configure_file_placeholder(self):
        source = "find_dependency(yggdrasil @LOKI_YGGDRASIL_REQUIRED_VERSION@ CONFIG REQUIRED)\n"

        self.assertEqual(replace_cmake_dependency(source, "yggdrasil", "999.0.5"), source)


if __name__ == "__main__":
    unittest.main()
