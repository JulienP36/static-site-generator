import os
from markdown_ops_blocks import extract_title, markdown_to_html_node

def get_file_content(file_path: str) -> str:
    if os.path.isfile(file_path):
        with open(file_path, 'r') as file:
            content = file.read()
        return content
    else:
        raise FileNotFoundError(f'File not found at "{file_path}"')

def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f'Generating page from "{from_path}" to "{dest_path}" using "{template_path}"')

    template_content = get_file_content(template_path)
    markdown_content = get_file_content(from_path)
    markdown_node = markdown_to_html_node(markdown_content)
    html_content = markdown_node.to_html()
    title = extract_title(markdown_content)
    template_content = template_content.replace("{{ Title }}", title, 1)
    template_content = template_content.replace("{{ Content }}", html_content, 1)

    dest_dir = os.path.dirname(dest_path)
    if dest_dir != "":
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, 'w') as dest_file:
        dest_file.write(template_content)