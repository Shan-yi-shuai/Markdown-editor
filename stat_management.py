import datetime
import atexit

class StatManagement:
    def __init__(self, stat_file_path = 'stat.txt'):
        self.stat_file_path = stat_file_path
        self.stats = {}  # {'file_name': duration}
        self.current_file = None
        self.add_session()
        
        atexit.register(self.close_stat)
        
    def add_session(self):
        try:
            with open(self.stat_file_path, 'a', encoding='utf-8') as file:
                file.write('session start at ' + str(datetime.datetime.now().strftime("%Y%m%d %H:%M:%S")) + '\n')
        except IOError:
            print(f"Error writing to file: {self.stat_file_path}")
    
    def update(self, work_time_history):
        self.stats = {}  # {'file_name': duration}
        self.current_file = None
        last_file_name = None
        last_time = None
        for item in work_time_history:
            current_file_name = item[0]
            current_time = item[1]
            if last_file_name is not None and current_file_name != last_file_name:
                duration = current_time - last_time
                self.stats[last_file_name] = self.stats.get(last_file_name, 0) + int(duration.total_seconds())

            last_file_name = current_file_name
            last_time = current_time
        
        if last_file_name is not None:
            duration = datetime.datetime.now() - last_time
            self.stats[last_file_name] = self.stats.get(last_file_name, 0) + int(duration.total_seconds())
        
        self.current_file = last_file_name
            
    
    def show_stats(self, mode = 'current'):
        if mode == 'current':
            print(f"{self.current_file} {self.format_duration(self.stats[self.current_file])}")
        elif mode == 'all':
            result = []
            for file_name, duration in self.stats.items():
                result.append(f"{file_name} {self.format_duration(duration)}")
            print('\n'.join(result))
        else:
            print('Unknown mode')
    
    def format_duration(self, seconds):
        # 定义时间单位
        minute = 60
        quarter_hour = 15 * minute
        half_hour = 30 * minute
        hour = 60 * minute
        day = 24 * hour

        # 计算每个单位的数量
        days = seconds // day
        seconds %= day
        hours = seconds // hour
        seconds %= hour
        half_hours = seconds // half_hour
        seconds %= half_hour
        quarter_hours = seconds // quarter_hour
        seconds %= quarter_hour
        minutes = seconds // minute
        seconds %= minute

        # 构建输出字符串
        result = []
        if days > 0:
            result.append(f"{days} 天")
        if hours > 0:
            result.append(f"{hours} 小时")
        if half_hours > 0:
            result.append("半小时")
        if quarter_hours > 0:
            result.append("一刻钟")
        if minutes > 0:
            result.append(f"{minutes} 分钟")
        if seconds > 0:
            result.append(f"{seconds} 秒")

        return " ".join(result)

    def close_stat(self):
        try:
            with open(self.stat_file_path, 'a', encoding='utf-8') as file:
                for file_name, duration in self.stats.items():
                    file.write(f"{file_name}: {self.format_duration(duration)}" + '\n')
        except IOError:
            print(f"Error writing to file: {self.stat_file_path}")
