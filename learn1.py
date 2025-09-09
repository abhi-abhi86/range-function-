##class string_calculation :
##    def __init__(self):
##        


def calculate_vowels(s):
    vowels='aeiou'
    count=sum(1 for char in s if char in vowels)
    return count
    
def calculate_string(f):
    
    vowels='abcdefghijklmnopqrstuvwxyz'
    count=sum(1 for char in f if char in vowels)
    return count


def main():
    while True :
        print("Options:")
        print("1. Calculate vowels in a sentence")
        print("2. Calculate letters in a sentence")
        print("3. Exit")
        try :
            choice =int(input("enter the choice:-->"))
            if choice==1:
                string=input("enter the sentence to calculate vowels:").lower()
                res=calculate_vowels(string)
                print(f"the vowels in your sentence is -->{res}")
            elif choice==2:
                string=input("enter the snetance to calculate letter in it :").lower()
                res=calculate_string(string)
                print(f"this much letter in your sentance-->{res}")
            elif choice==3:
                print("Good bye dude")
                exit()
            else:
                print("invalid input")
        except Exception as e:
            print("some thing went wrong")
if __name__=="__main__":
    main()
                
                        
            

    

    




















    
    
