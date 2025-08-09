from agent import Agent, Runner, function_tool, RunnerContextWrapper, input_guradrail, GuardrailFunctionOutput
from pydantic import BaseModel

# Multiple accounts ka database
ACCOUNTS = [
    {"name": "Anum", "pin": 1234, "account_number": "ACC001", "balance": 100000},
    {"name": "Ali", "pin": 5678, "account_number": "ACC002", "balance": 50000},
    {"name": "Sara", "pin": 1111, "account_number": "ACC003", "balance": 75000},
    {"name": "Ahmed", "pin": 2222, "account_number": "ACC004", "balance": 30000},
]

class Account(BaseModel):
    name: str
    pin: int
    account_number: str

class My_output(BaseModel):
    name: str
    balance: str

guardrail_agent = Agent(
    name="Guardrail Agent",
    Instruction="You are a guardrail agent. You check if the user is asking you bank related queries.",
    output_type=My_output,
)

@input_guradrail
async def check_bank_related(ctx: RunnerContextWrapper, agent: Agent, input: str) -> GuardrailFunctionOutput:
    result = await Runner.run(guardrail_agent, input, context=ctx.context)
    return GuardrailFunctionOutput(
        tripwire_triggered=True,
        result=result
    )

def check_user(ctx: RunnerContextWrapper, agent: Agent) -> bool:
    for acc in ACCOUNTS:
        if (
            ctx.context.name == acc["name"]
            and ctx.context.pin == acc["pin"]
            and ctx.context.account_number == acc["account_number"]
        ):
            return True
    return False

@function_tool(is_enabled=check_user)
def check_balance(account_number: str) -> str:
    for acc in ACCOUNTS:
        if acc["account_number"] == account_number:
            return f"The balance of account {account_number} is ${acc['balance']}"
    return "Account not found."

bank_agent = Agent(
    name="Bank agent",
    Instruction="You are a bank agent. You answer the queries of the customer related to bank accounts and their balance information.",
    tools=[check_balance],
    output_type=My_output
)

# -------- Create Account --------
def create_account():
    print("\n--- Create New Account ---")
    name = input("Enter your name: ").strip()
    pin = int(input("Set a 4-digit PIN: ").strip())
    acc_number = input("Enter new Account Number: ").strip().upper()
    balance = float(input("Enter initial balance: ").strip())

    for acc in ACCOUNTS:
        if acc["account_number"] == acc_number:
            print("⚠ Account number already exists!")
            return

    ACCOUNTS.append({
        "name": name,
        "pin": pin,
        "account_number": acc_number,
        "balance": balance
    })
    print(f"✅ Account created successfully for {name} with Account No: {acc_number}")

# -------- Login --------
def login():
    name_input = input("Enter your name: ").strip()
    pin_input = int(input("Enter your PIN: ").strip())
    acc_number_input = input("Enter your Account Number: ").strip().upper()

    for acc in ACCOUNTS:
        if name_input == acc["name"] and pin_input == acc["pin"] and acc_number_input == acc["account_number"]:
            print("✅ Login successful!")
            while True:
                print("\n--- Account Menu ---")
                print("1. Check Balance")
                print("2. Deposit Money")
                print("3. Withdraw Money")
                print("4. Logout")
                choice = input("Choose option: ")

                if choice == "1":
                    user_context = Account(name=name_input, pin=pin_input, account_number=acc_number_input)
                    result = Runner.run_sync(bank_agent, "I want to know my balance", context=user_context)
                    print(result.final_output)

                elif choice == "2":
                    amount = float(input("Enter amount to deposit: "))
                    acc["balance"] += amount
                    print(f"✅ ${amount} deposited successfully! New Balance: ${acc['balance']}")

                elif choice == "3":
                    amount = float(input("Enter amount to withdraw: "))
                    if amount <= acc["balance"]:
                        acc["balance"] -= amount
                        print(f"✅ ${amount} withdrawn successfully! New Balance: ${acc['balance']}")
                    else:
                        print("❌ Insufficient balance!")

                elif choice == "4":
                    print("👋 Logged out!")
                    return
                else:
                    print("⚠ Invalid choice!")
            return

    print("❌ Wrong credentials!")

# -------- Delete Account --------
def delete_account():
    print("\n--- Delete Account ---")
    name_input = input("Enter your name: ").strip()
    pin_input = int(input("Enter your PIN: ").strip())
    acc_number_input = input("Enter your Account Number: ").strip().upper()

    for acc in ACCOUNTS:
        if name_input == acc["name"] and pin_input == acc["pin"] and acc_number_input == acc["account_number"]:
            ACCOUNTS.remove(acc)
            print(f"🗑 Account {acc_number_input} deleted successfully!")
            return
    print("❌ Account not found or credentials incorrect!")

# -------- Main Menu --------
while True:
    print("\n===== Bank System =====")
    print("1. Create New Account")
    print("2. Login")
    print("3. Delete Account")
    print("4. Exit")
    choice = input("Choose option: ")

    if choice == "1":
        create_account()
    elif choice == "2":
        login()
    elif choice == "3":
        delete_account()
    elif choice == "4":
        print("👋 Thank you for using Bank System!")
        break
    else:
        print("⚠ Invalid choice! Please try again.")
