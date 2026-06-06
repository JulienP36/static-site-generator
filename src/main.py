from textnode import TextNode
from textnode import TextType

def main():
    node = TextNode()
    node.text = "This is some anchor text"
    node.text_type = TextType.TEXT
    node.url = "https://www.boot.dev"
    print(node)

if __name__ == "__main__":
    main()