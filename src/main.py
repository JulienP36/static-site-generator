from textnode import TextNode
from textnode import TextType
from file_ops import clear_then_copy

dir_path_static = "./static"
dir_path_public = "./public"

def main():
    '''
    node = TextNode()
    node.text = "This is some anchor text"
    node.text_type = TextType.TEXT
    node.url = "https://www.boot.dev"
    print(node)
    '''
    clear_then_copy(dir_path_static, dir_path_public)

if __name__ == "__main__":
    main()