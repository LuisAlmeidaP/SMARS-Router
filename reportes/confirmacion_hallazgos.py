"""Script de confirmacion de H-01 y H-06 (se ejecuta despues del analisis estatico)."""
import time
from smars import config
import smars.order_router as o
from smars.order_router import OrderRouter

def fallo_correo(_):
    raise RuntimeError("servidor de correo no disponible")

o.notify_power_peg_disabled = fallo_correo
config.FLAGS["RLP_FLAG"] = "1"
r = OrderRouter(sent=[])
t = time.time()
res = r.route({"id": "p1", "symbol": "XYZ", "qty": 100, "price": 10.0, "type": "PEG"}, {"ask": 10.1, "bid": 9.9})
print("H-01 resultado:", res, "| ordenes hijas:", len(r.sent), "| acciones enviadas:", sum(q for _, q, _ in r.sent),
      "| tiempo:", round(time.time() - t, 2), "s | la alerta fallo y no se registro nada")
a = OrderRouter(); b = OrderRouter(); a._send("ABC", 1, 1.0)
print("H-06 lista de b despues de enviar desde a:", b.sent)
