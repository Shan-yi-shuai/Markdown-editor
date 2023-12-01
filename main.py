from module import CoreModule, LogModule, StatModule, CommandIdentifier 

def get_command_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        return lines

def main():
    core_module = CoreModule()
    log_module = LogModule()
    stat_module = StatModule()
    
    command_identifier = CommandIdentifier()
    command_identifier.attach(core_module)
    command_identifier.attach(log_module)
    command_identifier.attach(stat_module)
    
    while True:
        command_string = input("> ")
        command_identifier.process_command(command_string)
    # command_list = get_command_text('test5.txt')
    # for command in command_list:
    #     print(command)
    #     command_identifier.process_command(command)
    
if __name__ == '__main__':
    main()