import math

class MyFraction():

    def __init__(self,num,den):
        self.num = num
        self.den = den
        #print("A new variable of class MyFraction has been made")
        
    def eval(self):
        return(self.num/self.den)

    def __float__(self):
        return (self.num/self.den)

    def __mul__(self,other):
        return (MyFraction(self.num*other.num, self.den*other.den))

    def __add__(self,other):
        CommonDen = self.den*other.den
        CommonNum = self.num*other.den + other.num*self.den
        return MyFraction(CommonNum, CommonDen)
        

    def __str__(self):
        return (str(self.num) + " // " + str(self.den))

    def print(self):
        print(str(self.num) + " / " + str(self.den))

    def normalize(self):
        gcd = math.gcd(self.num, self.den)
        print(gcd)
        self.num = int(self.num/gcd)
        self.den = int(self.den/gcd)

        
class NamedFraction(MyFraction):

    def __init__(self,num,den,name):
        super().__init__(num, den)
        self.name = name

    def __str__(self):
        return(self.name + ": \n" + str(self.num) + " // " + str(self.den))
        
A = MyFraction(3,4)
B = MyFraction(1,2)


C = NamedFraction(4,7,"My own fraction")
D = A+C
print(D)
