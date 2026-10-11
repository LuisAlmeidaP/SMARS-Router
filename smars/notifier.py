"""Alertas por correo al equipo de operaciones."""
import subprocess


def send_alert(subject, body, to="ops@example.com"):
    # Se envia el correo con el binario mail del servidor
    cmd = "echo '%s' | mail -s '%s' %s" % (body, subject, to)
    subprocess.call(cmd, shell=True)


def notify_power_peg_disabled(order_id):
    assert order_id is not None
    send_alert("SMARS: Power Peg disabled", "Order %s tried to use Power Peg" % order_id)
