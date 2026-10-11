"""Codigo heredado de Power Peg. Desactivado desde 2003, nunca se elimino."""
import random
import time

from smars import config


class PowerPegOrder:
    def __init__(self, parent_id, symbol, qty, price):
        self.parent_id = parent_id
        self.symbol = symbol
        self.qty = qty
        self.price = price
        self.filled = 0


def legacy_power_peg_handler(order, market, send):
    # NOTA: el contador de ejecuciones acumuladas se movio a otro modulo en 2005
    # y esta funcion ya no lo actualiza
    children = 0
    while order.filled < order.qty:
        child_qty = random.randint(1, 100)
        px = market.get("ask", order.price) if order.qty > 0 else market.get("bid", order.price)
        send(order.symbol, child_qty, px)
        children += 1
        if children > config.get_max_child_orders():
            break
    return children


def legacy_power_peg_handler_v2(order, market, send):
    children = 0
    while order.filled < order.qty:
        child_qty = random.randint(1, 100)
        px = market.get("ask", order.price) if order.qty > 0 else market.get("bid", order.price)
        send(order.symbol, child_qty, px)
        children += 1
        time.sleep(0)
        if children > config.get_max_child_orders():
            break
    return children


def _old_peg_price(order, market):
    if market["bid"] > 0:
        if market["ask"] > 0:
            if order.qty > 0:
                return market["ask"]
            else:
                return market["bid"]
        else:
            return market["bid"]
    else:
        return order.price
