import datetime
import atexit

class LogManagement:
    def __init__(self, log_file_path = 'log.txt'):
        self.log_file_path = log_file_path
        self.logs = self.read_logs()
        self.new_logs = []
        self.add_session()
        
        atexit.register(self.close_log)
    
    def add_session(self):
        try:
            with open(self.log_file_path, 'a', encoding='utf-8') as file:
                file.write('session start at ' + str(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S")) + '\n')
        except IOError:
            print(f"Error writing to file: {self.log_file_path}")
        
    def read_logs(self):
        try:
            with open(self.log_file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
            for line in lines:
                if line.startswith('session start at') or line == '\n':
                    lines.remove(line)
            return lines
        except FileNotFoundError:
            with open(self.log_file_path, 'w', encoding='utf-8') as file:
                pass
            return []
        except IOError:
            print(f"Error reading file: {self.log_file_path}")
            return None
    
    def add_log(self, log):
        text = str(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S")) + ' ' + log
        self.logs.append(text)
        self.new_logs.append(text)

    def show_logs(self, number):
        if number == -1:
            print(''.join(self.logs[:-1]))
        else:
            print(''.join(self.logs[-number - 1:-1]))
    
    def close_log(self):
        try:
            with open(self.log_file_path, 'a', encoding='utf-8') as file:
                for line in self.new_logs:
                    file.write(line + '\n')
        except IOError:
            print(f"Error writing to file: {self.log_file_path}")