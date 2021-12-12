from brownie import FundMe, accounts
from web3 import Web3


def deploy_this_test():
    account = accounts[0]
    # fund_me = FundMe.deploy({"from": account})
    print(account)


def main():
    deploy_this_test()
