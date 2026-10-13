import contextlib
import io
import tempfile
import unittest
from pathlib import Path

import av_enum


class OutputTests(unittest.TestCase):
    def test_output_file_contains_report_and_stdout_is_preserved(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "report.txt"
            stdout = io.StringIO()

            with contextlib.redirect_stdout(stdout):
                result = av_enum.main(["localhost-é", "--yes", "--output", str(output_path)])

            self.assertEqual(result, 0)
            self.assertEqual(output_path.read_text(encoding="utf-8"), stdout.getvalue())
            self.assertIn("[*] target : localhost-é", stdout.getvalue())
            self.assertIn("[*] output : " + str(output_path), stdout.getvalue())

    def test_output_write_failure_is_reported_without_traceback(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            missing_parent_path = Path(temp_dir) / "missing" / "report.txt"
            stdout = io.StringIO()
            stderr = io.StringIO()

            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                result = av_enum.run(
                    av_enum.argparse.Namespace(
                        target="localhost",
                        output=str(missing_parent_path),
                        verbose=False,
                    )
                )

            self.assertEqual(result, 1)
            self.assertEqual(stdout.getvalue(), "")
            self.assertIn("could not write output file", stderr.getvalue())
            self.assertNotIn("Traceback", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
