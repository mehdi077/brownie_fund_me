from brownie import FundMe
from scripts.halpful_scripts import get_account


# when interacting with a contract using brownie we need the address and an account
def fund_this():
    fund_me = FundMe[-1]
    account = get_account()
    get_enterance_fee = fund_me.getEnteranceFee() + 100
    print(f"the currient fee is {get_enterance_fee}")
    print("funding...")
    fund_me.fund({"from": account, "value": get_enterance_fee})


def withdraw():
    fund_me = FundMe[-1]
    account = get_account()
    fund_me.withdraw({"from": account})


def main():
    fund_this()
    withdraw()
