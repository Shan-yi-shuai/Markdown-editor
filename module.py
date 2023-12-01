from file_management import FileManagement
from log_management import LogManagement
from stat_management import StatManagement
from processor import FileCommandProcessor, EditorCommandProcessor, DisplayCommandProcessor, LogCommandProcessor, StatCommandProcessor
from command import CommandFactory, FILE_COMMAND, EDIT_COMMAND, DISPLAY_COMMAND, LOG_COMMAND, STAT_COMMAND

# Observer Interface
class Observer:
    def update(self):
        pass

# Subject Interface
class Subject:
    def attach(self, observer):
        pass

    def detach(self, observer):
        pass

    def notify(self):
        pass

# 负责通知而不需要知道command的具体实现
class CommandIdentifier(Subject):
    def __init__(self):
        self.module_list = []

    def process_command(self, command_string):
        parts = command_string.strip().split()
        command_name = parts[0]
        # args = parts[1:]
        
        self.notify(command_name, command_string)
    
    def attach(self, observer):
        self.module_list.append(observer)

    def detach(self, observer):
        self.module_list.remove(observer)

    def notify(self, command_name, command_string):
        for observer in self.module_list:
            command = observer.update(command_name, command_string)
            if command != None:
                command.execute()

class CoreModule(Observer):
    def __init__(self) -> None:
        self.file_management = FileManagement()
        self.file_command_processor = FileCommandProcessor(self.file_management)
        self.editor_command_processor = EditorCommandProcessor(self.file_management)
        self.display_command_processor = DisplayCommandProcessor(self.file_management)
        
    def update(self, command_name, command_string):
        return CommandFactory().create_command({FILE_COMMAND: self.file_command_processor, EDIT_COMMAND: self.editor_command_processor, DISPLAY_COMMAND: self.display_command_processor}, command_name, command_string)

class LogModule(Observer):
    def __init__(self) -> None:
        self.log_management = LogManagement()
        self.log_command_processor = LogCommandProcessor(self.log_management)
        
    def update(self, command_name, command_string):
        self.log_management.add_log(command_string.strip())
        return CommandFactory().create_command({LOG_COMMAND: self.log_command_processor}, command_name, command_string)

class StatModule(Observer):
    def __init__(self) -> None:
        self.file_management = FileManagement()
        self.stat_management = StatManagement()
        self.stat_command_processor = StatCommandProcessor(self.stat_management, self.file_management)
    
    def update(self, command_name, command_string):
        return CommandFactory().create_command({STAT_COMMAND: self.stat_command_processor}, command_name, command_string)

