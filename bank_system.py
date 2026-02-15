import os
class account():

    def __init__(self,name,account_number,pin,balance=0):
        self.name = name
        self.number = account_number
        self.pin = pin
        self.balance = balance
    
    def deposit(self,amount):
        if amount > 0:
            self.balance += amount
            print(f"Deposited {amount} successfully.\n available balance: {self.balance}")
        else:
            print("Invalid deposit amount.")
        
    def withdraw(self,amount):
        if amount>0 and amount<=self.balance:
            self.balance -=amount
            print(f"Withdrew {amount} successfully.\n available balance: {self.balance}")
        else:
            print("Invalid withdrawal amount or insufficient funds.")
            print(self.balance)
        
    def check_balance(self):
        print(f"Available balance: {self.balance}")
    
    def check_pin(self,entered_pin):
        if entered_pin == self.pin:
            print("PIN verified successfully.")
            return True
        else:
            print("Incorrect PIN.")
            return False
    
    def change_pin(self,old_pin,new_pin):
        if old_pin == self.pin:
            self.pin = new_pin
            print("PIN changed successfully.")
        else:
            print("Failed to change PIN due to incorrect old PIN.")
    
    def display_account_info(self):
        print(f"Account Holder: {self.name}\nAccount Number: {self.number}\nAvailable Balance: {self.balance}")
    
    def transfer(self,amount,recipient_account):
        if amount> 0 and amount <=self.balance:
            self.balance -=amount
            recipient_account.balance +=amount
            print(f"Transferred {amount} to {recipient_account.name} successfully.\n available balance: {self.balance}")
        else:
            print("Invalid transfer amount or insufficient funds.")


class banksystem():
    
    def __init__(self):
        self.accounts=[]
        self.load_data()
    
    def create_account(self,name,account_number,pin,balance=0): 
        new_account = account(name,account_number,pin,balance)
        self.accounts.append(new_account) 
        with open("accounts.txt","a") as f:
            f.write(f"{name},{account_number+1000},{pin + 1000},{balance}\n")
        
    def login(self,account_number,pin):
        for acc in self.accounts:
            if acc.number == account_number and acc.check_pin(pin):
                print("Login successful.")
                return acc    
        print("Login failed.")
        return None
    
    def load_data(self):
        if not os.path.exists("accounts.txt"):
            return
        
        if os.path.exists("accounts.txt"):
         with open("accounts.txt","r") as f:
            for line in f:

                name,account_number,pin,balance = line.strip().split(",")
                if not any(acc.number == int(account_number)-1000 for acc in self.accounts):
                    self.accounts.append(account(name,int(account_number)-1000,int(pin)-1000,int(balance)))
    
    def save_data(self):
        with open("accounts.txt","w") as f:
            for acc in self.accounts:
                f.write(f"{acc.name},{acc.number+1000},{acc.pin+1000},{acc.balance}\n")



def main():
    bank = banksystem()
    while True:
        print("\nWelcome to the Bank System")
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            name = input("Enter your name: ")
            if not bank.accounts:
                account_number = 1000
            else:
                account_number = bank.accounts[-1].number +1
            pin = int(input("Enter your PIN: "))
            balance = int(input("Enter initial balance (optional, default is 0): ") or 0)
            bank.create_account(name,account_number,pin,balance)
            print(f"Account created successfully. Your account number is {account_number}.")
        elif choice == "2":
            account_number = int(input("Enter your account number: "))
            pin = int(input("Enter your PIN: "))
            acc = bank.login(account_number,pin)
            if acc:
                while True:
                    print("\n1. Deposit")
                    print("2. Withdraw")
                    print("3. Check Balance")
                    print("4. Change PIN")
                    print("5. Display Account Info")
                    print("6. Transfer Funds")
                    print("7. Logout")
                    sub_choice = input("Enter your choice: ")
                    if sub_choice == "1":
                        amount = int(input("Enter amount to deposit: "))
                        acc.deposit(amount)
                        print(f"Deposited {amount}. New balance: {acc.balance}")
                        bank.save_data()
                    elif sub_choice == "2":
                        amount = int(input("Enter amount to withdraw: "))
                        acc.withdraw(amount)
                        print(f"Withdrew {amount}. New balance: {acc.balance}")
                        bank.save_data()
                    elif sub_choice == "3":
                        acc.check_balance()

                    elif sub_choice == "4":
                        old_pin = int(input("Enter old PIN: "))
                        new_pin = int(input("Enter new PIN: "))
                        acc.change_pin(old_pin,new_pin)
                        bank.save_data()
                    elif sub_choice == "5":
                        acc.display_account_info()
                    elif sub_choice == "6":
                        recipient_account_number = int(input("Enter recipient's account number: "))
                        recipient_acc = next((a for a in bank.accounts if a.number == recipient_account_number), None)
                        if recipient_acc:
                            amount = int(input("Enter amount to transfer: "))
                            acc.transfer(amount,recipient_acc)
                        else:
                            print("Recipient account not found.")
                    elif sub_choice == "7":
                        print("Logged out successfully.")
                        break
                    else:
                        print("Invalid choice.")
        elif choice == "3":
            bank.save_data()
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice.")    



if __name__ == "__main__":
    main()