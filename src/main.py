import sys
from file_ops import clear_then_copy
from page_generation import generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"

def main():
    
    clear_then_copy(dir_path_static, dir_path_public)
    generate_pages_recursive(dir_path_content, "template.html", dir_path_public)

if __name__ == "__main__":
    main()