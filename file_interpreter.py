# Strategy Interface
class MarkdownParserStrategy:
    def parse(self, text):
        pass

# Concrete Strategy Classes
class HeaderParser(MarkdownParserStrategy):
    def parse(self, text):
        # Implementation for header parsing
        pass

class ListParser(MarkdownParserStrategy):
    def parse(self, text):
        # Implementation for list parsing
        pass
