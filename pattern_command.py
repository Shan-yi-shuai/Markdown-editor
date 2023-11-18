FILE_COMMAND = "file"
EDIT_COMMAND = "edit"
DISPLAY_COMMAND = "display"

# Command Interface
class Command:
    type = None
    def execute(self):
        pass

# Concrete Command Classes

# load test.md
class LoadCommand(Command):
    Command.type = FILE_COMMAND
    def __init__(self, file_path):
        self.file_path = file_path
    
    def execute(self):
        # Implementation for load command
        pass

# save
class SaveCommand(Command):
    Command.type = FILE_COMMAND
    def __init__(self, file_name):
        self.file_name = file_name
    
    def execute(self):
        # Implementation for load command
        pass
    
    
class InsertCommand(Command):
    def execute(self):
        # Implementation for insert command
        pass

class UndoCommand(Command):
    def execute(self):
        # Implementation for undo command
        pass
