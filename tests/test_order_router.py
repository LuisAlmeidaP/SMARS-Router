from smars import config
from smars.order_router import OrderRouter


def make_order(**kw):
    base = {"id": "o1", "symbol": "XYZ", "qty": 100, "price": 10.0}
    base.update(kw)
    return base


def test_rejects_invalid_order():
    r = OrderRouter(sent=[])
    assert r.route(make_order(qty=0), {}) == "REJECTED"


def test_standard_route_buy():
    config.FLAGS.clear()
    r = OrderRouter(sent=[])
    assert r.route(make_order(), {"ask": 10.1, "bid": 9.9}) == "STANDARD"


def test_rlp_buy():
    config.FLAGS["RLP_FLAG"] = "1"
    r = OrderRouter(sent=[])
    assert r.route(make_order(rlp_eligible=True), {"ask": 10.1, "bid": 9.9}) == "RLP_BUY"
    config.FLAGS.clear()


def test_rlp_sell():
    config.FLAGS["RLP_FLAG"] = "1"
    r = OrderRouter(sent=[])
    assert r.route(make_order(qty=-50, rlp_eligible=True), {"ask": 10.1, "bid": 9.9}) == "RLP_SELL"
    config.FLAGS.clear()
