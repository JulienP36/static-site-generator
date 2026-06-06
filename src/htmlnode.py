
class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list["HTMLNode"] | None = None,
        props: dict[str, str] | None = None,
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError("to_html method not implemented in HTMLNode class")
    
    def props_to_html(self) -> str:
        if self.props is None:
            return ""
        props_html = ""
        for prop in self.props:
            props_html += f' {prop}="{self.props[prop]}"'
        return props_html
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(
            self,
            tag: str | None,
            value: str,
            props: dict[str, str] | None = None
        ) -> None:
        super().__init__(tag, value, None, props)
        self.tag = tag
        self.value = value
        self.props = props
    
    def to_html(self) -> str:
        if self.value == "":
            raise ValueError("The leaf node's value cannot be empty")
        if self.tag is None: # if no tag, return as raw text
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.props})"