class Point():
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    def show(self):
        print(f"x coordinate is {self.x} \ny coordinate is {self.y}")
    def move(self):
        self.x = int(input('new x coordinate: '))
        self.y = int(input('new y coordinate: '))
    def distance(self):
        self.distance = ( ( self.x ** 2 ) + ( self.y ** 2) ) ** 0.5
        print(f'distance is {self.distance}')
obj = Point()
obj.show()
obj.move()
obj.distance()