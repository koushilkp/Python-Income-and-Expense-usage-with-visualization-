import pandas as pd
import csv
from datetime import datetime
from entry import get_Amount,get_Category,get_date,get_Description
import matplotlib.pyplot as plt

class CSV:
    CSV_FILE = "finance_data.csv"
    Column=["Date","Amount","Category","Description"]
    FORMAT = "%d-%m-%Y"

    @classmethod
    def intialization_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.Column)
            df.to_csv(cls.CSV_FILE,index=False)
    @classmethod
    def add_entry(cls,Date,Amount,Category,Description):
        new_entry ={
            "Date"       :Date,
            "Amount"     :Amount,
            "Category"   :Category,
            "Description":Description
        }

        with open(cls.CSV_FILE,"a",newline="") as csvfile:
            writer = csv.DictWriter(csvfile,fieldnames=cls.Column)
            writer.writerow(new_entry)
        print("Entry Successfully Added")

    @classmethod
    def get_transaction(cls,Start_date,End_date):
        df= pd.read_csv(cls.CSV_FILE)
        df["Date"] =pd.to_datetime(df["Date"],format=CSV.FORMAT)
        Start_date = datetime.strptime(Start_date,CSV.FORMAT)
        End_date  = datetime.strptime(End_date,CSV.FORMAT)

        mask = (df["Date"]>=Start_date) & (df["Date"]<= End_date)
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print("NO transaction found i given date")
        else:
            print(
                f"Transaction from {Start_date.strftime(CSV.FORMAT)} to {End_date.strftime(CSV.FORMAT)}"
                )
            
            print(
                filtered_df.to_string(
                    index=False, formatters={"Date",lambda x : x.strftime(CSV.FORMAT)}
                )
            )

            total_income = filtered_df[filtered_df["Category"]== "Income"]["Amount"].sum()
            total_expanse = filtered_df[filtered_df["Category"]== "Expense"]["Amount"].sum()
            print("\n Summary:")
            print(f"Total_Income : ${total_income:.2f}")  
            print(f"Total_Expense : ${total_expanse:.2f}")
            print(f"NetSaving: ${(total_income-total_expanse):.2f}")

        return filtered_df   


def add():
    CSV.intialization_csv()
    Date =get_date(
        "Enter the transaction date(dd-mm-yyyy) or enter today date: ",
        allow_default=True
        )
    Amount =    get_Amount()
    Category =  get_Category()
    Description = get_Description()
    CSV.add_entry(Date,Amount,Category,Description)

def plot_transaction(df):
    df.set_index("Date",inplace=True)

    income_df = (
        df[df["Category"] == "Income"]
        .resample("D")
        .sum()
        .reindex(df.index,fill_value=0)
    )

    expense_df = (
        df[df["Category"] == "Expense"]
        .resample("D")
        .sum()
        .reindex(df.index,fill_value=0)
    )

    plt.figure(figsize=(10,5))
    plt.plot(income_df.index,income_df["Amount"],label="Income",color="g")
    plt.plot(expense_df.index,expense_df["Amount"],label="Income",color="r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expense over time")
    plt.legend()
    plt.show()


def main():
    while True:
        print("\n1. Add new Transaction")
        print("2. View the Transcation and Summary within a date range")
        print("3. Exit ")
        choise =input("Enter the number between 1-3: ")

        if choise == "1":
            add()
        elif choise == "2":
            Start_date = get_date("Enter the Start date (dd-mm-yyyy): ")
            End_date   = get_date("Enter the End date (dd-mm-yyyy): ")
            df = CSV.get_transaction(Start_date,End_date)
            if input("Do you want to See a Plot ? (y/n) ").lower()=="y":
                plot_transaction(df)
        elif choise == "3":
            print("Exit...")
            break
        else:
            print("Invalid Choice. Enter 1,2 or 3")

# CSV.intialization_csv()
# CSV.add_entry("14-07-2024",1240,"Income","Salary")

if __name__ == "__main__":
    main()