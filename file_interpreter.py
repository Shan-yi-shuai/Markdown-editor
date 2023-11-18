class MarkDownInterpreter:
    def interpret(self, text):
        raise NotImplementedError

class MarkdownElement:
    def render(self):
        raise NotImplementedError

class HeaderElement(MarkdownElement):
    def __init__(self, level, text):
        self.level = level
        self.text = text

    def render(self):
        return f"<h{self.level}>{self.text}</h{self.level}>"

class UnorderedElement(MarkdownElement):
    def __init__(self, text):
        self.text = text

    def render(self):
        return f"<li>{self.text}</li>"

def OrderedElement(MarkdownElement):    
    def __init__(self, text, index):
        self.text = text
        self.index = index

    def render(self):
        return f"<li>{self.text}</li>"

class UnorderedListElement(MarkdownElement):
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def render(self):
        list_items_html = ''.join(f"<li>{item}</li>" for item in self.items)
        return f"<ul>{list_items_html}</ul>"

class OrderedListElement(MarkdownElement):
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def render(self):
        list_items_html = ''.join(f"<li>{item}</li>" for item in self.items)
        return f"<ol>{list_items_html}</ol>"

class HeaderInterpreter(MarkDownInterpreter):
    def interpret(self, text):
        level = text.count('#')
        header_content = text.strip('# ').strip()
        return HeaderElement(level, header_content)

class UnorderedListInterpreter(MarkDownInterpreter):
    def interpret(self, text):
        list_element = UnorderedListElement()
        for line in text.splitlines():
            list_item = line.strip('* ').strip()
            list_element.add_item(list_item)
        return list_element

class OrderedListInterpreter(MarkDownInterpreter):
    def interpret(self, text):
        list_element = OrderedListElement()
        for line in text.splitlines():
            list_item = line.split('.')[1].strip()
            list_element.add_item(list_item)
        return list_element


class InterpreterFactory:
    @staticmethod
    def get_interpreter(text):
        if text.startswith('#'):
            return HeaderInterpreter()
        elif text.startswith(('*', '-', '+')):
            # todo
            return UnorderedListInterpreter()
        elif text.startswith('1.'):
            # todo
            return OrderedListInterpreter()
        else:
            return None
