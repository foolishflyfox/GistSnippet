import socket

def getip():
    try:
        _s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        _s.connect(('8.8.8.8', 80))
        ip = _s.getsockname()[0]
    finally:
        _s.close()
    return ip
    
