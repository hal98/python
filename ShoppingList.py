
import math

class Item():

    def __init__(self,Description,Number,UnitPrice):
        self.Description=Description
        self.Number=Number
        self.UnitPrice=UnitPrice

    def PrintItemInfo(self):
        print(self.Description, self.Number, self.UnitPrice)
    def __str__(self):
        return (self.Description)
        



ShoppingList=[]
ShoppingList.append(Item("Apple",1,0.5))
ShoppingList.append(Item("Tomato",3,15))
ShoppingList.append(Item("Orange",2,9))

Total=0
for n in range(len(ShoppingList)):
    print(ShoppingList[n].Description)
    Total+=(int(ShoppingList[n].Number)*int(ShoppingList[n].UnitPrice))
    print(str(Total))
    
    
