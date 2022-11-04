from brace_lang import BraceLang

def get_by_path(data, path, default_value = {}):
    # get item by path, e.g. "a.b.c.0" -> data["a"]["b"]["c"][0]
    # if the path is empty, return the whole data object
    # it the item or any of its parents does not exist, an empty dict is returned.
    if path == "":
        return data
    elif data is None:
        return default_value
    else:
        # path = unescape_path(path)
        keys = path.split(".") if isinstance(path, str) else [path]
        keys = (filter(lambda x:len(str(x)) > 0, keys))
        keys = list(map(unescape_path, keys))
        cur = data
        for key in keys:
            if isinstance(cur, list) and len(cur) > 0:
                idx = int(key)
                cur = cur[idx % len(cur)]
            elif isinstance(cur, dict) and key in cur:
                cur = cur[key]
            else:
                return default_value
        return cur

def escape_path(path, escaped="\:"):
    if isinstance(path, str):
        return path.replace(".", escaped)
    else:
        return path
def unescape_path(escaped_path, escaped="\:"):
    if isinstance(escaped_path, str):
        return escaped_path.replace(escaped, ".")
    else:
        return escaped_path

class FormatString(BraceLang):
    def evaluate_text(self, text, data): return text
    def evaluate_group(self, items, data): 
        s = "".join(map(str,items))
        return get_by_path(data, s, s)
    def evaluate_root(self, items, data): return "".join(map(str,items))
    def format_string(self, string, data): 
        return self.evaluate(self.parse(string), None, None, None, data)


def main():
    bl = BraceLang()
    tree = bl.parser.parse("Hello {na{m}e}!")
    print(tree.pretty())
    # Outputs the parsed lark tree

    res = bl.parse("Hello {na{m}e}!")
    print(res)
    print(repr(res))
    # Outputs:
    #
    # Hello {na{m}e}!
    # Root([Text('Hello '), Group([Text('na'), Group([Text('m')]), Text('e')]), Text('!')])('Hello ', ['na', ['m'], 'e'], '!')

    print(bl.transform(res))
    print(bl.transform(res,list,tuple))
    print(bl.evaluate(res))
    # Outputs:
    #
    # ('Hello ', ['na', ['m'], 'e'], '!')
    # ['Hello ', ('na', ('m',), 'e'), '!']
    # ['Hello ', ['na', ['m'], 'e'], '!']

    fs = FormatString()
    data = {"name": "John", "attr": "age", "John": {"age": {"value": 20}}}
    print(fs.format_string("Hello {name}! {{name}}", data))
    print(fs.format_string("The {attr} of {name}: {{name}.{attr}.value}", data))
    # Outputs:
    #
    # Hello John! {'age': {'value': 20}}
    # The age of John: 20
if __name__ == "__main__":
    main()
