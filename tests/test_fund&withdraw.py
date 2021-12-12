from scripts.halpful_scripts import get_account, LOCAL_DEV_CHAINS
from scripts.deploy import deploy_fund_me
from brownie import network, accounts, exceptions
import pytest


def test_can_fund_withdraw():
    account = get_account()
    fund_me = deploy_fund_me()
    enterance_fee = fund_me.getEnteranceFee() + 100
    tx = fund_me.fund({"from": account, "value": enterance_fee})
    tx.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == enterance_fee

    tx2 = fund_me.withdraw({"from": account})
    tx2.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == 0


def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_DEV_CHAINS:
        pytest.skip("only on local chain testing !")
    fund_me = deploy_fund_me()
    bad_actor = accounts.add()
    # using pytest if this test is indeed raising the expected error then the test is passed
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": bad_actor})

    # account = get_account()
    # fund_me = deploy_fund_me()
