import socket, json

def scan():
    available = []
    def _cc(port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.2)
            s.connect(("127.0.0.1", port))
            s.send(json.dumps({"version": "mtunn_cch1", "command": "forwarding"}).encode())
            r = s.recv(96).decode()
            s.close()
            return r
        except:
            return False

    for p in range(7010, 7091):
        try:
            st = _cc(p)
            if st != False and "<->" in st:
                remote, local = st.split("<->")
                available.append({"remote": remote.replace(" ", ""), "local": local.replace(" ", ""), "console": int(p)})
        except:
            pass
    return available

def execute(port, command):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("127.0.0.1", port))
        s.send(json.dumps({"version": "mtunn_cv1.0api", "command": command}).encode())
        fragments = []
        while True:
            chunk = s.recv(1024)
            fragments.append(chunk)
            if len(chunk) < 1024:
                break
        s.close()
        return b''.join(fragments).decode()
    except Exception as e:
        return str(e)
