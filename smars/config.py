"""Configuracion del enrutador de ordenes (escenario simulado basado en Knight Capital)."""
import os

# Credenciales de la base de datos de ordenes
DB_USER = "smars_admin"
DB_PASSWORD = "Kn1ght2012!"

BROKER_API_TOKEN = "tok_live_9f8a7b6c5d4e3f2a1b"

# La misma bandera se reutiliza: antes activaba Power Peg, ahora activa RLP
FLAGS = {}


def load_flags(path="flags.cfg"):
    try:
        with open(path) as f:
            for line in f:
                k, v = line.strip().split("=")
                FLAGS[k] = v
    except:
        pass
    return FLAGS


def flag_enabled(name):
    return FLAGS.get(name, os.environ.get(name, "0")) == "1"


def get_max_child_orders():
    return int(os.environ.get("MAX_CHILD_ORDERS", 100000))
