__version__ = '0.0.1'

import lark

class BraceLang:
    def __init__(self):
        # Simple language with open and close braces
        # to use { or }, use \{ or \}.
        # to use \, use \\.
        # other backslashes are interpreted as normal backslashes, i.e. \4 is the character '\' followed by the character '4'.
        # examples: 
        # - "Hello {name}!"
        # - "{attr} of {name}: {name.{attr}.value}"
        # - "This is an open brace: \{"
        self.parser = lark.Lark(
            r"""
            ?start: expr 
            expr: [(text | group)*]
            text: char+
            group: "{" expr "}"
            ?char: escaped_open_brace | escaped_close_brace | escaped_backslash | escaped_other | other_char
            ?escaped_open_brace: "\\" "{"
            ?escaped_close_brace: "\\" "}"
            ?escaped_backslash: "\\" "\\"
            ?escaped_other: "\\" other_char
            ?other_char: /[^{}\\]/
            """)
        self.setup_expected_token_to_string()
    class Text:
        def __init__(self, text): self.text = text
        def __str__(self): return self.text
        def __repr__(self): return f"Text({self.text!r})"
    class Group:
        def __init__(self, items): self.items = items
        def __str__(self): return "{"+"".join(map(str, self.items))+"}"
        def __repr__(self): return f"Group({self.items!r})"
    class Root:
        def __init__(self, items): self.items = items
        def __str__(self): return "".join(map(str, self.items))
        def __repr__(self): return f"Root({self.items!r})"
    def parse(self, text, without_root=False):
        success, exception, tree = self._parse_with_correction(text)
        if not success: raise exception
        root = self._parse_lark(tree)
        if without_root: root = self.root_to_group(root)
        return root
    def _try_parse(self, text):
        try: return True, None, self.parser.parse(text)
        except Exception as e: return False, e, None
    def _parse_with_correction(self, text):
        success, exception, tree = self._try_parse(text)
        if success: return success, exception, tree
        if isinstance(exception, lark.exceptions.UnexpectedEOF):
            for token in exception.expected:
                if token not in self._expected_token_to_string: continue
                corr = text + self._expected_token_to_string[token]
                s, e, t = self._parse_with_correction(corr)
                if s: return s, e, t
        return success, exception, tree
    def setup_expected_token_to_string(self):
        self._expected_token_to_string = {
            "RBRACE": "}"
        }
    def _parse_lark(self, tree):
        type = tree.data.value
        # the only place where a expr can be created is in the start rule and in group.
        # group is handled in the next if statement.
        if type == "expr": return self.Root([self._parse_lark(child) for child in tree.children])
        elif type == "group" and tree.children[0].data.value == "expr": return self.Group([self._parse_lark(child) for child in tree.children[0].children])
        elif type == "text": return self.Text("".join(self._parse_char(child) for child in tree.children))
        else: raise Exception(f"Unexpected type {type}, tree: {tree}")
    def _parse_char(self, tree):
        if not hasattr(tree, "data"): return tree.value
        type = tree.data.value
        if type == "escaped_open_brace": return "{"
        elif type == "escaped_close_brace": return "}"
        elif type == "escaped_backslash": return "\\"
        elif type == "escaped_other": return tree.children[0].value
        elif type == "other_char": return tree.children[0].value
        else: raise Exception(f"Unexpected type {type}, tree: {tree}")
    def transform(self, node, expr_type=tuple, group_type=list, text_type=str):
        if isinstance(node, self.Text): return text_type(node.text)
        elif isinstance(node, self.Group): return group_type([self.transform(child, expr_type, group_type, text_type) for child in node.items])
        elif isinstance(node, self.Root): return expr_type([self.transform(child, expr_type, group_type, text_type) for child in node.items])
        else: raise Exception(f"Unexpected node type {type(node)}")
    def root_to_group(self, node):
        if isinstance(node, self.Root): return self.Group(node.items)
        else: return node
    def evaluate_text(self, text, *args, **kwargs): return text
    def evaluate_group(self, items, *args, **kwargs): return items
    def evaluate_root(self, items, *args, **kwargs): return items
    def evaluate(self, node, eval_text=None, eval_group=None, eval_root=None, *args, **kwargs):
        if eval_text is None: eval_text = self.evaluate_text
        if eval_group is None: eval_group = self.evaluate_group
        if eval_root is None: eval_root = self.evaluate_root
        def recurse(node): return self.evaluate(node, eval_text, eval_group, eval_root, *args, **kwargs)
        if isinstance(node, self.Text): return eval_text(node.text, *args, **kwargs)
        elif isinstance(node, self.Group): return eval_group(list(map(recurse, node.items)), *args, **kwargs)
        elif isinstance(node, self.Root): return eval_root(list(map(recurse, node.items)), *args, **kwargs)

