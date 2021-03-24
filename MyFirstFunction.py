#our first function
def MyFunction(MyMessage):
    print("The message is "+MyMessage)

MyFunction("I hate this class")
MyFunction("I hate it very very muchhhh")
text="tomato"
MyFunction(text)
print(text)


def MyFunction2(MyMessage, Copies=3):
    for i in range(Copies):
        print(MyMessage)

MyFunction2(text,3)

def MyFunction3(MyMessage, a, Copies):
    for i in range(Copies):
        print(MyMessage + "" + str(a))


MyFunction3(text,"lulu",5)



def SumItems(ListArg):
    Sum=0
    for item in ListArg:
        Sum+=item
        print(str(Sum))


SumItems([1,2,5,7,9])

def SumItems2(*Args):   #also works for tuples
    Sum=0
    for Item in Args:
        Sum=Sum+Item
        print(str(Sum))

SumItems2(1,2,3,5,6,7)

import math
def MinMax(ListArg):
    Min=math.inf
    Max=-1*math.inf
    for Item in ListArg:
        if Item<Min:
            Min=Item
        if Item>Max:
            Max=Item
    return(Min,Max)

MyMinMax=MinMax([-4,10,2203,4.5,0])
print(MyMinMax)
print(type(MyMinMax))




    
