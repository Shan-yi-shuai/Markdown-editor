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
class CommandSubject(Subject):
    def attach(self, observer):
        pass

    def detach(self, observer):
        pass

    def notify(self):
        pass

class CoreModule(Observer):
    def update(self):
        pass

class LogModule(Observer):
    def update(self):
        pass

class StatModule(Observer):
    def update(self):
        pass

