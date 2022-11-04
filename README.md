# brace_lang

Simple language with open and close braces
to use { or }, use \{ or \}.
to use \, use \\.
other backslashes are interpreted as normal backslashes, i.e. \4 is the character '\\' followed by the character '4'.
Open braces are automatically closed when reaching end-of-text.
examples: 
- "Hello {name}!"
- "{attr} of {name}: {name.{attr}.value}"
- "This is an open brace: \\{"
- "Missing close bracket will be automatically inserted: {name"

The language will parse bracket groups which you can then evaluate as you wish.
An example for formating string as suggested in above examples is given in format_string.py:

```python3
class FormatString(BraceLang):
    def evaluate_text(self, text, data): return text
    def evaluate_group(self, items, data): 
        s = "".join(items)
        return get_by_path(data, s, s)
    def evaluate_root(self, items, data): return "".join(map(str,items))
    def format_string(self, string, data): 
        return self.evaluate(self.parse(string), None, None, None, data)

```
