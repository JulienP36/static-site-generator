import sys
from file_ops import clear_then_copy
from page_generation import generate_pages_recursive

dir_path_static = "./static"
dir_path_output = "./docs"
dir_path_content = "./content"

def main():
    if len(sys.argv) == 1:
        basepath = "/"
    elif len(sys.argv) == 2:
        basepath = sys.argv[1]
    else:
        raise Exception("Too many arguments")
    
    print(f"sys.argv = {sys.argv}")
    
    clear_then_copy(dir_path_static, dir_path_output)
    generate_pages_recursive(dir_path_content, "template.html", dir_path_output, basepath)

if __name__ == "__main__":
    main()