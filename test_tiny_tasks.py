import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from tiny_tasks import load_tasks, main


class TinyTasksTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / "nested" / "tasks.json"

    def run_command(self, *args):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            main(["--file", str(self.path), *args])
        return output.getvalue()

    def assert_command_error(self, *args):
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as error:
                self.run_command(*args)
        self.assertEqual(error.exception.code, 1)

    def test_new_list_does_not_create_a_file(self):
        self.assertEqual(self.run_command("list"), "No tasks yet.\n")
        self.assertFalse(self.path.exists())

    def test_add_persists_titles_and_unique_ids(self):
        self.run_command("add", "  Learn Python  ")
        self.run_command("add", "Publish on GitHub")
        tasks = load_tasks(self.path)
        self.assertEqual([task["id"] for task in tasks], [1, 2])
        self.assertEqual(tasks[0]["title"], "Learn Python")
        self.assertFalse(tasks[0]["done"])
        self.assertIn("[ ] #2 Publish on GitHub", self.run_command("list"))

    def test_completion_persists_and_pending_filter_hides_it(self):
        self.run_command("add", "Write a README")
        self.run_command("done", "1")
        self.assertTrue(load_tasks(self.path)[0]["done"])
        self.assertIn("[x] #1 Write a README", self.run_command("list"))
        self.assertEqual(self.run_command("list", "--pending"), "No pending tasks.\n")

    def test_missing_id_preserves_data(self):
        self.run_command("add", "Keep this task")
        before = self.path.read_bytes()
        self.assert_command_error("done", "99")
        self.assertEqual(self.path.read_bytes(), before)

    def test_blank_title_is_rejected(self):
        self.assert_command_error("add", "   ")
        self.assertFalse(self.path.exists())

    def test_corrupt_data_is_never_overwritten(self):
        self.path.parent.mkdir()
        for content in ('not json', '{}', '[{"id": 1}]'):
            with self.subTest(content=content):
                self.path.write_text(content, encoding="utf-8")
                self.assert_command_error("add", "New task")
                self.assertEqual(self.path.read_text(encoding="utf-8"), content)

    def test_duplicate_ids_are_rejected(self):
        self.run_command("add", "Original")
        self.path.write_text(
            '[{"id":1,"title":"A","done":false},'
            '{"id":1,"title":"B","done":false}]', encoding="utf-8",
        )
        self.assert_command_error("list")


if __name__ == "__main__":
    unittest.main()
