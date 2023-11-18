# Observer Interface
class Observer:
    def update(self):
        pass

# Subject (被观察者)
class Subject:
    def attach(self, observer):
        pass

    def detach(self, observer):
        pass

    def notify(self):
        pass
