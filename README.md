# brace_lang
A simple language with {open and close} braces. You can parse brace groups and evaluate them however you want.

Examples: 
- "Hello {name}!"
- "{attr} of {name}: {name.{attr}.value}"
- "This is an open brace: \\{"
- "Missing close brace will be automatically inserted: {name"

An example for formating string as suggested in above examples is given in format_string.py:

```python3
from brace_lang import BraceLang
def get_by_path(data,path,default_value): ...
class FormatString(BraceLang):
    def evaluate_text(self, text, data): 
        return text
    def evaluate_group(self, items, data): 
        s = "".join(items)
        return get_by_path(data, s, s)
    def evaluate_root(self, items, data): 
        return "".join(map(str,items))
    def format_string(self, string, data): 
        return self.evaluate(self.parse(string), None, None, None, data)


fs = FormatString()
data = {"name": "John", "attr": "age", "John": {"age": {"value": 20}}}
print(fs.format_string("Hello {name}! {{name}}", data))
print(fs.format_string("The {attr} of {name}: {{name}.{attr}.value}", data))
# Outputs:
# Hello John! {'age': {'value': 20}}
# The age of John: 20
```
## Installation:
Clone the repo, cd into it and `pip install .` it.

## Notes:
To use { or }, use \\{ or \\}.
To use \\, use \\\\.
Other backslashes are ignored, i.e. \4 will be interpreted as the character '4'.
Open braces are automatically closed when reaching end-of-text.


