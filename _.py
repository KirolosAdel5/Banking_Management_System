class one:
    def __init__(self):
        self.name="keroo"
        self.age="20"
    def printdata(self):
        print(f"name : {self.name} age : {self.age}")

class two(one):
    def printdata(self):
        print(f"name : {self.name} age : {self.age}")

instance=two()
instance.printdata()