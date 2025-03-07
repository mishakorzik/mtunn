import socket, json

def scan():
    available = []
    for p in range(7010, 7091):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 128)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 256)
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            sock.settimeout(0.1)
            sock.connect(("127.0.0.1", p))
            sock.send(json.dumps({"version": "mtunn_cch1", "command": {"execute": "forwarding"}}).encode('utf-8'))
            data = sock.recv(128)
            sock.close()
            data = json.loads(data.decode())
            available.append({"remote": data["remote"], "local": data["local"], "console": int(p)})
        except:
            pass
    return available

class console:
    def __init__(self, port):
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1024)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 2048)
        self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.sock.connect(("127.0.0.1", port))

    def execute(self, command, args1=None, args2=None, args3=None):
        try:
            j = {"version": "mtunn_cv1.3", "command": {"execute": command}}
            if args1 is not None: j["command"]["args1"] = str(args1)
            if args2 is not None: j["command"]["args2"] = str(args2)
            if args3 is not None: j["command"]["args3"] = str(args3)
            self.sock.send(json.dumps(j).encode('utf-8'))
            if command != "stop":
                fragments = []
                while True:
                    chunk = self.sock.recv(1024)
                    fragments.append(chunk)
                    if len(chunk) < 1024:
                        break
                response = b''.join(fragments).decode('utf-8')
                if "{" in response and "}" in response:
                    response = json.loads(response)
                return response
            self.sock.close()
            return "tunnel \033[01;31mstopped\033[0m"
        except Exception as e:
            return str(e)

    def close(self):
        self.sock.close()
