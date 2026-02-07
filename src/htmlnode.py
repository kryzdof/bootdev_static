class HTMLNode:
    def __init__(self, tag: [None, str] = None, value:[None, str] = None, children = None, props: [None, dict] = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        prop_string = ""
        if self.props:
            for k,v in self.props.items():
                prop_string += f' {k}="{v}"'
        return prop_string

    def __repr__(self):
        return f"HTMLNode(tag: {self.tag}, value: {self.value}, kids: {self.children}, props: {self.props_to_html()})"

