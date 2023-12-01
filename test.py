import unittest
from unittest.mock import Mock, patch
from module import CoreModule, LogModule, StatModule, CommandIdentifier
from io import StringIO
import os
import time


class TestCommands(unittest.TestCase):

    def setUp(self):
        self.core_module = CoreModule()
        self.log_module = LogModule()
        self.stat_module = StatModule()
        self.command_identifier = CommandIdentifier()
        self.command_identifier.attach(self.core_module)
        self.command_identifier.attach(self.log_module)
        self.command_identifier.attach(self.stat_module)
        self.exit_file = 'test.md'
        self.not_exit_file = '_test.md'
        self.insert_content = '# Header1'

    def tearDown(self):
        self.core_module.file_management.refresh()
        if os.path.exists(self.not_exit_file):
            os.remove(self.not_exit_file)
        self.log_module.log_management.close_log()
        self.stat_module.stat_management.close_stat()
        # time.sleep(0.1)

    # 1-1
    def test_load_command_exit(self):
        self.command_identifier.process_command(f"load {self.exit_file}")
        self.assertEqual(
            self.core_module.file_management.get_current_file_name(), self.exit_file)

    # 1-2
    def test_load_command_not_exit(self):
        self.command_identifier.process_command(f"load {self.not_exit_file}")
        self.assertEqual(
            self.core_module.file_management.get_current_file_name(), self.not_exit_file)

    # 1-3
    def test_load_command_switch(self):
        self.command_identifier.process_command(f"load {self.exit_file}")
        self.command_identifier.process_command(f"load {self.not_exit_file}")
        self.assertEqual(
            self.core_module.file_management.get_current_file_name(), self.not_exit_file)

    # 1-4
    @patch('sys.stdout', new_callable=StringIO)
    def test_load_command_duplicate(self, mock_stdout):
        self.command_identifier.process_command(f"load {self.exit_file}")
        self.command_identifier.process_command(f"load {self.exit_file}")
        self.assertEqual(
            self.core_module.file_management.get_current_file_name(), self.exit_file)
        self.assertEqual(mock_stdout.getvalue().strip(), "file already loaded")

    # 2-1
    def test_save_command_exit(self):
        self.command_identifier.process_command(f"load {self.exit_file}")
        self.command_identifier.process_command("save")
        self.assertEqual(
            self.core_module.file_management.get_current_file_status(), "saved")

    # 2-2
    @patch('sys.stdout', new_callable=StringIO)
    def test_save_command_not_exit(self, mock_stdout):
        self.command_identifier.process_command("save")
        self.assertEqual(mock_stdout.getvalue().strip(), "no file loaded")

    # 3-1
    @patch('sys.stdout', new_callable=StringIO)
    def test_ws_command(self, mock_stdout):
        self.command_identifier.process_command(f"load {self.exit_file}")
        self.command_identifier.process_command(f"load {self.not_exit_file}")
        self.command_identifier.process_command(
            f"append-head {self.insert_content}")
        self.command_identifier.process_command("ws")
        self.assertEqual(mock_stdout.getvalue().strip(),
                         f"1 {self.exit_file}\n2 {self.not_exit_file}*<")

    # 4-1
    @patch('sys.stdout', new_callable=StringIO)
    def test_switch_command_exit(self, mock_stdout):
        self.command_identifier.process_command(f"load {self.exit_file}")
        self.command_identifier.process_command(f"load {self.not_exit_file}")
        self.command_identifier.process_command("switch 1")
        self.command_identifier.process_command("ws")
        self.assertEqual(mock_stdout.getvalue().strip(),
                         f"1 {self.exit_file}<\n2 {self.not_exit_file}")

    # 4-2
    @patch('sys.stdout', new_callable=StringIO)
    def test_switch_command_not_exit(self, mock_stdout):
        self.command_identifier.process_command(f"load {self.exit_file}")
        self.command_identifier.process_command(f"load {self.not_exit_file}")
        self.command_identifier.process_command("switch 3")
        self.assertEqual(mock_stdout.getvalue().strip(), "invalid index")

    # 5-1
    @patch('builtins.input', return_value='y')
    def test_close_command_exit_save(self, mock_input):
        self.command_identifier.process_command(f"load {self.exit_file}")
        self.command_identifier.process_command(f"load {self.not_exit_file}")
        self.command_identifier.process_command(
            f"append-head {self.insert_content}")
        self.command_identifier.process_command("close 2")
        self.assertEqual(
            self.core_module.file_management.get_current_file_name(), self.exit_file)
        self.command_identifier.process_command(f"load {self.not_exit_file}")
        self.assertEqual(self.core_module.file_management.get_current_file_content(
        ), self.insert_content + '\n')

    # 5-2
    @patch('builtins.input', return_value='n')
    def test_close_command_exit_not_save(self, mock_input):
        self.command_identifier.process_command(f"load {self.exit_file}")
        self.command_identifier.process_command(f"load {self.not_exit_file}")
        self.command_identifier.process_command(
            f"append-head {self.insert_content}")
        self.command_identifier.process_command("close 2")
        self.assertEqual(
            self.core_module.file_management.get_current_file_name(), self.exit_file)
        self.command_identifier.process_command(f"load {self.not_exit_file}")
        self.assertEqual(
            self.core_module.file_management.get_current_file_content(), '')

    # 5-3
    @patch('sys.stdout', new_callable=StringIO)
    def test_close_command_not_exit(self, mock_stdout):
        self.command_identifier.process_command(f"load {self.exit_file}")
        self.command_identifier.process_command("close 2")
        self.assertEqual(mock_stdout.getvalue().strip(), "invalid index")

    # 6-1
    def test_insert_command_with_line_number(self):
        self.command_identifier.process_command(f"load {self.not_exit_file}")
        self.command_identifier.process_command(
            f"insert 1 {self.insert_content}")
        self.assertEqual(self.core_module.file_management.get_current_file_content(
        ), self.insert_content + '\n')

    # 6-2
    def test_insert_command_without_line_number(self):
        self.command_identifier.process_command(f"load {self.not_exit_file}")
        self.command_identifier.process_command(
            f"insert {self.insert_content}")
        self.assertEqual(self.core_module.file_management.get_current_file_content(
        ), self.insert_content + '\n')

    # 7-1
    def test_append_head_command(self):
        self.command_identifier.process_command(f"load {self.not_exit_file}")
        self.command_identifier.process_command(
            f"append-head {self.insert_content}")
        self.assertEqual(self.core_module.file_management.get_current_file_content(
        ), self.insert_content + '\n')

    # 8-1
    def test_append_tail_command(self):
        self.command_identifier.process_command(f"load {self.not_exit_file}")
        self.command_identifier.process_command(
            f"append-tail {self.insert_content}")
        self.assertEqual(self.core_module.file_management.get_current_file_content(
        ), self.insert_content + '\n')

    # 9-1
    def test_delete_command_with_text(self):
        self.command_identifier.process_command(f"load {self.not_exit_file}")
        self.command_identifier.process_command(
            f"append-head {self.insert_content}")
        self.command_identifier.process_command(f"delete Header1")
        self.assertEqual(
            self.core_module.file_management.get_current_file_content(), '')

    # 9-2
    def test_delete_command_with_line_number(self):
        self.command_identifier.process_command(f"load {self.not_exit_file}")
        self.command_identifier.process_command(
            f"append-head {self.insert_content}")
        self.command_identifier.process_command(f"delete 1")
        self.assertEqual(
            self.core_module.file_management.get_current_file_content(), '')

    # 10-1
    def test_undo_command_edit(self):
        self.command_identifier.process_command(f"load {self.not_exit_file}")
        self.command_identifier.process_command(
            f"append-head {self.insert_content}")
        self.command_identifier.process_command(f"undo")
        self.assertEqual(
            self.core_module.file_management.get_current_file_content(), '')

    # 10-2
    def test_undo_command_file(self):
        self.command_identifier.process_command(f"load {self.not_exit_file}")
        self.command_identifier.process_command(
            f"append-head {self.insert_content}")
        self.command_identifier.process_command(f"save")
        self.command_identifier.process_command(f"undo")
        self.assertEqual(self.core_module.file_management.get_current_file_content(
        ), self.insert_content + '\n')

    # 10-3
    def test_undo_command_display(self):
        self.command_identifier.process_command(f"load {self.not_exit_file}")
        self.command_identifier.process_command(
            f"append-head {self.insert_content}")
        self.command_identifier.process_command(f"undo")
        self.assertEqual(
            self.core_module.file_management.get_current_file_content(), '')

    # 11-1
    def test_redo_command_undo(self):
        self.command_identifier.process_command(f"load {self.not_exit_file}")
        self.command_identifier.process_command(
            f"append-head {self.insert_content}")
        self.command_identifier.process_command(f"undo")
        self.command_identifier.process_command(f"redo")
        self.assertEqual(self.core_module.file_management.get_current_file_content(
        ), self.insert_content + '\n')

    # 11-2
    @patch('sys.stdout', new_callable=StringIO)
    def test_redo_command_not_undo(self, mock_stdout):
        self.command_identifier.process_command(f"load {self.not_exit_file}")
        self.command_identifier.process_command(
            f"append-head {self.insert_content}")
        self.command_identifier.process_command(f"redo")
        self.assertEqual(mock_stdout.getvalue().strip(), "No redo operation")

    # 12-1
    @patch('sys.stdout', new_callable=StringIO)
    def test_list_command(self, mock_stdout):
        self.command_identifier.process_command(f"load {self.not_exit_file}")
        self.command_identifier.process_command(
            f"append-head {self.insert_content}")
        self.command_identifier.process_command(f"list")
        self.assertEqual(mock_stdout.getvalue().strip(), self.insert_content)
    
    # 13-1
    @patch('sys.stdout', new_callable=StringIO)
    def test_list_tree_command(self, mock_stdout):
        tree ="""└── 我的资源
    ├── 程序设计
    │   └── 软件设计
    │       └── 设计模式
    │           ├── 1. 观察者模式
    │           ├── 2. 策略模式
    │           └── 3. 组合模式
    └── ⼯具箱
        └── Adobe"""
        self.command_identifier.process_command(f"load {self.exit_file}")
        self.command_identifier.process_command(f"list-tree")
        self.assertEqual(mock_stdout.getvalue().strip(), tree)
    
    # 14-1
    @patch('sys.stdout', new_callable=StringIO)
    def test_dir_tree_command_with_dir(self, mock_stdout):
        tree ="""└── 程序设计
    └── 软件设计
        └── 设计模式
            ├── 1. 观察者模式
            ├── 2. 策略模式
            └── 3. 组合模式"""
        self.command_identifier.process_command(f"load {self.exit_file}")
        self.command_identifier.process_command(f"dir-tree 程序设计")
        self.assertEqual(mock_stdout.getvalue().strip(), tree)
    
    # 14-2
    @patch('sys.stdout', new_callable=StringIO)
    def test_dir_tree_command_without_dir(self, mock_stdout):
        tree ="""└── 我的资源
    ├── 程序设计
    │   └── 软件设计
    │       └── 设计模式
    │           ├── 1. 观察者模式
    │           ├── 2. 策略模式
    │           └── 3. 组合模式
    └── ⼯具箱
        └── Adobe"""
        self.command_identifier.process_command(f"load {self.exit_file}")
        self.command_identifier.process_command(f"dir-tree")
        self.assertEqual(mock_stdout.getvalue().strip(), tree)
    
    # 15-1
    @patch('sys.stdout', new_callable=StringIO)
    def test_history_command_without_num(self, mock_stdout):
        self.command_identifier.process_command(f"history")
        with open('log.txt', 'r', encoding='utf-8') as file:
                lines = file.readlines()
        for line in lines:
            if line.startswith('session start at') or line == '\n':
                lines.remove(line)
        history = ''.join(lines)
        self.assertEqual(mock_stdout.getvalue().strip(), history.strip())
    
    # 15-2
    @patch('sys.stdout', new_callable=StringIO)
    def test_history_command_with_num(self, mock_stdout):
        self.command_identifier.process_command(f"history 2")
        with open('log.txt', 'r', encoding='utf-8') as file:
                lines = file.readlines()
        for line in lines:
            if line.startswith('session start at') or line == '\n':
                lines.remove(line)
        history = ''.join(lines[-2:])
        self.assertEqual(mock_stdout.getvalue().strip(), history.strip())
    
    # 15-3
    @patch('sys.stdout', new_callable=StringIO)
    def test_history_command_with_num_exceed(self, mock_stdout):
        self.command_identifier.process_command(f"history 1000000")
        with open('log.txt', 'r', encoding='utf-8') as file:
                lines = file.readlines()
        for line in lines:
            if line.startswith('session start at') or line == '\n':
                lines.remove(line)
        history = ''.join(lines)
        self.assertEqual(mock_stdout.getvalue().strip(), history.strip())
        
    # 16-1
    @patch('sys.stdout', new_callable=StringIO)
    def test_stats_command_current(self, mock_stdout):
        self.command_identifier.process_command(f"load {self.exit_file}")
        time.sleep(5.1)
        self.command_identifier.process_command(f"stats current")
        self.assertEqual(mock_stdout.getvalue().strip(), f"{self.exit_file} 5 秒")
    
    # 16-2
    @patch('sys.stdout', new_callable=StringIO)
    def test_stats_command_all(self, mock_stdout):
        self.command_identifier.process_command(f"load {self.exit_file}")
        time.sleep(1.1)
        self.command_identifier.process_command(f"load {self.not_exit_file}")
        time.sleep(2.1)
        self.command_identifier.process_command(f"stats all")
        self.assertEqual(mock_stdout.getvalue().strip(), f"{self.exit_file} 1 秒\n{self.not_exit_file} 2 秒")
    
# 运行测试
if __name__ == '__main__':
    unittest.main()
