# Markdown-editor

## 需求文档

见`./requirement/requirement.md`和`./requirement/testcase.md`

## 使用说明

```bash
## run
$ python3 main.py
```

```bash
## test
$ python3 test.py
```

## 项目目录

```python
requirement # 需求文档和测试用例
testcase # 使用testcase进行的手动测试以及结果
command.py # 实现CommandFactory和所有Command类
file_interpreter.py # Markdown文件解析器
file_management.py # 文件管理系统
log_management.py # 日志管理系统
log.txt # 日志记录
main.py # 程序启动入口
module.py # 实现CommandIdentifier，CoreModule，LogModule，StatModule
processor.py # 实现处理所有类型命令的Processor类
stat_management.py # 统计管理系统
stat.txt # 统计记录
test.md # 测试辅助文件
test.py # 自动测试入口
```

## 功能完成度列表

自动测试代码见test.py

| 命令 | 功能 | 完成状态 | 测试编号 |
| --- | --- | --- | --- |
| load 文件路径 | 从指定路径加载文件到内存中进⾏编辑 | 完成 | 1-1 |
|  | 如果指定的文件不存在，则新建⼀个文件 | 完成 | 1-2 |
|  | 在已经加载文件后继续载入新的文件，则将原先的文件保持在后台，⾃动切换到新加载的文件进⾏编辑 | 完成 | 1-3 |
|  | 不能重复打开同⼀个文件 | 完成 | 1-4 |
| save | 有文件已经被加载 | 完成 | 2-1 |
|  | 没有文件被加载 | 完成 | 2-2 |
| ws | 显⽰已加载的所有文件名称，按加载顺序排列并显⽰序号。修改未保存的文件后加上*符号（包括新建的文件，和加载后已经修改过的文件），当前正在编辑的文件加上<符号。 | 完成 | 3-1 |
| switch 文件序号 | 切换到存在序号的文件进⾏编辑 | 完成 | 4-1 |
|  | 切换到不存在序号的文件进⾏编辑 | 完成 | 4-2 |
| close 文件序号 | 关闭序号存在的文件，选择保存 | 完成 | 5-1 |
|  | 关闭序号存在的文件，选择不保存 | 完成 | 5-2 |
|  | 关闭序号不存在的文件 | 完成 | 5-3 |
| insert [⾏号] 标题/文本 | 指定行号插入 | 完成 | 6-1 |
|  | 不指定行号插入 | 完成 | 6-2 |
| append-head 标题/文本 | 在文件起始位置插入标题或文本 | 完成 | 7-1 |
| append-tail 标题/文本 | 在文件最后⼀⾏插入标题或文本 | 完成 | 8-1 |
| delete 标题/文本 或delete ⾏号 | delete 标题/文本 | 完成 | 9-1 |
|  | delete ⾏号 | 完成 | 9-2 |
| undo | 上⼀个命令属于编辑命令 | 完成 | 10-1 |
|  | 上⼀个命令属于load与save等文件相关命令组时不能被撤销不能被跳过 | 完成 | 10-2 |
|  | 属于list，list-tree与dir-tree等显⽰相关命令组时应该被跳过 | 完成 | 10-3 |
| redo | 上⼀个编辑命令是undo | 完成 | 11-1 |
|  | 上⼀个编辑命令不是undo | 完成 | 11-2 |
| list | 以文本形式显⽰当前编辑的内容 | 完成 | 12-1 |
| list-tree | 以树形结构显⽰当前编辑的内容 | 完成 | 13-1 |
| dir-tree [⽬录] | 以树形结构显⽰指定⽬录（标题）下的内容。 | 完成 | 14-1 |
|  | 如果不指定⽬录，默认显⽰当前⼯作⽬录下的内容，即完整的树结构 | 完成 | 14-2 |
| history [数量] | 默认显⽰全部记录 | 完成 | 15-1 |
|  | 通过参数限制显⽰的数量 | 完成 | 15-2 |
|  | 指定的数量⼤于存储的历史命令数量，也显⽰全部命令记录 | 完成 | 15-3 |
| stats [all  current] | stats all | 完成 | 16-1 |
|  | stats current | 完成 | 16-2 |

## 设计模式使用

### 观察者模式

`CommandIdentifier`是被观察者（Subject），`CoreModule`，`LogModule`，`StatModule`是观察者（Observer）

当`CommandIdentifier`收到命令行输入之后，将通知所有的观察者

观察者收到通知之后会统一使用`CommandFactory()`来生成命令，当切仅当命令行输入是合法的并且是该module可以处理的

其中`LogModule`可以因此记录所有的命令输入

### 命令模式

所有的命令都继承了`Command`类，比如`class LoadCommand(Command)`

每个具体命令类的构造函数中都会初始化执行命令需要的参数以及执行命令需要的processor

```python
# load 文件路径
class LoadCommand(Command):
    def __init__(self, processor, file_path):
        self.type = FILE_COMMAND
        self.file_path = file_path
        self.processor = processor
    
    def execute(self):
        self.processor.load_file(self.file_path)
```

命令的执行延迟到`command.execute()`，而不是命令生成的时候

在具体的实现中，命令的执行统一在`CommandIdentifier`中执行，这有助于一次性输入多条命令的处理

### 工厂模式

在两个地方使用了工厂模式：命令的生成，解释器的生成

在命令生成的时候，我将参数的完整解析延迟到了`CommandFactory()`中，所以不同的Module不需要知道命令是什么，而只需要调用`CommandFactory().create()`即可

在语法解析器生成的时候，`InterpreterFactory()`根据需要解析的文本返回相应的解释器，将具体的解析过程延迟到解释器生成之后，即调用`MarkDownInterpreter().interpret()`

### 解析器模式

在解析Markdown文本的时候使用了解释器模式

针对本次任务中需要处理的不同层级的标题项，以及使⽤ *，-，+等⽆序列表或1.，2.等有序列表作为文本项，构建了不同的解释器

```python
class MarkDownInterpreter:
    def interpret(self, text):
        raise NotImplementedError
class RootInterpreter(MarkDownInterpreter)
class HeaderInterpreter(MarkDownInterpreter)
class UnorderedListInterpreter(MarkDownInterpreter)
class OrderedListInterpreter(MarkDownInterpreter)
```

### 组合模式

组合模式用于表示和管理Markdown文档的结构。以下的元素可以进行嵌套和组合从而构成树状结构，这有助于`list-tree`和`dir-tree`两个指令的实现

```python
class MarkdownElement:
    def render(self):
        raise NotImplementedError
class RootElement(MarkdownElement)
class HeaderElement(MarkdownElement)
class UnorderedElement(MarkdownElement)
class OrderedElement(MarkdownElement)
class UnorderedListElement(MarkdownElement)
class OrderedListElement(MarkdownElement)
```

### 单例模式

`FileManagement`使用了单例模式，因为`CoreModule`和`StatModule`都需要用到`FileManagement`，并且任何时刻都应该只有一个`FileManagement`，所以使用单例模式可以保证文件管理的一致性

```python
def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance

@singleton
class FileManagement:
```

### 外观模式

所有`Module`本质上都是外观类，其中包含了处理命令的`processor`和管理信息的`management`，这些子系统负责实现实际的功能，而`Module`为外界提供简化的接口

```python
class CoreModule(Observer):
    def __init__(self) -> None:
        self.file_management = FileManagement()
        self.file_command_processor = FileCommandProcessor(self.file_management)
        self.editor_command_processor = EditorCommandProcessor(self.file_management)
        self.display_command_processor = DisplayCommandProcessor(self.file_management)
        
    def update(self, command_name, command_string):
        return CommandFactory().create_command({FILE_COMMAND: self.file_command_processor, EDIT_COMMAND: self.editor_command_processor, DISPLAY_COMMAND: self.display_command_processor}, command_name, command_string)
```
