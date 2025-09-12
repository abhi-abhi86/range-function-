class Calculator:

    def addition (self):
        a=int(input("enter the first number:"))
        b=int(input("enter the second number :"))
        print(f"sum of two numbr is :{a+b}\n")
        print("----------------------------------")
    def subtraction (self):
        a=int(input("enter the first number :"))
        b=int(input("enter the second number :"))
        print(f"sub of two number is :{a-b}\n")
        print("----------------------------------")
    def mul(self):
        a=int(input("enter the first number :"))
        b=int(input("enter the second number :"))
        print(f"multipication value of two number is :{a*b}\n")
        print("----------------------------------")
    def div (self):
        a=int(input("enter the first number :"))
        b=int(input("enter the second number :"))
        print(f"division value of two number is :{a/b}\n")
        print("----------------------------------")
def main():
    while True:
        c=Calculator ()
        print('''options:\n
1,addition
2,subtraction
3,multiplication
4,division
5,exit
    ''')
        a=input("enter the choice in given :")
        if a =="1":
            c.addition()#return can be used 
        elif a=="2":
            c.subtraction()#return can be used 
        elif a=="3":
            c.mul()#return can be used 
        elif a=="4":
            returnc.div()#return can be used 
        elif a=="5":
            print("good bye ")
            print("----------------------------------")
            exit()
        else :
            print("----------------------------------")
            print("choice the given choice only ")
            print("----------------------------------")



if __name__=="__main__":
    main()
