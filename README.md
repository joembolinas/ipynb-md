---
title: Notebook To Markdown Converter
emoji: 🌖
colorFrom: indigo
colorTo: yellow
sdk: gradio
sdk_version: 5.16.0
app_file: app.py
pinned: false
license: apache-2.0
short_description: Converts jupyter notebooks to markdown files.
---

## Notebook to Markdown Converter

Convert Jupyter notebooks (`.ipynb`) to Markdown using a simple Gradio web UI.

This converter includes:

- Markdown and code cell content
- Code cell outputs (including charts/diagrams when present in notebook outputs)
- Friendly error messages for invalid uploads

## Features

- Supports notebook uploads from the web interface
- Handles both filepath-based and file-like notebook inputs
- Preserves code blocks as fenced Python markdown
- Includes common output types:
  - `stream` output (`stdout`/`stderr`) as fenced text
  - `error` traceback as fenced text
  - `image/png` as embedded data URI markdown image
  - `image/svg+xml` inline SVG
  - `text/html` inline HTML
  - `text/plain` as fenced text

## Requirements

- Python 3.10+
- `gradio`

## Quick Start (Windows PowerShell)

From the project root:

1. Create a virtual environment (if needed)
2. Activate it
3. Install dependencies
4. Run the app

Example commands:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install gradio
python app.py
```

Once running, open the local Gradio URL shown in the terminal, upload an `.ipynb`, and copy the generated markdown.

## Running Tests

The project includes `unittest` coverage for core conversion behavior.

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

## Why some charts/diagrams may still be missing

The converter can only include outputs that are already saved in the notebook file. If visuals are missing, usually one of these is true:

- The notebook cell was not executed before saving
- Outputs were cleared before saving
- The visualization is rendered externally and not stored in the notebook `outputs`

Tip: re-run the notebook cells and save the `.ipynb` with outputs before converting.

## Troubleshooting

### `ModuleNotFoundError: gradio is required...`

Install Gradio in the same Python environment used to run `app.py`.

### PowerShell execution policy command fails

If `Set-ExecutionPolicy` cannot load in your shell, activate the virtual environment from a standard PowerShell instance or run Python directly from `.venv\Scripts\python.exe`.

## Acknowledgments

This project is inspired by the original Hugging Face Space:

- **m-ric / notebook_to_markdown**: <https://huggingface.co/spaces/m-ric/notebook_to_markdown>

Special thanks to **m-ric (Aymeric Roucher)** for the original idea and implementation that inspired this project.

This repository is my learning-driven adaptation, built with gratitude and expanded with additional handling for notebook outputs (including chart/diagram rendering data where available).

## Hugging Face Spaces

This repository includes Spaces frontmatter metadata at the top of this file.
For configuration options, see:

- <https://huggingface.co/docs/hub/spaces-config-reference>
