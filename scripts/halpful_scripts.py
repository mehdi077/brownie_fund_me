from brownie import accounts, config, network, MockV3Aggregator
from web3 import Web3

DECMILS = 8
STARTING_PRICE = 200000000000

FORKED_CAHINS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_DEV_CHAINS = ["ganache-loc", "development"]


def get_account():
    if (
        network.show_active() in LOCAL_DEV_CHAINS
        or network.show_active() in FORKED_CAHINS
    ):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def deploy_mocks():
    print(f"The active network is {network.show_active()}")
    print("Deploying Mocks...")
    if len(MockV3Aggregator) <= 0:
        MockV3Aggregator.deploy(DECMILS, STARTING_PRICE, {"from": get_account()})
    print("Mocks deployed")
