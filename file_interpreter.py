# 根结点
ROOT = 'root'
# 如果同一层有多个并列项，则最后一个符号为└──，其余均为├──
L_SHAPED_DASH = '└── '
T_SHAPED_DASH = '├── '
I_SHAPED_DASH = '│   '
SPACE = '    '


class MarkDownInterpreter:
    def interpret(self, text):
        raise NotImplementedError

class MarkdownElement:
    def render(self):
        raise NotImplementedError
    
class RootElement(MarkdownElement):
    def __init__(self):
        self.children = []
        self.list = []
        self.text = None
        self.level = 0
    
    def add(self, item):
        self.children.append(item)
    
    def add_list(self, list_element):
        self.list.append(list_element)
    
    def render(self):
        content = ''
        level_list = [False]
        # list一定是叶子节点，所以如果出现则一定在header之前
        for index, list_element in enumerate(self.list):
            content += list_element.render(level = 0, base_level = 1, level_list = level_list)
        for index, item in enumerate(self.children):
            content += item.render(base_level = 1, tail = index == (len(self.children) - 1), level_list = level_list + [ index + 1 < len(self.children) ])
        
        return content

class HeaderElement(MarkdownElement):
    def __init__(self, level, text):
        self.level = level
        self.text = text
        self.children = []
        self.list = []
        self.successor = None
    
    def add(self, item):
        self.children.append(item)
    
    def add_list(self, list_element):
        self.list.append(list_element)
    
    def set_successor(self, successor):
        self.successor = successor;

    def render(self, base_level = 1, tail = True, level_list = [False, False]):
        # content = SPACE * (self.level - base_level)
        content = ''
        for i in range(1, self.level - base_level + 1):
            if level_list[i]:
                content += I_SHAPED_DASH
            else:
                content += SPACE
        
        if tail:
            content += L_SHAPED_DASH + self.text + '\n'
        else:
            content += T_SHAPED_DASH + self.text + '\n'
        
        for index, list_element in enumerate(self.list):
            content += list_element.render(level = self.level, base_level = base_level, level_list = level_list)
        for index, item in enumerate(self.children):
            content += item.render(base_level = base_level, tail = index == (len(self.children) - 1), level_list = level_list + [ index + 1 < len(self.children) ])
        
        return content

class UnorderedElement(MarkdownElement):
    def __init__(self, text):
        self.text = text
        self.successor = None
    
    def set_successor(self, successor):
        self.successor = successor;

    def render(self, level, base_level = 1,  tail = True, level_list = [False, False]):
        # content = SPACE * (level - base_level + 1)
        content = ''
        for i in range(1, level - base_level + 2):
            if level_list[i]:
                content += I_SHAPED_DASH
            else:
                content += SPACE
        
        if tail:
            content += L_SHAPED_DASH
        else:
            content += T_SHAPED_DASH
        return content + '·' + self.text + '\n'

class OrderedElement(MarkdownElement):    
    def __init__(self, text, index):
        self.text = text
        self.index = index
        self.successor = None
        
    def set_successor(self, successor):
        self.successor = successor;

    def render(self, level, base_level = 1,  tail = True, level_list = [False, False]):
        # content = SPACE * (level - base_level + 1)
        content = ''
        for i in range(1, level - base_level + 2):
            if level_list[i]:
                content += I_SHAPED_DASH
            else:
                content += SPACE
        
        if tail:
            content += L_SHAPED_DASH
        else:
            content += T_SHAPED_DASH
        return content + str(self.index) + '. ' + self.text + '\n'

class UnorderedListElement(MarkdownElement):
    def __init__(self):
        self.items = []
        self.successor = None

    def add_item(self, item):
        self.items.append(item)
    
    def set_successor(self, successor):
        self.successor = successor;

    def render(self, level, base_level = 1, level_list = [False, False]):
        content = ''
        for index, item in enumerate(self.items):
            content += item.render(level = level, base_level = base_level, tail = index == len(self.items) - 1, level_list = level_list)
        return content

class OrderedListElement(MarkdownElement):
    def __init__(self):
        self.items = []
        self.successor = None

    def add_item(self, item):
        self.items.append(item)
    
    def set_successor(self, successor):
        self.successor = successor;

    def render(self, level, base_level = 1, level_list = [False, False]):
        content = ''
        for index, item in enumerate(self.items):
            content += item.render(level = level, base_level = base_level, tail = index == len(self.items) - 1, level_list = level_list)
        return content
    
class RootInterpreter(MarkDownInterpreter):
    def interpret(self, text = '', successor_element = None):
        return RootElement()

class HeaderInterpreter(MarkDownInterpreter):
    def interpret(self, text, successor_element):
        level = 0
        for char in text:
            if char == '#':
                level += 1
            else:
                break
        header_content = text[level:].strip()
        header_element = HeaderElement(level, header_content)
        
        # assert isinstance(successor_element, RootElement) or isinstance(successor_element, HeaderElement)
        while not(isinstance(successor_element, RootElement) or isinstance(successor_element, HeaderElement)):
            successor_element = successor_element.successor
        if (header_element.level > successor_element.level):
            successor_element.add(header_element)
            header_element.set_successor(successor_element)
        else:
            while header_element.level <= successor_element.level:
                successor_element = successor_element.successor
            successor_element.add(header_element)
            header_element.set_successor(successor_element.successor)
                
        return header_element

class UnorderedListInterpreter(MarkDownInterpreter):
    def interpret(self, text, successor_element):
        element = UnorderedElement(text.strip('* ').strip())
        if isinstance(successor_element, UnorderedListElement):
            element.set_successor(successor_element)
            successor_element.add_item(element)
            return successor_element
        elif isinstance(successor_element, OrderedListElement):
            successor_element = successor_element.successor
            list_element = UnorderedListElement()
            list_element.set_successor(successor_element)
            successor_element.add_list(list_element)
            list_element.add_item(element)
            return list_element
        else:
            list_element = UnorderedListElement()
            list_element.set_successor(successor_element)
            successor_element.add_list(list_element)
            list_element.add_item(element)
            return list_element

class OrderedListInterpreter(MarkDownInterpreter):
    def interpret(self, text, successor_element):
        element = OrderedElement(text.split('.')[1].strip(), text.split('.')[0].strip())
        if isinstance(successor_element, OrderedListElement):
            element.set_successor(successor_element)
            successor_element.add_item(element)
            return successor_element
        elif isinstance(successor_element, UnorderedListElement):
            successor_element = successor_element.successor
            list_element = OrderedListElement()
            list_element.set_successor(successor_element)
            successor_element.add_list(list_element)
            list_element.add_item(element)
            return list_element
        else:
            list_element = OrderedListElement()
            list_element.set_successor(successor_element)
            list_element.add_item(element)
            successor_element.add_list(list_element)
            return list_element

class InterpreterFactory:
    @staticmethod
    def get_interpreter(text):
        if text == '':
            return None
        elif text == ROOT:
            return RootInterpreter()
        elif text.startswith(('#')):
            return HeaderInterpreter()
        elif any(text.lstrip().startswith(mark) for mark in ('*', '-', '+')):
            return UnorderedListInterpreter()
        elif text.lstrip()[0].isdigit() and '.' in text:
            return OrderedListInterpreter()
        else:
            return None

def parse_markdown(text):
    root = None
    successor_element = None
    interpreter = InterpreterFactory.get_interpreter(ROOT)
    root = interpreter.interpret(ROOT, successor_element)
    successor_element = root

    for line in text.split('\n')[:-1]:
        interpreter = InterpreterFactory.get_interpreter(line)
        if interpreter:
            successor_element = interpreter.interpret(line, successor_element)
        else:
            raise Exception(f"Unknown markdown syntax: {line}")
    return root

def find_element(root, content):
    if root.text == content:
        return root
    else:
        for child in root.children:
            result = find_element(child, content)
            if result:
                return result
        return None

