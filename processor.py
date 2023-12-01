class Processor():
    pass

class FileCommandProcessor(Processor):
    def __init__(self, file_management):
        self.file_management = file_management
    
    def load_file(self, file_path):
        self.file_management.load_file(file_path)
    
    def save_file(self):
        self.file_management.save_file()
        
    def ws_file(self):
        self.file_management.ws_file()
    
    def switch_file(self, index):
        self.file_management.switch_file(index)
    
    def close_file(self, index):
        self.file_management.close_file(index)
    

class EditorCommandProcessor(Processor):
    def __init__(self, file_management):
        self.file_management = file_management
    
    def insert(self, content, line_number = -1):
        self.file_management.insert(content, line_number)
    
    def append_head(self, content):
        self.file_management.insert(content, 0)
    
    def append_tail(self, content):
        self.file_management.insert(content)
    
    def delete(self, content = '', line_number = -1):
        self.file_management.delete(content, line_number)
    
    def undo(self):
        self.file_management.undo()
    
    def redo(self):
        self.file_management.redo()

class DisplayCommandProcessor(Processor):
    def __init__(self, file_management):
        self.file_management = file_management
    
    def list(self):
        self.file_management.list()
    
    def list_tree(self):
        self.file_management.list_tree()
    
    def dir_tree(self, dir):
        self.file_management.dir_tree(dir)

class LogCommandProcessor(Processor):
    def __init__(self, log_management):
        self.log_management = log_management
    
    def history(self, number):
        self.log_management.show_logs(number)
        
class StatCommandProcessor(Processor):
    def __init__(self, stat_management, file_management):
        self.stat_management = stat_management
        self.file_management = file_management
    
    def stats(self, mode = 'current'):
        self.stat_management.update(self.file_management.get_file_work_history())
        self.stat_management.show_stats(mode)