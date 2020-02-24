#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Utility methods for plot generations."""
import sys
import logging
import json
from typing import List, Dict, Tuple
from collections import OrderedDict
from decimal import Decimal

from TokenInfo import TOKEN_NAMES, TOKEN_DECIMALS

EDGE_TYPE = Tuple[str, str]
NODE_TYPE = str

# Set float precision (used for string representation).
FLOAT_PREC = Decimal('1e-6')


class LevelFilter(object):
    """Filter for log levels."""

    def __init__(self, level):
        """Initialize."""
        self.level = level

    def filter(self, record):
        """Filter."""
        return record.levelno < self.level


def configure_logger(loglevel):
    """Configure logger (logFile via filename = '...')."""
    FORMAT = (
        "[%(levelname)s: %(filename)s:%(lineno)s | %(funcName)s()]  %(message)s")
    formatter = logging.Formatter(FORMAT)
    root = logging.getLogger()
    root.setLevel(loglevel)

    # Print everything but errors to stdout.
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(loglevel)
    stdout_handler.setFormatter(formatter)
    stdout_handler.addFilter(LevelFilter(logging.ERROR))
    root.addHandler(stdout_handler)

    # Print errors to stderr.
    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(logging.ERROR)
    stderr_handler.setFormatter(formatter)
    root.addHandler(stderr_handler)


def decimal_to_str(v: Decimal, prec=FLOAT_PREC):
    """Convert decimal to string with given precision."""
    if v is None:
        v = Decimal('NaN')
    assert isinstance(v, Decimal)
    return str(v.quantize(FLOAT_PREC))


def _order_data_to_decimal(orders: List[Dict]) -> List[Dict]:
    """Convert order data from string to Decimal."""
    for i in range(len(orders)):
        for key in ['sellAmount', 'buyAmount', 'execSellAmount', 'execBuyAmount']:
            orders[i][key] = Decimal(orders[i].get(key, '0'))

    return orders


def read_instance_from_file(instance_file: str) -> Dict:
    """Read data from instance JSON file.

    Args:
        instance_file: Instance JSON file.

    Returns:
        A dict containing the instance data.

    """
    try:
        with open(instance_file) as f:
            inst = json.load(f, object_pairs_hook=OrderedDict)

        # Read order data as decimal by default.
        assert 'orders' in inst
        inst['orders'] = _order_data_to_decimal(inst['orders'])

        # Cap orders by the available account balance.
        for i, o in enumerate(inst['orders']):
            aID = o.get('accountID')
            tS = o['sellToken']
            available_balance = Decimal(
                inst.get('accounts', {}).get(aID, {}).get(tS, 0))
            xS_capped = min(o['sellAmount'], available_balance)
            xB_capped = xS_capped * o['buyAmount'] / o['sellAmount']

            inst['orders'][i]['sellAmount'] = xS_capped
            inst['orders'][i]['buyAmount'] = xB_capped

        return inst

    except ValueError:
        raise


def read_instance_from_blockchain() -> Dict:
    """Read data directly from blockchain.

    Returns:
        A dict containing the instance data.

    """
    import contract_reader

    # Get ID of current batch.
    batch_id = contract_reader.get_current_batch_id()

    # Read all orders.
    orders = contract_reader.get_current_orderbook()

    # Extract set of participating tokens from orders.
    tokens = sorted(
        list(set(sum([(o['sellToken'], o['buyToken']) for o in orders], ()))))
    ref_token = tokens[0]

    # Init accounts.
    accounts = contract_reader.get_account_balances(tokens, orders)

    inst = {'tokens': tokens,
            'refToken': ref_token,
            'accounts': accounts,
            'orders': orders,
            'fee': {'token': tokens[0], 'ratio': 0.001}}

    with open('./instance-%s.json' % batch_id, 'w') as f:
        json.dump(inst, f, indent=4)

    inst['orders'] = _order_data_to_decimal(inst['orders'])
    return inst


def get_token_name(token_ID: str) -> str:
    """Get the name of a token.

    Args:
        token_ID: Token ID as string.

    Returns:
        The name of the token.

    """
    # If not available, fall back to the token ID.
    return TOKEN_NAMES.get(token_ID, token_ID)


def get_token_ID(token_str: str) -> str:
    """Get the ID of a token.

    Args:
        token_str: Token name or ID.

    Returns:
        The ID of the token.

    """
    # If available, return token ID; otherwise fall back to input string.
    if token_str in TOKEN_NAMES.values():
        return list(TOKEN_NAMES.keys())[list(TOKEN_NAMES.values()).index(token_str)]
    else:
        return token_str


def get_token_decimals(token_ID: str) -> Decimal:
    """Get the number of decimals of a token.

    Args:
        token_ID: Token ID as string.

    Returns:
        The name of the token.

    """
    # If not available, fall back to 18 decimals.
    return Decimal(TOKEN_DECIMALS.get(token_ID, 18))


def get_token_prices(prices: Dict[str, str]) -> Dict[str, Decimal]:
    """Get the computed token prices.

    Args:
        prices: Dict of token prices(as big - int).

    Returns:
        Dict with all total token prices scaled to floating - point.

    """
    return {get_token_name(t): Decimal(p) / Decimal(10**(36 - get_token_decimals(t)))
            for t, p in prices.items() if p is not None}


def get_order_amount_scaled(amount: Decimal, token_ID: str):
    """Convert order amount from big-int to human-readable."""
    return amount / Decimal(10**get_token_decimals(token_ID))


def get_nr_orders_tokenpair(orders: List[Dict]) -> Dict[EDGE_TYPE, int]:
    """Get the total number of orders on every token pair.

    Args:
        orders: List of orders.

    Returns:
        A dict of {(t1, t2): nr_orders} containing the total number of a
        token t1 that can be traded against another token t2.

    """
    nr_orders_tokenpair = dict()

    for o in orders:
        tS, tB = get_token_name(o['sellToken']), get_token_name(o['buyToken'])

        # Update number of orders on tokenpair.
        if (tS, tB) in nr_orders_tokenpair:
            nr_orders_tokenpair[tS, tB] += 1
        elif (tB, tS) in nr_orders_tokenpair:
            nr_orders_tokenpair[tB, tS] += 1
        else:
            nr_orders_tokenpair[tS, tB] = 1

    for (t1, t2), n in sorted(nr_orders_tokenpair.items(),
                              key=lambda i: i[1], reverse=True):
        logging.debug(
            "Number of orders on token pair %5s <> %-5s : %3d" % (t1, t2, n))

    return nr_orders_tokenpair


def get_total_traded_amounts(orders: List) -> Tuple[Dict]:
    """Get total traded amounts of all tokens and token pairs.

    Args:
        orders: List of orders.

    Returns:
        Dictionaries with all total traded amounts.

    """
    token_amounts_sold = dict()
    token_amounts_bought = dict()

    tokenpair_amounts_sold = dict()
    tokenpair_amounts_bought = dict()

    nr_exec_orders_tokenpair = dict()

    for o in orders:
        tS, tB = get_token_name(o['sellToken']), get_token_name(o['buyToken'])

        # Get executed amounts, scaled by the number of token decimals,
        # so that they are 'real-world'numbers.
        assert all(attr in o for attr in ['execSellAmount', 'execBuyAmount'])
        xS_exec = get_order_amount_scaled(o['execSellAmount'], o['sellToken'])
        xB_exec = get_order_amount_scaled(o['execBuyAmount'], o['buyToken'])

        if xS_exec == 0:
            assert xB_exec == 0
            continue

        # Add tokens/token pairs to dicts, if necessary.
        if tS not in token_amounts_sold:
            token_amounts_sold[tS] = Decimal('0')

        if tB not in token_amounts_bought:
            token_amounts_bought[tB] = Decimal('0')

        if (tS, tB) not in tokenpair_amounts_sold:
            tokenpair_amounts_sold[(tS, tB)] = Decimal('0')

        if (tB, tS) not in tokenpair_amounts_bought:
            tokenpair_amounts_bought[(tB, tS)] = Decimal('0')

        # Update traded amounts.
        token_amounts_sold[tS] += xS_exec
        token_amounts_bought[tB] += xB_exec
        tokenpair_amounts_sold[tS, tB] += xS_exec
        tokenpair_amounts_bought[tB, tS] += xB_exec

        # Update number of orders on tokenpair.
        if (tS, tB) in nr_exec_orders_tokenpair:
            nr_exec_orders_tokenpair[tS, tB] += 1
        elif (tB, tS) in nr_exec_orders_tokenpair:
            nr_exec_orders_tokenpair[tB, tS] += 1
        else:
            nr_exec_orders_tokenpair[tS, tB] = 1

    return (token_amounts_sold,
            token_amounts_bought,
            tokenpair_amounts_sold,
            tokenpair_amounts_bought,
            nr_exec_orders_tokenpair)


def log_orders(orders: List[Dict]):
    """Print human-readable representation of orders."""
    for o in sorted(orders, key=lambda o: o['sellToken']):
        tS = get_token_name(o['sellToken'])
        tB = get_token_name(o['buyToken'])

        xS = get_order_amount_scaled(o['sellAmount'], o['sellToken'])
        xB = get_order_amount_scaled(o['buyAmount'], o['buyToken'])

        aID = o['accountID']

        logging.info("<%s>  Sell  %42s  %-6s  for at least  %42s  %-6s"
                     % (aID[:8],
                        xS.quantize(FLOAT_PREC), '[' + tS + ']',
                        xB.quantize(FLOAT_PREC), '[' + tB + ']',))
