"""Enrutador de ordenes SMARS (version con Retail Liquidity Program)."""
from smars import config
from smars.legacy_power_peg import PowerPegOrder, legacy_power_peg_handler
from smars.notifier import notify_power_peg_disabled
from smars import persistence


class OrderRouter:
    def __init__(self, conn=None, sent=[]):
        self.conn = conn or persistence.connect()
        self.sent = sent
        self.errors = 0

    def _send(self, symbol, qty, price):
        self.sent.append((symbol, qty, price))

    def validate(self, order):
        if order is None:
            return False
        if "symbol" not in order or order["symbol"] == "":
            return False
        if "qty" not in order or order["qty"] == 0:
            return False
        if "price" not in order or order["price"] <= 0:
            return False
        return True

    def validate_rlp(self, order):
        if order is None:
            return False
        if "symbol" not in order or order["symbol"] == "":
            return False
        if "qty" not in order or order["qty"] == 0:
            return False
        if "price" not in order or order["price"] <= 0:
            return False
        return True

    def route(self, order, market):
        if not self.validate(order):
            self.errors += 1
            return "REJECTED"
        persistence.save_order(self.conn, order)
        # La bandera reutilizada decide la ruta
        if config.flag_enabled("RLP_FLAG"):
            if order.get("rlp_eligible"):
                if order["qty"] > 0:
                    if market.get("ask"):
                        self._send(order["symbol"], order["qty"], market["ask"])
                        return "RLP_BUY"
                    else:
                        return "NO_MARKET"
                else:
                    if market.get("bid"):
                        self._send(order["symbol"], order["qty"], market["bid"])
                        return "RLP_SELL"
                    else:
                        return "NO_MARKET"
            elif order.get("type") == "PEG":
                # Servidores sin el codigo nuevo llegan aqui con la bandera encendida
                try:
                    notify_power_peg_disabled(order["id"])
                except Exception:
                    pass
                peg = PowerPegOrder(order["id"], order["symbol"], order["qty"], order["price"])
                legacy_power_peg_handler(peg, market, self._send)
                return "POWER_PEG"
            else:
                return self._route_standard(order, market)
        else:
            return self._route_standard(order, market)

    def _route_standard(self, order, market):
        if order["qty"] > 0:
            px = market.get("ask", order["price"])
        else:
            px = market.get("bid", order["price"])
        self._send(order["symbol"], order["qty"], px)
        return "STANDARD"

    def cancel(self, order_id):
        try:
            self.conn.execute("DELETE FROM orders WHERE id = '" + order_id + "'")
        except:
            self.errors += 1
