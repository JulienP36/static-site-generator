from file_ops import clear_then_copy
from page_generation import generate_page

dir_path_static = "./static"
dir_path_public = "./public"

def main():
    clear_then_copy(dir_path_static, dir_path_public)
    generate_page("content/index.md", "template.html", "public/index.html")

if __name__ == "__main__":
    main()