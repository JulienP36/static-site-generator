import os, pathlib
from markdown_ops_blocks import extract_title, markdown_to_html_node

def get_file_content(file_path: str) -> str:
    if os.path.isfile(file_path):
        with open(file_path, 'r') as file:
            content = file.read()
        return content
    else:
        raise FileNotFoundError(f'File not found at "{file_path}"')

def generate_page(from_path: str, template_path: str, dest_path: str, base_path: str) -> None:
    print(f'Generating page from "{from_path}" to "{dest_path}" using "{template_path}"')

    template_content = get_file_content(template_path)
    markdown_content = get_file_content(from_path)
    markdown_node = markdown_to_html_node(markdown_content)
    html_content = markdown_node.to_html()
    title = extract_title(markdown_content)
    template_content = template_content.replace("{{ Title }}", title, 1)
    template_content = template_content.replace("{{ Content }}", html_content, 1)
    print(f"base_path: {base_path}")
    template_content = template_content.replace('href="/', f'href="{base_path}')
    template_content = template_content.replace('src="/', f'src="{base_path}')

    dest_dir = os.path.dirname(dest_path)
    if dest_dir != "":
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, 'w') as dest_file:
        dest_file.write(template_content)

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str, base_path: str) -> None:
    if os.path.isdir(dir_path_content):
        dir_content = os.listdir(dir_path_content)
        for file in dir_content:
            file_path = os.path.join(dir_path_content, file)
            file_path_target = os.path.join(dest_dir_path, file)
            if os.path.isfile(file_path):
                file_extension = pathlib.Path(file_path).suffix.lower()
                if file_extension == ".md":
                    file_path_target = pathlib.Path(file_path_target).with_suffix(".html")
                    generate_page(file_path ,template_path , file_path_target, base_path)
                else:
                    print(f'Skipping "{file}" because it is not a markdown file')
            elif os.path.isdir(file_path):
                dir_to_check = os.path.join(dir_path_content, file)
                generate_pages_recursive(dir_to_check, template_path, file_path_target, base_path)
    else:
        raise Exception("The path provided is not a directory")