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

class CommandClassifier(Subject):
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

