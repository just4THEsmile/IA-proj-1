import numpy
class Move:
    def __init__(self,start,destiny):
        self.start=start
        self.detiny=destiny
    def add(self):
        self.a+=1
    def __str__(self):
        return 'Move' + str(self.start) +'->'+ str(self.detiny)
    def __repr__(self) -> str:
        return 'move' + str(self.start) +'->'+ str(self.detiny)
array=numpy.array([Move((2,1),(20,3))])
object=Move((0,1),(2,3))
array=numpy.append(array,object)
print(array)    
print(Move((0,1),(2,3)))
print(array[0].start[0])
print(numpy.delete(array,numpy.where(array == object)[0]))