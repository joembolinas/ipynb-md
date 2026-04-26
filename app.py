import json
import os

try:
    import gradio as gr
except ModuleNotFoundError:  # Enables test/import without Gradio dependency
    gr = None


def _normalize_text_lines(value):
    """Return notebook text-like values as a list of strings."""
    if value is None:
        return []
    if isinstance(value, list):
        return [str(line) for line in value]
    return [str(value)]


def _append_output_as_markdown(markdown_output, output):
    """Append one notebook output object to markdown_output list."""
    output_type = output.get("output_type")

    if output_type == "stream":
        text_lines = _normalize_text_lines(output.get("text"))
        if text_lines:
            markdown_output.append("```text\n")
            markdown_output.extend(text_lines)
            if not text_lines[-1].endswith("\n"):
                markdown_output.append("\n")
            markdown_output.append("```\n\n")
        return

    if output_type == "error":
        traceback_lines = _normalize_text_lines(output.get("traceback"))
        if traceback_lines:
            markdown_output.append("```text\n")
            markdown_output.extend(traceback_lines)
            if not traceback_lines[-1].endswith("\n"):
                markdown_output.append("\n")
            markdown_output.append("```\n\n")
        return

    data = output.get("data", {})
    if not isinstance(data, dict):
        return

    # Prefer rich media first so charts/diagrams are preserved visually.
    png_data = data.get("image/png")
    if png_data:
        png_text = "".join(_normalize_text_lines(png_data)).replace("\n", "")
        markdown_output.append(
            f"![notebook output](data:image/png;base64,{png_text})\n\n"
        )
        return

    svg_data = data.get("image/svg+xml")
    if svg_data:
        markdown_output.extend(_normalize_text_lines(svg_data))
        if not str(markdown_output[-1]).endswith("\n"):
            markdown_output.append("\n")
        markdown_output.append("\n")
        return

    html_data = data.get("text/html")
    if html_data:
        markdown_output.extend(_normalize_text_lines(html_data))
        if not str(markdown_output[-1]).endswith("\n"):
            markdown_output.append("\n")
        markdown_output.append("\n")
        return

    plain_text = data.get("text/plain")
    if plain_text:
        plain_lines = _normalize_text_lines(plain_text)
        markdown_output.append("```text\n")
        markdown_output.extend(plain_lines)
        if not plain_lines[-1].endswith("\n"):
            markdown_output.append("\n")
        markdown_output.append("```\n\n")


def _load_notebook_content(file):
    """Load notebook JSON from a Gradio upload value.

    Supports file-like objects, file paths (including Gradio NamedString),
    and objects carrying a ``name`` path.
    """
    if file is None:
        raise ValueError("No file uploaded")

    if hasattr(file, "read"):
        return json.load(file)

    if isinstance(file, (str, os.PathLike)):
        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)

    file_name = getattr(file, "name", None)
    if isinstance(file_name, (str, os.PathLike)):
        with open(file_name, "r", encoding="utf-8") as f:
            return json.load(f)

    raise TypeError(
        f"Unsupported uploaded file type: {type(file).__name__}. "
        "Expected a file path or file-like object."
    )


def convert_notebook_to_markdown(file):
    """
    Convert a Jupyter notebook file to Markdown format.

    Args:
        file: Uploaded file object from Gradio
    Returns:
        str: Converted markdown content
    """
    try:
        # Read the notebook content
        content = _load_notebook_content(file)

        # Initialize markdown output
        markdown_output = []

        # Process each cell
        for cell in content["cells"]:
            # Handle markdown cells
            if cell["cell_type"] == "markdown":
                markdown_output.extend(_normalize_text_lines(cell.get("source")))
                markdown_output.append("\n")

            # Handle code cells
            elif cell["cell_type"] == "code":
                markdown_output.append("```python\n")
                markdown_output.extend(_normalize_text_lines(cell.get("source")))
                markdown_output.append("\n```\n")

                for output in cell.get("outputs", []):
                    _append_output_as_markdown(markdown_output, output)

        # Join all content
        final_markdown = "".join(markdown_output)

        return final_markdown

    except Exception as e:
        return f"Error converting notebook: {str(e)}"


# Create Gradio interface
iface = None
if gr is not None:
    iface = gr.Interface(
        fn=convert_notebook_to_markdown,
        inputs=gr.File(
            label="Upload Jupyter Notebook (.ipynb)",
            type="filepath",
            file_types=[".ipynb"],
        ),
        outputs=gr.Textbox(label="Converted Markdown", lines=20),
        title="Jupyter Notebook to Markdown Converter",
        description="Upload a Jupyter notebook (.ipynb) file to convert it to Markdown format. Code cells will be wrapped in Python code blocks.",
        examples=[],
        cache_examples=False,
    )

# Launch the app
if __name__ == "__main__":
    if iface is None:
        raise ModuleNotFoundError(
            "gradio is required to launch the web interface. "
            "Install it with: pip install gradio"
        )
    iface.launch()
