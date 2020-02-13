"""Module that reads batch auction data from smart contract."""
from typing import Dict, List
from web3 import Web3
from decimal import Decimal
import logging


# Specify Infura credentials (currently: Martins access key).
infura_url = "https://node.mainnet.gnosisdev.com"
web3 = Web3(Web3.HTTPProvider(infura_url))


# Set smart contract info.
abi = '[{"constant":true,"inputs":[],"name":"IMPROVEMENT_DENOMINATOR","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getSecondsRemainingInBatch","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getEncodedOrders","outputs":[{"name":"elements","type":"bytes"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"buyToken","type":"uint16"},{"name":"sellToken","type":"uint16"},{"name":"validUntil","type":"uint32"},{"name":"buyAmount","type":"uint128"},{"name":"sellAmount","type":"uint128"}],"name":"placeOrder","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"batchId","type":"uint32"},{"name":"claimedObjectiveValue","type":"uint256"},{"name":"owners","type":"address[]"},{"name":"orderIds","type":"uint16[]"},{"name":"buyVolumes","type":"uint128[]"},{"name":"prices","type":"uint128[]"},{"name":"tokenIdsForPrice","type":"uint16[]"}],"name":"submitSolution","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"id","type":"uint16"}],"name":"tokenIdToAddressMap","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"token","type":"address"},{"name":"amount","type":"uint256"}],"name":"requestWithdraw","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"FEE_FOR_LISTING_TOKEN_IN_OWL","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"token","type":"address"},{"name":"amount","type":"uint256"}],"name":"deposit","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"orderIds","type":"uint16[]"}],"name":"cancelOrders","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"AMOUNT_MINIMUM","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"feeToken","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"buyTokens","type":"uint16[]"},{"name":"sellTokens","type":"uint16[]"},{"name":"validFroms","type":"uint32[]"},{"name":"validUntils","type":"uint32[]"},{"name":"buyAmounts","type":"uint128[]"},{"name":"sellAmounts","type":"uint128[]"}],"name":"placeValidFromOrders","outputs":[{"name":"orderIds","type":"uint16[]"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint16"}],"name":"currentPrices","outputs":[{"name":"","type":"uint128"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"user","type":"address"}],"name":"getEncodedUserOrders","outputs":[{"name":"elements","type":"bytes"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"},{"name":"","type":"uint256"}],"name":"orders","outputs":[{"name":"buyToken","type":"uint16"},{"name":"sellToken","type":"uint16"},{"name":"validFrom","type":"uint32"},{"name":"validUntil","type":"uint32"},{"name":"priceNumerator","type":"uint128"},{"name":"priceDenominator","type":"uint128"},{"name":"usedAmount","type":"uint128"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"numTokens","outputs":[{"name":"","type":"uint16"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"},{"name":"","type":"address"}],"name":"lastCreditBatchId","outputs":[{"name":"","type":"uint32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"addr","type":"address"}],"name":"hasToken","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"latestSolution","outputs":[{"name":"batchId","type":"uint32"},{"name":"solutionSubmitter","type":"address"},{"name":"feeReward","type":"uint256"},{"name":"objectiveValue","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"user","type":"address"},{"name":"token","type":"address"}],"name":"getPendingDeposit","outputs":[{"name":"","type":"uint256"},{"name":"","type":"uint32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"cancellations","type":"uint16[]"},{"name":"buyTokens","type":"uint16[]"},{"name":"sellTokens","type":"uint16[]"},{"name":"validFroms","type":"uint32[]"},{"name":"validUntils","type":"uint32[]"},{"name":"buyAmounts","type":"uint128[]"},{"name":"sellAmounts","type":"uint128[]"}],"name":"replaceOrders","outputs":[{"name":"","type":"uint16[]"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"user","type":"address"},{"name":"token","type":"address"}],"name":"getPendingWithdraw","outputs":[{"name":"","type":"uint256"},{"name":"","type":"uint32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"batchId","type":"uint32"}],"name":"acceptingSolutions","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"token","type":"address"}],"name":"addToken","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"user","type":"address"},{"name":"token","type":"address"}],"name":"getBalance","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"FEE_DENOMINATOR","outputs":[{"name":"","type":"uint128"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"BATCH_TIME","outputs":[{"name":"","type":"uint32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getCurrentBatchId","outputs":[{"name":"","type":"uint32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"user","type":"address"},{"name":"offset","type":"uint16"},{"name":"pageSize","type":"uint16"}],"name":"getEncodedUserOrdersPaginated","outputs":[{"name":"elements","type":"bytes"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"addr","type":"address"}],"name":"tokenAddressToIdMap","outputs":[{"name":"","type":"uint16"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"token","type":"address"},{"name":"amount","type":"uint256"},{"name":"batchId","type":"uint32"}],"name":"requestFutureWithdraw","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"user","type":"address"},{"name":"token","type":"address"}],"name":"hasValidWithdrawRequest","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"MAX_TOKENS","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"user","type":"address"},{"name":"token","type":"address"}],"name":"withdraw","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"MAX_TOUCHED_ORDERS","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getCurrentObjectiveValue","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[{"name":"maxTokens","type":"uint256"},{"name":"_feeToken","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"name":"owner","type":"address"},{"indexed":false,"name":"index","type":"uint16"},{"indexed":true,"name":"buyToken","type":"uint16"},{"indexed":true,"name":"sellToken","type":"uint16"},{"indexed":false,"name":"validFrom","type":"uint32"},{"indexed":false,"name":"validUntil","type":"uint32"},{"indexed":false,"name":"priceNumerator","type":"uint128"},{"indexed":false,"name":"priceDenominator","type":"uint128"}],"name":"OrderPlacement","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"owner","type":"address"},{"indexed":false,"name":"id","type":"uint256"}],"name":"OrderCancelation","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"owner","type":"address"},{"indexed":false,"name":"id","type":"uint256"}],"name":"OrderDeletion","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"owner","type":"address"},{"indexed":true,"name":"orderId","type":"uint16"},{"indexed":false,"name":"executedSellAmount","type":"uint256"},{"indexed":false,"name":"executedBuyAmount","type":"uint256"}],"name":"Trade","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"owner","type":"address"},{"indexed":true,"name":"orderId","type":"uint16"},{"indexed":false,"name":"executedSellAmount","type":"uint256"},{"indexed":false,"name":"executedBuyAmount","type":"uint256"}],"name":"TradeReversion","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"user","type":"address"},{"indexed":true,"name":"token","type":"address"},{"indexed":false,"name":"amount","type":"uint256"},{"indexed":false,"name":"batchId","type":"uint32"}],"name":"Deposit","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"user","type":"address"},{"indexed":true,"name":"token","type":"address"},{"indexed":false,"name":"amount","type":"uint256"},{"indexed":false,"name":"batchId","type":"uint32"}],"name":"WithdrawRequest","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"user","type":"address"},{"indexed":true,"name":"token","type":"address"},{"indexed":false,"name":"amount","type":"uint256"}],"name":"Withdraw","type":"event"}]'
address = "0x6F400810b62df8E13fded51bE75fF5393eaa841F"
contract = web3.eth.contract(address=address, abi=abi)


def get_current_batch_id():
    """Get ID of current batch."""
    return contract.functions.getCurrentBatchId().call()


def _read_order_from_bytes(order_bytes) -> Dict[str, str]:
    """Decode order information from bytes.

    Each order is encoded as 112 bytes:
    -- 20 bytes for accountID
    -- 32 bytes for account balance of the sellToken
    --  2 bytes for buyToken
    --  2 bytes for sellToken
    --  4 bytes for validFrom
    --  4 bytes for validUntil
    -- 16 bytes for priceNumerator
    -- 16 bytes for priceDenominator
    -- 16 bytes for remainingAmount (i.e., sellAmount)

    Returns:
        A dict containing the order information.

    """
    assert len(order_bytes) == 112

    encoding_nr_bytes = {
        'accountID': 20,
        'sellTokenBalance': 32,
        'buyToken': 2,
        'sellToken': 2,
        'validFrom': 4,
        'validUntil': 4,
        'priceNumerator': 16,
        'priceDenominator': 16,
        'remainingAmount': 16
    }

    order = {}
    i = 0
    for attr, n in encoding_nr_bytes.items():

        _bytes = order_bytes[i:i + n]

        if attr == 'accountID':
            order[attr] = '0x' + _bytes.hex()
        else:
            order[attr] = int.from_bytes(_bytes, "big")

        i += n

    return order


def get_orderbook():
    """Get all order data from smart contract.

    Returns:
        A list of all orders.

    """
    orders = []

    # Get raw order data.
    orders_encoded = contract.functions.getEncodedOrders().call()

    # Get current batch ID (for validity check).
    batch_id = get_current_batch_id()

    # Iterate over order byte strings (one order = 112 bytes).
    for order_bytes in [orders_encoded[k:k + 112]
                        for k in range(0, len(orders_encoded), 112)]:

        # Get order data.
        o = _read_order_from_bytes(order_bytes)

        # Skip orders that are no longer or not yet valid.
        if o['validUntil'] < batch_id or o['validFrom'] > batch_id:
            continue

        # Set token names.
        sell_token = 'token' + str(o['sellToken'])
        buy_token = 'token' + str(o['buyToken'])

        # Get sell amount.
        sell_amount = Decimal(min(o['remainingAmount'], o['sellTokenBalance']))
        if sell_amount == 0:
            continue

        # Compute buy amount from sell amount and limit price.
        limit_price = Decimal(o['priceNumerator']) / Decimal(o['priceDenominator'])
        if limit_price == 0:
            buy_amount = 1
        else:
            buy_amount = (sell_amount * limit_price).to_integral_value()

        logging.debug(
            "Read order: sellAmount %40d %7s -- buyAmount %40d %7s -- accountID %s"
            % (sell_amount, sell_token, buy_amount, buy_token, o['accountID']))

        orders.append({'accountID': o['accountID'],
                       'sellToken': sell_token,
                       'buyToken': buy_token,
                       'sellAmount': str(int(sell_amount)),
                       'buyAmount': str(int(buy_amount))})

    return orders


def get_account_balances(tokens: List[str],
                         orders: List[Dict]) -> Dict[str, Dict[str, str]]:
    """Get account balances of the sell tokens of all orders.

    Args:
        tokens: List of tokens with their JSON name (i.e., 'token0' etc.)
        orders: List of extracted orders.

    Returns:
        A dict of the account balances.

    """
    # Get token adresses first.
    token_adresses = {}
    for t in tokens:
        tID = int(t.replace('token', ''))
        token_adresses[t] = contract.functions.tokenIdToAddressMap(tID).call()

    # Read account balances.
    accounts = {}

    for o in orders:
        tS = o['sellToken']
        aID = o['accountID']

        if aID not in accounts:
            accounts[aID] = {}

        if tS not in accounts[aID]:
            accounts[aID][tS] = str(contract.functions.getBalance(
                Web3.toChecksumAddress(aID),
                token_adresses[tS]).call())

    return accounts
