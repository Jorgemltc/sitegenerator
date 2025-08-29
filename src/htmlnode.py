class HTMLNode ():
    tag  = ""
    value = ""
    children = []
    props = {}

    def __init__(self, tag = None, value = None, children = None, props = None): 
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        return ("".join( f' {k}="{v}"' for k,v in self.props.items()) if self.props is not None else "")

    def __repr__(self):
        return f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props_to_html})'
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None): 
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value is None: 
            raise ValueError("All leaf nodes must have a value")
        
        if self.tag is None: 
            return self.value
        
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
        #return super().to_html()

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None): 
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag is None: 
            raise ValueError("All parent nodes must have tag")
        
        if self.children is None: 
            raise ValueError("All parent nodes must have children")
        
        parent_string = ""
        for node in self.children:
            parent_string += node.to_html()
        
        return f'<{self.tag}{self.props_to_html()}>{parent_string}</{self.tag}>'
        #return super().to_html()