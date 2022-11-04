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
