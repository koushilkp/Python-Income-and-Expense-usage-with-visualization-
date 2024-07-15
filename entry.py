from datetime import datetime

date_format =  "%d-%m-%Y"
Category_type = {"I":"Income","E":"Expense"}

def get_date(prompt,allow_default=False):
    date_str = input(prompt)
    if allow_default and not date_str:
        return datetime.today().strftime(date_format)
    
    try:
        valid_date = datetime.strptime(date_str,date_format)
        return valid_date.strftime(date_format)   

    except ValueError:
        print("Invalid Date format. Kindly Enter the in DD-MM-YYYY")
        return get_date(prompt,allow_default=False)

def get_Amount():
    try:
        amount= float(input("Enter the Amount : "))
        if amount <0:
            raise ValueError("Amount Should be Non Negative")
        return amount
    except ValueError as e:
        print(e)
        return get_Amount()


def get_Category():
    catogies =input("Enter the Category ('I' as Income or 'E' as Expense)").upper()
    if catogies in Category_type:
        return Category_type[catogies]
    
    print("Invaild Catarogy mention in type Other from 'I' or 'E' ")
    return get_Category()


def get_Description ():
    return input("Enter the  description: ")