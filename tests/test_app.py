import io
import json
import tempfile
import unittest
from pathlib import Path

from app import _load_notebook_content, convert_notebook_to_markdown


class NotebookConversionTests(unittest.TestCase):
    def test_convert_from_filepath(self):
        notebook = {
            "cells": [
                {"cell_type": "markdown", "source": ["# Title\n", "Text\n"]},
                {"cell_type": "code", "source": ["print('hello')\n"]},
            ]
        }

        with tempfile.TemporaryDirectory() as tmp:
            nb_path = Path(tmp) / "sample.ipynb"
            nb_path.write_text(json.dumps(notebook), encoding="utf-8")

            result = convert_notebook_to_markdown(str(nb_path))

        self.assertIn("# Title", result)
        self.assertIn("```python", result)
        self.assertIn("print('hello')", result)

    def test_load_from_file_like_object(self):
        notebook = {"cells": [{"cell_type": "markdown", "source": ["Hi\n"]}]}
        file_like = io.StringIO(json.dumps(notebook))

        loaded = _load_notebook_content(file_like)

        self.assertEqual(loaded["cells"][0]["cell_type"], "markdown")

    def test_load_raises_for_none(self):
        with self.assertRaises(ValueError):
            _load_notebook_content(None)

    def test_convert_returns_error_for_bad_input_type(self):
        result = convert_notebook_to_markdown(object())
        self.assertTrue(result.startswith("Error converting notebook:"))

    def test_convert_includes_stream_output(self):
        notebook = {
            "cells": [
                {
                    "cell_type": "code",
                    "source": ["print('chart ready')\n"],
                    "outputs": [
                        {
                            "output_type": "stream",
                            "name": "stdout",
                            "text": ["chart ready\n"],
                        }
                    ],
                }
            ]
        }

        with tempfile.TemporaryDirectory() as tmp:
            nb_path = Path(tmp) / "with_stream.ipynb"
            nb_path.write_text(json.dumps(notebook), encoding="utf-8")
            result = convert_notebook_to_markdown(str(nb_path))

        self.assertIn("```text", result)
        self.assertIn("chart ready", result)

    def test_convert_includes_png_output_as_data_uri(self):
        notebook = {
            "cells": [
                {
                    "cell_type": "code",
                    "source": ["# plot\n"],
                    "outputs": [
                        {
                            "output_type": "display_data",
                            "data": {"image/png": "iVBORw0KGgoAAAANSUhEUgAAAAUA"},
                            "metadata": {},
                        }
                    ],
                }
            ]
        }

        with tempfile.TemporaryDirectory() as tmp:
            nb_path = Path(tmp) / "with_png.ipynb"
            nb_path.write_text(json.dumps(notebook), encoding="utf-8")
            result = convert_notebook_to_markdown(str(nb_path))

        self.assertIn("![notebook output](data:image/png;base64,", result)


if __name__ == "__main__":
    unittest.main()
