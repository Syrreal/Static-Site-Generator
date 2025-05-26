class HTMLNode():

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if self.props:
            return "".join(list(map(lambda x: f' {x}="{self.props[x]}"', self.props)))

    def __repr__(self):
        return f'''HTMLNode({self.tag}, {self.value},\n
                {self.children},\n
                {self.props})\n
                '''
    
class LeafNode(HTMLNode):
    
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value:
            if not self.tag:
                return self.value
            else:
                if self.props:
                    return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
                else:
                    return f'<{self.tag}>{self.value}</{self.tag}>'
        raise ValueError(f"Value required in leaf node: {self}")
