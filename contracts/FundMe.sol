// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";

contract FundMe {
    using SafeMathChainlink for uint256;

    mapping(address => uint256) public addressToAmountFunded;
    address[] public funders;
    address public owner;
    AggregatorV3Interface priceFeed;

    constructor(address _pricefeed) public {
        priceFeed = AggregatorV3Interface(_pricefeed);
        owner = msg.sender;
    }

    // msg.value will be in eth .................THE 1er IMPORTANT
    function fund() public payable {
        uint256 minimumUSD = 50 * 10**18;
        require(
            getConversionRate(msg.value) >= minimumUSD,
            "You need to spend more ETH!"
        );
        addressToAmountFunded[msg.sender] += msg.value;
        funders.push(msg.sender);
    }

    function getVersion() public view returns (uint256) {
        return priceFeed.version();
    }

    // returns the price ETHUSD in wie
    function getPrice() public view returns (uint256) {
        (, int256 answer, , , ) = priceFeed.latestRoundData();
        return uint256(answer * 10000000000);
        // the "answer" is in gwie, we x to 10000000000 to get the wie conversion
    }

    // this ruturn in wie
    function getConversionRate(uint256 _ethAmount)
        public
        view
        returns (uint256)
    {
        uint256 ethPrice = getPrice();
        uint256 ethAmountInUsd = (ethPrice * _ethAmount) / 1000000000000000000;
        return ethAmountInUsd;
    }

    //this returns price in ETH
    function getEnteranceFee() public view returns (uint256) {
        uint256 price = getPrice();
        uint256 minimumUSD = 50 * 10**18;
        uint256 precision = 1 * 10**18;
        return (minimumUSD * precision) / price;
    }

    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }

    // msg.value will be in eth .................THE 2end IMPORTANT
    function withdraw() public payable onlyOwner {
        msg.sender.transfer(address(this).balance);

        // update the stutas of the funders
        for (uint256 i = 0; i < funders.length; i++) {
            address funder = funders[i];
            addressToAmountFunded[funder] = 0;
        }
        funders = new address[](0);
    }

    // just knowing the value payed of each address
    function getamountinUSD(address _accountowner)
        public
        view
        returns (uint256)
    {
        uint256 amountinUSD = addressToAmountFunded[_accountowner];
        return getConversionRate(amountinUSD);
    }
}
