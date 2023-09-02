import io
import os
import sys
import unittest
from pathlib import Path

import pytest

from httprunner.cli import main
from httprunner.loader import load_project_meta
from httprunner.pyproject import project_root_path


class TestCli(unittest.TestCase):
    def setUp(self):
        self.captured_output = io.StringIO()
        sys.stdout = self.captured_output

    def tearDown(self):
        sys.stdout = sys.__stdout__  # Reset redirect.

    def test_show_version(self):
        sys.argv = ["hrun", "-V"]

        with self.assertRaises(SystemExit) as cm:
            main()

        self.assertEqual(cm.exception.code, 0)

        from httprunner import __version__

        self.assertIn(__version__, self.captured_output.getvalue().strip())

    def test_show_help(self):
        sys.argv = ["hrun", "-h"]

        with self.assertRaises(SystemExit) as cm:
            main()

        self.assertEqual(cm.exception.code, 0)

        from httprunner import __description__

        self.assertIn(__description__, self.captured_output.getvalue().strip())

    def test_debug_pytest(self):
        cwd = project_root_path
        try:
            postman_echo_dir = os.path.join(cwd, "examples", "postman_echo")
            os.chdir(postman_echo_dir)
            # call load_project_meta() to load debugtalk.py properly
            load_project_meta(Path.cwd().as_posix(), True)
            exit_code = pytest.main(
                [
                    "-s",
                    "request_methods/request_with_testcase_reference_test.py",
                ]
            )
            self.assertEqual(exit_code, 0)
        finally:
            os.chdir(cwd)
