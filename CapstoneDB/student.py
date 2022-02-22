class Student:
    """
    Student class
    """
    def __init__(self, ruid, name, encodings=[]):
        self.ruid = ruid
        self.name = name
        # 128 floats of facial encodings
        self.encodings = encodings
    def something(self):
        pass