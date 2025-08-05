import language_tool_python

class GrammarCheck:
    def __init__(self, text=None, filepath=None):
        self.text = text
        self.file = filepath
        self.tool = language_tool_python.LanguageTool('en-US')

    def check(self):
        error = []
        if self.text:
            text = self.text

        elif self.file:
            with open(self.file, "r", encoding="utf-8") as f:
                text = f.read()

        else:
            raise TypeError("There's no text or file.")
        
        matches = self.tool.check(text)

        return [{
            "message": match.message,
            "replacements": match.replacements,
            "offset": match.offset,
            "context": match.context
                } for match in matches]

