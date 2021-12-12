from brownie import FundMe, MockV3Aggregator, config, network, config
from scripts.halpful_scripts import get_account, deploy_mocks, LOCAL_DEV_CHAINS
from web3 import Web3


def deploy_fund_me():
    account = get_account()
    # fund_me = FundMe.deploy({"from": account}, publish_source=True)
    # to pass in objects to constractor it has to be first and in ""

    if network.show_active() not in LOCAL_DEV_CHAINS:

        print(f"The active network is {network.show_active()} .")
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address
    print("three here")
    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )
    print(f"Contract FundMe deployed to : {fund_me.address}")
    print(f"the network we are in is {network.show_active()}")
    return fund_me


def main():
    deploy_fund_me()
