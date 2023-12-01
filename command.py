FILE_COMMAND = "file"
EDIT_COMMAND = "edit"
DISPLAY_COMMAND = "display"
LOG_COMMAND = "log"
STAT_COMMAND = "stat"

# 识别command
class CommandFactory:
    def create_command(self, processors, command_name, command_string):
        if command_name == "load":
            if processors.get(FILE_COMMAND) == None:
                return None
            if len(command_string.split()) != 2:
                print("Invalid command")
                return None
            return LoadCommand(processors[FILE_COMMAND], command_string.split(" ", 1)[1].strip())
        elif command_name == "save":
            if processors.get(FILE_COMMAND) == None:
                return None
            if len(command_string.split()) != 1:
                print("Invalid command")
                return None
            return SaveCommand(processors[FILE_COMMAND])
        elif command_name == "ws":
            if processors.get(FILE_COMMAND) == None:
                return None
            if len(command_string.split()) != 1:
                print("Invalid command")
                return None
            return WSCommand(processors[FILE_COMMAND])
        elif command_name == "switch":
            if processors.get(FILE_COMMAND) == None:
                return None
            if len(command_string.split()) != 2 or not command_string.split()[1].strip().isdigit():
                print("Invalid command")
                return None
            return SwitchCommand(processors[FILE_COMMAND], int(command_string.split()[1].strip()))
        elif command_name == "close":
            if processors.get(FILE_COMMAND) == None:
                return None
            if len(command_string.split()) != 2 or not command_string.split()[1].strip().isdigit():
                print("Invalid command")
                return None
            return CloseCommand(processors[FILE_COMMAND], int(command_string.split()[1].strip()))
        elif command_name == "insert":
            if processors.get(EDIT_COMMAND) == None:
                return None
            if len(command_string.split()) < 2:
                print("Invalid command")
                return None
            if command_string.split()[1].strip().isdigit():
                if len(command_string.split()) == 2:
                    print("Invalid command")
                    return None
                else:
                    return InsertCommand(processors[EDIT_COMMAND], command_string.split(" ", 2)[2].strip(), int(command_string.split()[1].strip()))
            else:
                return InsertCommand(processors[EDIT_COMMAND], command_string.split(" ", 1)[1].strip())
        elif command_name == "append-head":
            if processors.get(EDIT_COMMAND) == None:
                return None
            if len(command_string.split()) < 2:
                print("Invalid command")
                return None
            return AppendHeadCommand(processors[EDIT_COMMAND], command_string.split(" ", 1)[1].strip())
        elif command_name == "append-tail":
            if processors.get(EDIT_COMMAND) == None:
                return None
            if len(command_string.split()) < 2:
                print("Invalid command")
                return None
            return AppendTailCommand(processors[EDIT_COMMAND], command_string.split(" ", 1)[1].strip())
        elif command_name == "delete":
            if processors.get(EDIT_COMMAND) == None:
                return None
            if len(command_string.split()) < 2:
                print("Invalid command")
                return None
            if command_string.split()[1].strip().isdigit():
                return DeleteCommand(processors[EDIT_COMMAND], "", int(command_string.split()[1].strip()))
            else:
                return DeleteCommand(processors[EDIT_COMMAND], command_string.split(" ", 1)[1].strip())
        elif command_name == "undo":
            if processors.get(EDIT_COMMAND) == None:
                return None
            if len(command_string.split()) != 1:
                print("Invalid command")
                return None
            return UndoCommand(processors[EDIT_COMMAND])
        elif command_name == "redo":
            if processors.get(EDIT_COMMAND) == None:
                return None
            if len(command_string.split()) != 1:
                print("Invalid command")
                return None
            return RedoCommand(processors[EDIT_COMMAND])
        elif command_name == "list":
            if processors.get(DISPLAY_COMMAND) == None:
                return None
            if len(command_string.split()) != 1:
                print("Invalid command")
                return None
            return ListCommand(processors[DISPLAY_COMMAND])
        elif command_name == "list-tree":
            if processors.get(DISPLAY_COMMAND) == None:
                return None
            if len(command_string.split()) != 1:
                print("Invalid command")
                return None
            return ListTreeCommand(processors[DISPLAY_COMMAND])
        elif command_name == "dir-tree":
            if processors.get(DISPLAY_COMMAND) == None:
                return None
            if len(command_string.split()) == 1:
                return ListTreeCommand(processors[DISPLAY_COMMAND])
            if len(command_string.split()) != 2:
                print("Invalid command")
                return None
            return DirTreeCommand(processors[DISPLAY_COMMAND], command_string.split(" ", 1)[1].strip())
        elif command_name == "history":
            if processors.get(LOG_COMMAND) == None:
                return None
            if len(command_string.split()) == 1:
                return HistoryCommand(processors[LOG_COMMAND])
            elif len(command_string.split()) == 2 and command_string.split()[1].strip().isdigit():
                return HistoryCommand(processors[LOG_COMMAND], int(command_string.split()[1].strip()))
            else:
                print("Invalid command")
                return None
        elif command_name == "stats":
            if processors.get(STAT_COMMAND) is None:
                return None
            if len(command_string.split()) == 1:
                return StatsCommand(processors[STAT_COMMAND])
            elif len(command_string.split()) == 2 and command_string.split()[1].strip() in ['all', 'current']:
                return StatsCommand(processors[STAT_COMMAND], command_string.split()[1].strip())
            else:
                print("Invalid command")
                return None
        else:
            raise ValueError("Unknown command type")


# Command Interface
class Command:
    def execute(self):
        pass
    
    
# load 文件路径
class LoadCommand(Command):
    def __init__(self, processor, file_path):
        self.type = FILE_COMMAND
        self.file_path = file_path
        self.processor = processor
    
    def execute(self):
        self.processor.load_file(self.file_path)

# save
class SaveCommand(Command):
    def __init__(self, processor):
        self.type = FILE_COMMAND
        self.processor = processor
    
    def execute(self):
        self.processor.save_file()

# ws
class WSCommand(Command):
    Command.type = FILE_COMMAND
    def __init__(self, processor):
        self.processor = processor
    
    def execute(self):
        self.processor.ws_file()

# switch 文件序号
class SwitchCommand(Command):
    def __init__(self, processor, file_index):
        self.type = FILE_COMMAND
        self.file_index = file_index
        self.processor = processor
    
    def execute(self):
        self.processor.switch_file(self.file_index)

# close 文件序号
class CloseCommand(Command):
    def __init__(self, processor, file_index):
        self.type = FILE_COMMAND
        self.file_index = file_index
        self.processor = processor
    
    def execute(self):
        self.processor.close_file(self.file_index)

# insert [⾏号] 标题/文本
class InsertCommand(Command):
    def __init__(self, processor, text, line_number = -1):
        self.type = EDIT_COMMAND
        self.processor = processor
        self.text = text
        self.line_number = line_number
        
    def execute(self):
        self.processor.insert(self.text, self.line_number)
    
    
# append-head 标题/文本
class AppendHeadCommand(Command):
    def __init__(self, processor, text):
        self.type = EDIT_COMMAND
        self.processor = processor
        self.text = text
        
    def execute(self):
        self.processor.append_head(self.text)


# append-tail 标题/文本
class AppendTailCommand(Command):
    def __init__(self, processor, text):
        self.type = EDIT_COMMAND
        self.processor = processor
        self.text = text
        
    def execute(self):
        self.processor.append_tail(self.text)


# delete 标题/文本 或delete ⾏号
class DeleteCommand(Command):
    def __init__(self, processor, text = "", line_number = -1):
        self.type = EDIT_COMMAND
        self.processor = processor
        self.text = text
        self.line_number = line_number
        
    def execute(self):
        self.processor.delete(self.text, self.line_number)

    
# undo
# 因为任何FILE_COMMAND都会导致undo指令被忽略，所以撤销的一定是当前文件的编辑操作，所以不需要考虑撤销错文件的情况
# 而且对于其他指令，FILE都是看不到的，所以自然可以跳过
class UndoCommand(Command):
    def __init__(self, processor):
        self.type = EDIT_COMMAND
        self.processor = processor
    
    def execute(self):
        self.processor.undo()

# redo
class RedoCommand(Command):
    def __init__(self, processor):
        self.type = EDIT_COMMAND
        self.processor = processor
    
    def execute(self):
        self.processor.redo()

# list
class ListCommand(Command):
    def __init__(self, processor):
        self.type = DISPLAY_COMMAND
        self.processor = processor
    
    def execute(self):
        self.processor.list()

# list-tree
class ListTreeCommand(Command):
    def __init__(self, processor):
        self.type = DISPLAY_COMMAND
        self.processor = processor
    
    def execute(self):
        self.processor.list_tree()

# dir-tree [⽬录]
class DirTreeCommand(Command):
    def __init__(self, processor, dir_path):
        self.type = DISPLAY_COMMAND
        self.processor = processor
        self.dir_path = dir_path
    
    def execute(self):
        self.processor.dir_tree(self.dir_path)

# history [数量]c
class HistoryCommand(Command):
    def __init__(self, processor, count = -1):
        self.type = LOG_COMMAND
        self.processor = processor
        self.count = count
    
    def execute(self):
        self.processor.history(self.count)

# stats [all | current]
class StatsCommand(Command):
    def __init__(self, processor, stats_mode = 'current'):
        self.type = STAT_COMMAND
        self.processor = processor
        self.stats_mode = stats_mode
    
    def execute(self):
        self.processor.stats(self.stats_mode)