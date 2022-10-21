import socket

# https://stackoverflow.com/a/28950776
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        s.connect(('25.5.114.247', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '25.5.114.247'

    finally:
        s.close()
    return IP

ip = get_ip()
port = 80
services_prefix = "/core"
verbose_log = True

arcade = "Monkey Business"
paseli = 5730
maintenance_mode = False
