class Model:
    '''
    Базовый класс для моделей
    '''

    def __init__(self, **kwargs):
        self.fields = []

        print(kwargs)
        for k, v in kwargs.items():
            if hasattr(self, k):
                attr = setattr(self, k, v)
                self.fields.append(k)
            else:
                print("[WARNING]", f"Unknown propery '{k}' for '{self._class__}'")

    def __str__(self):
        return ', '.join([f"({attr}, {str(getattr(self, attr))})" for attr in self.fields])
