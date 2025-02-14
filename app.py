import json
import gradio as gr

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
        content = json.load(file)
        
        # Initialize markdown output
        markdown_output = []
        
        # Process each cell
        for cell in content['cells']:
            # Handle markdown cells
            if cell['cell_type'] == 'markdown':
                markdown_output.extend(cell['source'])
                markdown_output.append('\n')
                
            # Handle code cells
            elif cell['cell_type'] == 'code':
                markdown_output.append('```python\n')
                markdown_output.extend(cell['source'])
                markdown_output.append('\n```\n')
        
        # Join all content
        final_markdown = ''.join(markdown_output)
        
        return final_markdown
        
    except Exception as e:
        return f"Error converting notebook: {str(e)}"

# Create Gradio interface
iface = gr.Interface(
    fn=convert_notebook_to_markdown,
    inputs=gr.File(
        label="Upload Jupyter Notebook (.ipynb)",
        file_types=[".ipynb"]
    ),
    outputs=gr.Textbox(
        label="Converted Markdown",
        lines=20
    ),
    title="Jupyter Notebook to Markdown Converter",
    description="Upload a Jupyter notebook (.ipynb) file to convert it to Markdown format. Code cells will be wrapped in Python code blocks.",
    examples=[],
    cache_examples=False
)

# Launch the app
iface.launch()