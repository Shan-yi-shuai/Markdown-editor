from file_interpreter import parse_markdown, find_element
import datetime
# 首先需要有一层面对文件的接口，只需要知道文件的存在即可
# 然后中间层是对文件内容的解析，所有解析过的文件应该存储在module里面作为缓存
# 还需要一个文件状态管理器，用来管理文件的打开状态，以及文件的序号
# 最后是面向其他module的接口，比如支持file类型命令的查询等，以及edit类型命令对文件的修改
# 所以其他module能看到的就是file的状态，以及对file的操作
class File:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file_name = file_path.split('/')[-1]
        # list
        self.original_content = self.read_file()
        self.undo_content = None
        self.redo_content = None
        self.current_content = self.original_content[:]
        self.status = 'loaded'
        self.last_status = None
    
    def get_file_content(self):
        return ''.join(self.current_content)
    
    def read_file(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
            return lines
        except FileNotFoundError:
            # 创建一个新文件，并返回空列表
            with open(self.file_path, 'w', encoding='utf-8') as file:
                pass
            return []
        except IOError:
            print(f"Error reading file: {self.file_path}")
            return None
    
    def load_file(self):
        self.status = 'loaded'
        self.current_content = self.read_file()
        self.undo_content = self.original_content[:]
        self.current_content = self.original_content[:]

    def save_file(self):
        try:
            with open(self.file_path, 'w', encoding='utf-8') as file:
                for line in self.current_content:
                    file.write(line)
            self.status = 'saved'
        except IOError:
            print(f"Error writing to file: {self.file_path}")
    
    def close_file(self):
        user_input = input("save changed file before closing? (y/n)")
        if user_input == 'y':
            self.save_file()
        elif user_input == 'n':
            self.status = 'closed'
        else:
            self.close_file()
    
    def insert(self, content, line_number = -1):
        self.last_status = self.status
        self.status = 'modified'
        self.undo_content = self.current_content[:]

        if line_number == -1:
            self.current_content.append(content + '\n')
        else:
            self.current_content.insert(line_number - 1, content + '\n')
    
    def delete_by_line_number(self, line_number):
        self.last_status = self.status
        self.status = 'modified'
        self.undo_content = self.current_content[:]
        self.current_content.pop(line_number - 1)
    
    def delete_by_text(self, text):
        self.last_status = self.status
        self.status = 'modified'
        self.undo_content = self.current_content[:]
        for index, line in enumerate(self.current_content):
            assert len(line.split(" ", 1)) == 2
            if line.split(" ", 1)[1].strip() == text:
                self.current_content.pop(index)
                break
    
    def undo(self):
        if self.undo_content is None:
            print("No undo operation")
            return
        if self.status == 'saved':
            return
        self.last_status = 'undo'
        self.status = self.last_status
        self.redo_content = self.current_content[:]
        self.current_content = self.undo_content[:]
    
    def redo(self):
        if self.last_status != 'undo':
            print("No redo operation")
            return
        self.status = 'modified'
        self.last_status = 'redo'
        self.current_content = self.redo_content[:]
    
# 单例模式
def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance

@singleton
class FileManagement:
    def __init__(self):
        self.files = []
        self.current_file_index = -1
        self.file_work_history = []
        
    def get_current_file_name(self):
        if self.current_file_index == -1:
            return None
        return self.files[self.current_file_index].file_name
    
    def get_current_file_status(self):
        if self.current_file_index == -1:
            return None
        return self.files[self.current_file_index].status
    
    def get_current_file_content(self):
        if self.current_file_index == -1:
            return None
        return self.files[self.current_file_index].get_file_content()

    def load_file(self, file_path):
        for file in self.files:
            if file.file_path == file_path:
                print("file already loaded")
                return
            
        file = File(file_path)
        self.files.append(file)
        self.current_file_index = len(self.files) - 1
        self.add_file_work_history(self.files[self.current_file_index].file_name)
    
    # save之后文件处于可编辑状态
    def save_file(self):
        if self.current_file_index == -1:
            print("no file loaded")
            return
        self.files[self.current_file_index].save_file()
    
    def ws_file(self):
        for index, file in enumerate(self.files):
            content = str(index + 1) + ' ' + file.file_name
            if file.status == 'modified':
                content += '*'
            if index == self.current_file_index:
                content += '<'
            print(content)
    
    def switch_file(self, index):
        if index <= 0 or index > len(self.files):
            print("invalid index")
            return
        self.current_file_index = index - 1
        self.add_file_work_history(self.files[self.current_file_index].file_name)
    
    def close_file(self, index):
        if index <= 0 or index > len(self.files):
            print("invalid index")
            return
        index = index - 1
        self.files[index].close_file()
        if self.current_file_index == index:
            if len(self.files) == 1:
                self.current_file_index = -1
            elif self.current_file_index == len(self.files) - 1:
                self.current_file_index -= 1
        elif self.current_file_index > index:
            self.current_file_index -= 1
        
        self.files.pop(index)
        
        if self.current_file_index == -1:
            self.add_file_work_history()
        else:
            self.add_file_work_history(self.files[self.current_file_index].file_name)
        
    
    def insert(self, content, line_number = -1):
        self.files[self.current_file_index].insert(content, line_number)
    
    # def append_head(self, content):
    #     self.files[self.current_file_index].insert(content, 0)
    
    # def append_tail(self, content):
    #     self.files[self.current_file_index].insert(content)
    
    def delete(self, content = '', line_number = -1):
        if line_number != -1:
            self.files[self.current_file_index].delete_by_line_number(line_number)
        else:
            self.files[self.current_file_index].delete_by_text(content)
        
    def undo(self):
        self.files[self.current_file_index].undo()
    
    def redo(self):
        self.files[self.current_file_index].redo()
    
    def list(self):
        print(self.files[self.current_file_index].get_file_content())
    
    def list_tree(self):
        root = parse_markdown(self.files[self.current_file_index].get_file_content())
        content = root.render()
        print(content)
    
    def dir_tree(self, dir):
        root = parse_markdown(self.files[self.current_file_index].get_file_content())
        element = find_element(root, dir)
        content = element.render(base_level = element.level)
        print(content)
    
    def add_file_work_history(self, file_name = None):
        self.file_work_history.append([file_name, datetime.datetime.now()])
        
    def get_file_work_history(self):
        return self.file_work_history
    
    def refresh(self):
        self.files = []
        self.current_file_index = -1
        self.file_work_history = []
    

# file = File("test.md")
# # file.close_file()
# file.insert("#### test", 3)
# file.delete_by_line_number(1)
# file.show_file()

FileModule = FileManagement()
test = FileManagement()
# FileModule.load_file("test.md")
# FileModule.insert("##### test", 5)
# FileModule.list()
# FileModule.undo()
# FileModule.list()
# FileModule.redo()
# FileModule.list()
# FileModule.ws_file()
# FileModule.close_file()
# FileModule.ws_file()