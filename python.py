a=int(input("enter the choice  number"\n1,Add\n2,sub\n3,mul\n4,div\n"))
match a:
    case 1:
        a=int(input("enter the first  number"))
        b=int(input("enter the second number"))
        print(f"add of two number is {a+b}")
    case 2:
        a=int(input("enter the first  number"))
        b=int(input("enter the second number"))
        print(f"sub of two number is {a-b}")
    case 3:
        a=int(input("enter the first  number"))
        b=int(input("enter the second number"))
        print(f"mul of two number is {a*b}")
    case 4:
        a=int(input("enter the first  number"))
        b=int(input("enter the second number"))     
        print(f"div of two number is {a/b}")
    case _:
        print("invalid choice")