#!/usr/bin/python3
r"""
                __              __                             .__
  _____ _____  |  | __ ____   _/  |_ __ __  ____   ____   ____ |  |
 /     \\__  \ |  |/ // __ \  \   __\  |  \/    \ /    \_/ __ \|  |
|  Y Y  \/ __ \|    <\  ___/   |  | |  |  /   |  \   |  \  ___/|  |__
|__|_|  (____  /__|_ \\___  >  |__| |____/|___|  /___|  /\___  >____/
      \/     \/     \/    \/                   \/     \/     \/

 Дякую за використання цієї бібліотеки для відкриття портів!
 Якщо знайдете хибу у коді будь ласка повідомте! Буду вдячний :D

 Переваги:
  01. Потужний захист від DDoS-атак, включаючи розширені механізми фільтрації трафіку
  02. Оптимізована багатопотокова обробка для роботи з великими обсягами трафіку
  03. Інтуїтивно зрозумілий інтерфейс для управління TCP-тунелями та налаштування портів
  04. Надійна система NAT-пробивання для зручного доступу до пристроїв у локальній мережі
  05. Автоматичний перезапуск тунелів для забезпечення безперервного з'єднання
  06. Інтеграція з API для автоматизації створення та управління тунелями
  07. Можливість роботи з динамічними IP-адресами для гнучкої маршрутизації
  08. Підтримка роботи через протоколи IPv4 та IPv6 (подвійний стек)
  09. Безпечна консоль для управління активними з'єднаннями та їх статусом у реальному часі
  10. Підтримка QoS (Quality of Service) для пріоритизації трафіку критичних застосунків

 Додатково:
  01. Для роботи бібліотеки потрібний python >= 3.6
  02. Для коректної роботи потрібно не менше 50 мб оперативної пам'яті
  03. Протестовано бібліотеку на системах linux, windows

 he1zen networks.
 copyring © 2024. All rights reserved.
"""

try:
    import subprocess as sp
    import http.client, urllib.parse, platform, threading, argparse, signal, queue, time, json, ssl, re, os, sys
    import ipaddress, itertools, socket, struct, getpass, lockis, base64, shutil, curses, json, gzip, zlib
    from cryptography.hazmat.primitives.serialization import PublicFormat, Encoding
    from cryptography.hazmat.primitives.asymmetric import padding
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import hashes
    from cryptography.x509 import load_pem_x509_certificate
    from pathlib import Path
except Exception as e:
    import subprocess, platform, sys
    if "curses" in str(e):
        if platform.system().lower() == "windows":
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "windows-curses>=2.4.0"])
                print("Installed: windows-curses")
                print("Please run «mtunn» again")
            except subprocess.CalledProcessError as e:
                print(f"Error occurred while installing “windows-curses”: {e}")
        else:
            print("Error occurred module curses not found")
    elif "ipaddress" in str(e):
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "ipaddress>=1.0.21"])
            print("Installed: ipaddress")
            print("Please run «mtunn» again")
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while installing “ipaddress”: {e}")
    elif "cryptography" in str(e):
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "cryptography>=3.2"])
            print("Installed: cryptography")
            print("Please run «mtunn» again")
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while installing “cryptography”: {e}")
    elif "lockis" in str(e):
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "lockis>=1.0.2"])
            print("Installed: lockis")
            print("Please run «mtunn» again")
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while installing “lockis”: {e}")
    else:
        print(str(e))
    sys.exit(0)

version = '1.3.1'
build = 'stable'

global debug
global potato_mode
global compression
global current_os
global support_ipv4
global support_ipv6
global supported_tls
global server_version
global server_build
global server_status
global server_latency
global is_reconnecting
global is_running_first
global is_running_console
global is_running_window

global bandwidth
global saved_network
global max_network
global used_network
global sum_tunnel_traffic
global max_connections

global tunnels_hostname
global tunnels_address
global cnt_tunnel_traffic
global max_tunnels
global tunnel_domain
global tunnel_address
global tunnel_active
global tunnel_conn
global tunnel_one
global tunnel_two
global tunnel_quota

global nat_banned_ips
global nat_priory

debug = False
colors = False
main_worker = True
is_reconnecting = False
is_running_first = True
is_running_window = False
is_running_console = False
loop_command = False
potato_mode = False
bandwidth = -1
conections = 1
compression = False
support_ipv4 = False
support_ipv6 = False
user_agent = f"openssl/{ssl.OPENSSL_VERSION.split(' ')[1]} (mtunn v{version} {build}; {str(platform.python_version())}) {str(platform.machine())}"
current_os = platform.system().lower()
supported_tls = None
max_tunnels = "0"
tunnel_active = "0"
all_conn = ""
tunnel_quota = "-"
max_network = "-"
tunnel_conn = 0
used_network = 0
max_connections = 0
cnt_tunnel_traffic = 0
sum_tunnel_traffic = 0
compressed_network = 0
saved_network = 0
stop_command = 0
packet_loss = 0
explore_port = 0
explore_domain = ""
tunnel_one = ""
tunnel_two = ""
server_build = ""
server_version = ""
server_latency = "-"
server_status = "offline"
tunnels_hostname = []
tunnels_address = []
tunnels_domain = []
nat_banned_ips = []
nat_priory = []

def init():
    global colors, current_os, supported_tls, ping_method

    # detect supported tls
    openssl_version = re.sub(r"[a-zA-Z]", "", ssl.OPENSSL_VERSION.split()[1])
    version_tuple = tuple(map(int, openssl_version.split(".")))

    if version_tuple >= (1, 1, 1):
        supported_tls = 13
    elif version_tuple >= (1, 0, 1):
        supported_tls = 12
    else:
        supported_tls = 11

    # check system for colors
    if current_os == "windows":
        if int(sys.getwindowsversion().major) >= 10:
            if str(os.system("")) == "0":
                colors = True
    elif current_os == "linux":
        colors = True

    # check if ping exists
    if shutil.which("ping"):
        ping_method = "icmp"
    else:
        ping_method = "tcp"

def printf(text, n=True):
    # modded print command
    global debug, colors
    if not colors:
        text = text.replace("\033[0m", "")
        text = text.replace("\033[01;31m", "")
        text = text.replace("\033[01;32m", "")
        text = text.replace("\033[01;33m", "")
        text = text.replace("\033[01;34m", "")
        text = text.replace("\033[01;35m", "")
        text = text.replace("\033[01;36m", "")
        text = text.replace("\033[01;37m", "")
    if debug:
        if n: print(text)
        else: print(text, end=" ", flush=True)
    else:
        if "ERROR" in text:
            if n: print(text)
            else: print(text, end=" ", flush=True)

def validate_config(cfg, schema):
    # validate tunnel config
    for key, sub in schema.items():
        if key not in cfg:
            return False
        if isinstance(sub, dict) and not validate_config(cfg[key], sub):
            return False
    return True

def check_internet():
    # check internet connections
    global tunnel_conf, support_ipv4, support_ipv6
    with open(tunnel_conf, "r") as file:
        data = [line.strip() for line in file if line.strip()]
    if len(data) < 2:
        return False
    ipv4, ipv6 = data[0].split(","), data[1].split(",")
    if not (ipv4 or ipv6):
        return False
    del data
    if support_ipv4:
        for ip in ipv4:
            sock = None
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.connect((ip, 80))
                if sock.getsockname()[0]:
                    return True
            except:
                pass
            finally:
                if sock:
                    sock.close()
    if support_ipv6:
        for ip in ipv6:
            sock = None
            try:
                sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
                sock.connect((ip, 80))
                if sock.getsockname()[0]:
                    return True
            except:
                pass
            finally:
                if sock:
                    sock.close()
    return False

def ipv():
    # detect ipv4 and ipv6
    global tunnel_conf, support_ipv4, support_ipv6
    if not (support_ipv4 or support_ipv6):
        support_ipv4 = False
        support_ipv6 = False
        with open(tunnel_conf, "r") as file:
            data = [line.strip() for line in file if line.strip()]
        if len(data) < 2:
            return False
        ipv4, ipv6 = data[0].split(","), data[1].split(",")
        if not ipv4 or not ipv6:
            return False
        del data
        for ip in ipv4:
            sock = None
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.connect((ip, 80))
                if sock.getsockname()[0]:
                    support_ipv4 = True
                    break
            except:
                pass
            finally:
                if sock:
                    sock.close()
        for ip in ipv6:
            sock = None
            try:
                sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
                sock.connect((ip, 80))
                if sock.getsockname()[0]:
                    support_ipv6 = True
                    break
            except:
                pass
            finally:
                if sock:
                    sock.close()
        if not (support_ipv4 or support_ipv6):
            return False
    return True

def configs():
    # read configs path
    global tunnel_conf, tunnel_cert, current_os
    if current_os == "windows":
        exc_script = str(Path(__file__).resolve().parent)+r"\storage"
        os.makedirs(exc_script, exist_ok=True)

        tunnel_cert = exc_script+r"\cert.pem"
        tunnel_conf = exc_script+r"\conf.hz"
    else:
        exc_script = str(Path(__file__).resolve().parent)+r"/storage"
        os.makedirs(exc_script, exist_ok=True)

        tunnel_cert = exc_script+"/cert.pem"
        tunnel_conf = exc_script+"/conf.hz"

    if not os.path.exists(tunnel_cert):
        with open(tunnel_cert, 'w') as file:
            file.write("")
    if not os.path.exists(tunnel_conf):
        with open(tunnel_conf, 'w') as file:
            file.write("8.8.8.8,1.1.1.1,9.9.9.9\n2001:4860:4860::8888,2606:4700:4700::1111,2620:fe::fe")

def build_dns_query(domain, record_type):
    # dns query builder
    transaction_id = 0x8500
    flags = 0x0100
    questions = 1
    answer_rrs = 0
    authority_rrs = 0
    additional_rrs = 0
    header = struct.pack(">HHHHHH", transaction_id, flags, questions, answer_rrs, authority_rrs, additional_rrs)
    domain_parts = domain.split(".")
    query_body = b"".join(struct.pack("B", len(part)) + part.encode("utf-8") for part in domain_parts) + b"\x00"
    query_type = struct.pack(">H", record_type)
    query_class = struct.pack(">H", 1)
    return header + query_body + query_type + query_class

def parse_name(response, offset):
    # dns name parser
    name = []
    while True:
        length = response[offset]
        if (length & 0xC0) == 0xC0:
            ptr = struct.unpack(">H", response[offset:offset+2])[0]
            offset += 2
            ptr &= 0x3FFF
            part, _ = parse_name(response, ptr)
            return ".".join(part), offset
        elif length == 0:
            offset += 1
            break
        else:
            offset += 1
            name.append(response[offset:offset+length].decode())
            offset += length
    return ".".join(name), offset

def parse_dns_response(response):
    # dns response parser
    transaction_id, flags, questions, answer_rrs, authority_rrs, additional_rrs = struct.unpack(">HHHHHH", response[:12])
    offset = 12
    for _ in range(questions):
        _, offset = parse_name(response, offset)
        offset += 4
    results = []
    for _ in range(answer_rrs):
        _, offset = parse_name(response, offset)
        record_type, record_class, ttl, data_length = struct.unpack(">HHIH", response[offset:offset+10])
        offset += 10
        if record_type == 1 and data_length == 4:  # IPv4
            results.append(socket.inet_ntop(socket.AF_INET, response[offset:offset+4]))
        elif record_type == 28 and data_length == 16:  # IPv6
            results.append(socket.inet_ntop(socket.AF_INET6, response[offset:offset+16]))
        offset += data_length
    return results

def send_dns_query(domain, record_type):
    # send dns query and return response
    global tunnel_conf
    with open(tunnel_conf, 'r') as file:
        data = [line.strip() for line in file if line.strip()]
    if len(data) < 2:
        raise ValueError("the domain could not be resolved because the configuration is corrupted.")
    ipv4, ipv6 = data[0].split(","), data[1].split(",")
    if not ipv4 or not ipv6:
        raise ValueError("the domain could not be resolved because the configuration is corrupted.")
    del data
    if support_ipv6:
        for dns in ipv6:
            try:
                query = build_dns_query(domain, record_type)
                with socket.socket(socket.AF_INET6, socket.SOCK_DGRAM) as sock:
                    sock.settimeout(5)
                    sock.sendto(query, (dns, 53))
                    response = sock.recvfrom(4096)[0]
                return parse_dns_response(response)
            except:
                pass
    else:
        for dns in ipv4:
            try:
                query = build_dns_query(domain, record_type)
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                    sock.settimeout(5)
                    sock.sendto(query, (dns, 53))
                    response = sock.recvfrom(4096)[0]
                return parse_dns_response(response)
            except:
                pass
    return None

def create_connection(host, port, use_https, timeout):
    # create http(s) connection only for (rget, rpost)
    global supported_tls, tunnel_cert, support_ipv4, support_ipv6
    ip = send_dns_query(host, 28)[0] if support_ipv6 else send_dns_query(host, 1)[0]

    if use_https:
        try:
            if support_ipv6:
                sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            else:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            sock.settimeout(timeout)
            sock.connect((ip, port))

            if supported_tls == 13:
                context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
                context.minimum_version = ssl.TLSVersion.TLSv1_3
                context.maximum_version = ssl.TLSVersion.TLSv1_3
            elif supported_tls == 12:
                if hasattr(ssl, "TLSVersion"):
                    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
                    context.minimum_version = ssl.TLSVersion.TLSv1_2
                    context.maximum_version = ssl.TLSVersion.TLSv1_2
                else:
                    context = ssl.SSLContext(ssl.PROTOCOL_TLS)
                    context.options |= ssl.OP_NO_TLSv1
                    context.options |= ssl.OP_NO_TLSv1_1
                context.set_ciphers("ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384")
            else:
                raise ValueError("only TLSv1.3 and TLSv1.2 supported")
            context.options |= ssl.OP_NO_COMPRESSION
            context.verify_mode = ssl.CERT_REQUIRED
            context.check_hostname = True

            if port == 443:
                context.load_default_certs(ssl.Purpose.SERVER_AUTH)
            else:
                context.load_verify_locations(cafile=tunnel_cert)

            ssl_sock = context.wrap_socket(sock, server_hostname=host)
            if supported_tls == 13:
                if ssl_sock.version() != "TLSv1.3":
                    raise ValueError("failed to create TLSv1.3 connection")
            elif supported_tls == 12:
                if ssl_sock.version() != "TLSv1.2":
                    raise ValueError("failed to create TLSv1.2 connection")
            else:
                raise ValueError("failed to create TLSv1.3 or TLSv1.2 connection")
            conn = http.client.HTTPSConnection(host, port, timeout=timeout)
            conn.sock = ssl_sock
            return conn
        except:
            return None
    else:
        return http.client.HTTPConnection(ip, port, timeout=timeout)

def rget(url, timeout=5):
    # send get request and return response
    parsed_url = urllib.parse.urlparse(url)
    use_https = parsed_url.scheme == "https"
    port = parsed_url.port or (443 if use_https else 80)
    conn = create_connection(parsed_url.hostname, port, use_https, timeout)
    if conn is None:
        return {}
    else:
        try:
            if port in (443, 80):
                headers = {"User-Agent": "Mozilla/5.0 (X11; Debian; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "identity", "Connection": "close"}
            else:
                headers = {"User-Agent": user_agent, "Accept-Language": "en-US", "Accept-Encoding": "identity", "Connection": "close"}
            path = parsed_url.path or "/"
            if parsed_url.query:
                path += "?" + parsed_url.query
            conn._http_vsn = 11
            conn._http_vsn_str = "HTTP/1.1"
            conn.request("GET", path, headers=headers)
            response = conn.getresponse()
            data = response.read().decode()
            if "{" in data and "}" in data and ":" in data:
                try:
                    data = json.loads(data)
                except:
                    pass
        finally:
            conn.close()
        return {"response": data, "status": response.status, "reason": response.reason}

def rpost(url, json_data=None, timeout=5):
    # send post request and return response
    parsed_url = urllib.parse.urlparse(url)
    use_https = parsed_url.scheme == "https"
    port = parsed_url.port or (443 if use_https else 80)
    conn = create_connection(parsed_url.hostname, port, use_https, timeout)
    if conn is None:
        return {}
    else:
        try:
            if port in (443, 80):
                headers = {"User-Agent": "Mozilla/5.0 (X11; Debian; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "identity", "Connection": "close"}
            else:
                headers = {"User-Agent": user_agent, "Accept-Language": "en-US", "Accept-Encoding": "identity", "Connection": "close"}
            if json_data is not None:
                body = json.dumps(json_data).encode("utf-8")
                headers["Content-Type"] = "application/json"
            else:
                body = None
            path = parsed_url.path or "/"
            if parsed_url.query:
                path += "?" + parsed_url.query
            conn._http_vsn = 11
            conn._http_vsn_str = "HTTP/1.1"
            conn.request("POST", path, body=body, headers=headers)
            response = conn.getresponse()
            data = response.read().decode()
            if "{" in data and "}" in data and ":" in data:
                try:
                    data = json.loads(data)
                except:
                    pass
        finally:
            conn.close()
        return {"response": data, "status": response.status, "reason": response.reason}

def parse_yaml(file):
    # parse yaml file
    with open(file, 'r', encoding="utf-8") as f:
        result = {}
        stack = [(result, -1)]
        for line in f:
            line = line.rstrip()
            if not line.strip() or line.lstrip().startswith('#'):
                continue
            indent = len(line) - len(line.lstrip())
            if ':' in line and not line.lstrip().startswith('- '):
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
                while stack and stack[-1][1] >= indent:
                    stack.pop()
                current_dict = stack[-1][0]
                if value == "":
                    current_dict[key] = {}
                    stack.append((current_dict[key], indent))
                else:
                    current_dict[key] = parse_value(value)
        return json.loads(json.dumps(result))

def parse_value(value):
    # return velue from yaml
    if value.lower() in ("true", "false"):
        return value.lower() == "true"
    if value.lower() in ("null", "none"):
        return None
    try:
        if '.' in value:
            return float(value)
        return int(value)
    except ValueError:
        pass
    if value.startswith('[') and value.endswith(']'):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            pass
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):  # Рядки
        return value[1:-1]
    return value

def tunnels():
    # parse all tunnels
    global tunnels_hostname, tunnels_address, tunnels_domain
    try:
        data = rget("https://raw.githubusercontent.com/mishakorzik/mtunn/refs/heads/main/tunnels.json", timeout=5)
        response = data["response"]
    except Exception as e:
        print("tunnel config error: {str(e)}")
        sys.exit(0)

    hostname_list = []
    for tunnel in response.get("tunnels", []):
        server_latency = -1
        supported_types = ""
        if "ip4" in tunnel:
            tunnel_ip = tunnel["ip4"]
            supported_types += "ipv4" if supported_types == "" else ",ipv4"
        if "ip6" in tunnel:
            tunnel_ip = tunnel["ip6"]
            if support_ipv6 != True:
                tunnel_ip = tunnel.get("ip4", tunnel_ip)
            supported_types += "ipv6" if supported_types == "" else ",ipv6"
        if support_ipv6:
            tunnels_address.append(tunnel_ip)
        else:
            tunnels_address.append(tunnel.get("ip4", tunnel_ip))
        for _ in range(3):
            if "ipv6" in supported_types and support_ipv6:
                try:
                    latency_str = ping.ipv6(tunnel_ip)
                    server_latency += float(latency_str[:-2])
                except Exception:
                    server_latency -= 1
            else:
                try:
                    latency_str = ping.ipv4(tunnel_ip)
                    server_latency += float(latency_str[:-2])
                except Exception:
                    server_latency -= 1
        latency_result = str(round(server_latency / 3)) + "ms"
        hostname = tunnel.get("hostname", "unknown")
        tunnels_domain.append(hostname)
        hostname_list.append(hostname)
        tunnels_hostname.append({
            "tunnel": hostname,
            "types": supported_types,
            "latency": latency_result
        })
    return tunnels_hostname, hostname_list

def resolve_tunnel(tunnel, method="A"):
    # resolve tunnel domain using github
    try:
        get = rget("https://raw.githubusercontent.com/mishakorzik/mtunn/refs/heads/main/tunnels.json", timeout=5)["response"]["tunnels"]
        for check in get:
            if check["hostname"] == tunnel:
                if method == "A":
                    try: return check["ip4"]
                    except: return check["ip6"]
                elif method == "AAAA":
                    try: return check["ip6"]
                    except: return check["ip4"]
        return None
    except:
        return None

def resolve_domain(domain, method="A"):
    # resolve domain using dns
    if method == "A":
        parsed = send_dns_query(domain, 1)
        if parsed == [] or parsed == None:
            if check_internet():
                return ""
            else:
                return None
        else:
            return parsed[0]
    elif method == "AAAA":
        parsed = send_dns_query(domain, 28)
        if parsed == [] or parsed == None:
            if check_internet():
                return ""
            else:
                return None
        else:
            return parsed[0]
    return None

def certs(main_server, timeout=5):
    # check server status and ssl certificate
    global tunnel_cert
    try:
        post = rpost(f"https://{main_server}:5569/c/status", json_data={"id": 0}, timeout=timeout)["response"]
        if post["server"] == "ok" and post["tls"]["version"] in ("TLSv1.3", "TLSv1.2"):
            return {"verified": "yes", "lockis": post["lockis"]["version"]}
        else:
            return {"verified": "no", "lockis": "N/A"}
    except (ssl.SSLError, KeyError, TypeError):
        try:
            get = rget(f"https://raw.githubusercontent.com/mishakorzik/mtunn/refs/heads/pages/certs/{main_server}.txt", timeout=5)["response"]
            with open(tunnel_cert, "w") as file:
                file.write(get)
            post = rpost(f"https://{main_server}:5569/c/status", json_data={"id": 0}, timeout=timeout)["response"]
            if post["server"] == "ok" and post["tls"]["version"] in ("TLSv1.3", "TLSv1.2"):
                return {"verified": "yes", "lockis": post["lockis"]["version"]}
            else:
                return {"verified": "no", "lockis": "N/A"}
        except:
            return {"verified": "no", "lockis": "N/A"}
    except (socket.timeout, socket.gaierror, ConnectionRefusedError, http.client.RemoteDisconnected, http.client.CannotSendRequest):
        return {"verified": "no", "lockis": "N/A"}

def set_net(buffer):
    # set buffer size
    if current_os == "linux":
        os.system("sudo sysctl -w net.core.rmem_default=262144")
        os.system("sudo sysctl -w net.core.wmem_default=131072")
        os.system("sudo sysctl -w net.core.rmem_max={str(buffer)}")
        os.system("sudo sysctl -w net.core.wmem_max={str(buffer // 2)}")
        return True
    elif current_os in ("freebsd", "netbsd", "openbsd"):
        os.system("sudo sysctl -w net.inet.tcp.recvspace={str(buffer)}")
        os.system("sudo sysctl -w net.inet.tcp.sendspace={str(buffer // 2)}")
        return True
    else:
        return False

def get_net():
    # get buffer size (recv, send)
    global current_os
    recv, send = 0, 0
    try:
        if current_os == "linux":
            result = sp.run(["sysctl", "-a"], capture_output=True, text=True)
            if result.returncode == 0:
                for line in result.stdout.splitlines():
                    if "net.core.rmem_max" in line:
                        recv = int(line.split("=")[-1].strip())
                    elif "net.core.wmem_max" in line:
                        send = int(line.split("=")[-1].strip())
        elif system in ("freebsd", "netbsd", "openbsd"):
            result = sp.run(["sysctl", "-a"], capture_output=True, text=True)
            if result.returncode == 0:
                for line in result.stdout.splitlines():
                    if "net.inet.tcp.recvspace" in line:
                        recv = int(line.split("=")[-1].strip())
                    elif "net.inet.tcp.sendspace" in line:
                        send = int(line.split("=")[-1].strip())
        return recv, send
    except:
        return 0, 0

def mtunn_path():
    # get path to mtunn authentification config
    global current_os
    if current_os == "windows":
        path = Path(os.getenv("APPDATA", Path.home() / "AppData" / "Roaming" / "config"))
        os.makedirs(path, exist_ok=True)
        return str(path / "mtunn-auth.hz")
    elif current_os in ("openbsd", "freebsd", "netbsd", "darwin", "linux", "dragonfly", "haiku", "sunos", "solaris"):
        path = Path(os.getenv("XDG_CONFIG_HOME", Path.home() / ".config"))
        os.makedirs(path, exist_ok=True)
        return str(path / "mtunn-auth.hz")
    else:
        return None

def is_ip(ip):
    # check if is IP-address
    try:
        ipaddress.ip_address(ip)
        return True
    except:
        return False

def menu(stdscr, options, type):
    # account navigation menu
    if curses.has_colors():
        curses.init_color(0, 0, 0, 0)
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_WHITE, 0)
        stdscr.bkgd(' ', curses.color_pair(4))
    curses.curs_set(0)
    selected_index = 0
    while True:
        stdscr.clear()
        if type == 1:
            stdscr.addstr(1, 2, "Use the ↑ and ↓ keys to select which entry is highlighted.", curses.A_BOLD)
            stdscr.addstr(2, 2, "You in account control, select option to view details.", curses.A_BOLD)
            try:
                y = 0
                for i, option in enumerate(options):
                    x = 4
                    y = 4 + i
                    mark = "*" if i == selected_index else " "
                    stdscr.addstr(y, x, f"{mark} {option}")
            except curses.error:
                sys.exit(0)
        elif type == 2:
            options.sort(key=lambda option: int(option['latency'][:-2]))
            stdscr.addstr(1, 2, "Use the ↑ and ↓ keys to select which entry is highlighted.", curses.A_BOLD)
            try:
                y = 0
                for i, option in enumerate(options):
                    x = 4
                    y = 3 + i
                    mark = "*" if i == selected_index else " "
                    size = len(f"{mark} {option['tunnel']}  {option['types']}")
                    stdscr.addstr(y, x, f"{mark} {option['tunnel']}  {option['types']}")
                    if int(option['latency'][:-2]) >= 200:
                        stdscr.addstr(y, x+size+2, option['latency'], curses.color_pair(3))
                    elif int(option['latency'][:-2]) >= 100:
                        stdscr.addstr(y, x+size+2, option['latency'], curses.color_pair(1))
                    else:
                        stdscr.addstr(y, x+size+2, option['latency'], curses.color_pair(2))
            except curses.error:
                sys.exit(0)
            stdscr.addstr(y+2, 2, "Warning:", curses.color_pair(1))
            stdscr.addstr(y+2, 11, "The server you choose will be your primary one. If you want")
            stdscr.addstr(y+3, 2, "to switch to another server, you will need to create a new account.")

        stdscr.refresh()
        try:
            key = stdscr.getch()
        except:
            sys.exit(0)

        if key == curses.KEY_UP and selected_index > 0:
            selected_index -= 1
        elif key == curses.KEY_DOWN and selected_index < len(options) - 1:
            selected_index += 1
        elif key == ord('\n'):
            stdscr.clear()
            return selected_index

def account(stdscr, path):
    # get account information
    with open(path, "r") as file:
        data = [value for value in file.read().split("\n") if value]
        token = data[0]
        email = data[1]
        main_server = data[2]
    post = rpost(f"https://{main_server}:5569/auth/register_date", json_data={"token": token, "email": email}, timeout=5)["response"]
    if post["status"] == "success":
        date = post["message"]
    else:
        date = "unknown"
    post = rpost(f"https://{main_server}:5569/auth/get_quota", json_data={"token": token, "email": email}, timeout=5)["response"]
    if post["status"] == "success":
        max_connections, tunnels, network, ports, payouts = post["message"].split(" ")
    else:
        max_connections = "?"
        tunnels = "?"
        network = "?"
        ports = "?"
        payouts = "?"
    if curses.has_colors():
        curses.init_color(0, 0, 0, 0)
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_WHITE, 0)
        stdscr.bkgd(' ', curses.color_pair(4))
    curses.curs_set(0)
    stdscr.clear()
    end_time = time.time() + 5
    for symbol in itertools.cycle(['⠋', '⠙', '⠹', '⠼', '⠴', '⠦', '⠧', '⠏']):
        if time.time() >= end_time:
            break

        stdscr.clear()
        stdscr.addstr(0, 0, f"{symbol} parsing...", curses.color_pair(1))
        stdscr.refresh()
        time.sleep(0.1)

    stdscr.clear()
    stdscr.addstr(0, 0, 'Done!', curses.color_pair(1))
    stdscr.refresh()

    stdscr.clear()

    stdscr.addstr(0, 0, "Account information:")
    stdscr.addstr(1, 0, f" account email    : {email}", curses.color_pair(2))
    stdscr.addstr(2, 0, f" account token    : {token}", curses.color_pair(2))
    stdscr.addstr(3, 0, f" account server   : {main_server}")
    stdscr.addstr(4, 0, f" register date    : {date}")
    stdscr.addstr(5, 0, "")
    stdscr.addstr(6, 0, f" tunnel(s)        : {tunnels}")
    stdscr.addstr(7, 0, f" connections      : {max_connections}")
    stdscr.addstr(8, 0, f" network limit    : {network} GB")
    stdscr.addstr(9, 0, f" allowed ports    : {ports}")
    stdscr.addstr(10, 0, "")
    stdscr.addstr(11, 0, f" available        : {payouts} month(s)", curses.color_pair(3))
    stdscr.addstr(12, 0, "\nPress 'q' to exit.")
    stdscr.refresh()
    while True:
        key = stdscr.getch()
        if key == ord('q'):
            break

def delete_account(stdscr, path):
    # permanently delete account
    if curses.has_colors():
        curses.init_color(0, 0, 0, 0)
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_WHITE, 0)
        stdscr.bkgd(' ', curses.color_pair(4))

    stdscr.clear()
    stdscr.addstr(0, 0, "WARNING.", curses.color_pair(3))
    stdscr.addstr(0, 9, "Do you really want to delete account without recovery?")
    stdscr.addstr(1, 0, "All your unused quota on this account will be deleted.")
    stdscr.addstr(3, 0, "To delete account type: “                       ”")
    stdscr.addstr(3, 25, "yes, delete my account.", curses.color_pair(2))
    stdscr.addstr(4, 0, "Delete account?: ")
    stdscr.refresh()

    curses.echo()
    curses.curs_set(1)
    try:
        key = stdscr.getstr(4, 17).decode("utf-8")
    except:
        sys.exit(0)
    curses.noecho()
    curses.curs_set(0)
    if key.lower() == "yes, delete my account.":
        try:
            with open(path, "r") as file:
                data = file.read().split("\n")
                token = data[0]
                email = data[1]
                main_server = data[2]
            post = rpost(f"https://{main_server}:5569/auth/delete_account", json_data={"token": token, "email": email}, timeout=5)["response"]
            if post["status"] == "success":
                stdscr.addstr(6, 0, post["message"], curses.color_pair(1))
            else:
                stdscr.addstr(6, 0, post["message"], curses.color_pair(2))
        except:
            stdscr.addstr(6, 0, "Failed to delete account.", curses.color_pair(2))
    else:
        stdscr.addstr(6, 0, "Account deletion cancelled.", curses.color_pair(1))
    stdscr.refresh()
    stdscr.addstr(8, 0, "Press 'q' to exit.")
    stdscr.refresh()
    while True:
        key = stdscr.getch()
        if key == ord('q'):
            break

def change_email(stdscr, path):
     # change to new email
    if curses.has_colors():
        curses.init_color(0, 0, 0, 0)
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_WHITE, 0)
        stdscr.bkgd(' ', curses.color_pair(4))

    stdscr.clear()
    stdscr.addstr(0, 0, "Changing Email...", curses.color_pair(2))

    try:
        with open(path, "r") as file:
            data = [value for value in file.read().split("\n") if value]
        token = data[0]
        old_email = data[1]
        main_server = data[2]
        del data
    except:
        stdscr.addstr(2, 0, "Error reading email data.", curses.color_pair(3))
        stdscr.refresh()
        stdscr.addstr(3, 0, "\nPress 'q' to exit.")
        while True:
            key = stdscr.getch()
            if key == ord('q'):
                break
        return

    stdscr.addstr(2, 0, "Enter your new email: ")
    stdscr.refresh()

    curses.echo()
    curses.curs_set(1)
    try:
        new_email = stdscr.getstr(2, 22).decode("utf-8")
    except:
        sys.exit(0)
    curses.noecho()
    curses.curs_set(0)
    try:
        post = rpost(f"https://{main_server}:5569/auth/change_email", json_data={"new_email": new_email, "old_email": old_email, "token": token}, timeout=5)["response"]
        if post["status"] == "success":
            stdscr.addstr(3, 0, "Enter code from email: ")
            stdscr.refresh()

            curses.echo()
            code = stdscr.getstr(3, 23).decode("utf-8")
            curses.noecho()

            post = rpost(f"https://{main_server}:5569/auth/verify_account", json_data={"email": new_email, "code": code}, timeout=5)["response"]
            if post["status"] == "success" and "token:" in post["message"]:
                with open(path, "w") as file:
                    file.write(post["message"].replace("token:", "") + "\n")
                    file.write(new_email+"\n")
                    file.write(main_server)
                stdscr.addstr(4, 0, f"Email changed to: {new_email}", curses.color_pair(1))
            elif post["status"] == "error":
                stdscr.addstr(4, 0, str(post["message"]), curses.color_pair(3))
            else:
                stdscr.addstr(4, 0, "Failed to change email!", curses.color_pair(3))
        elif post["status"] == "error":
            stdscr.addstr(4, 0, str(post["message"]), curses.color_pair(3))
        else:
            stdscr.addstr(4, 0, "Failed to change email!", curses.color_pair(3))

    except Exception as e:
        stdscr.addstr(4, 0, f"Error: {str(e)}", curses.color_pair(3))

    stdscr.addstr(6, 0, "Press 'q' to exit.")
    stdscr.refresh()
    while True:
        key = stdscr.getch()
        if key == ord('q'):
            break

def tos_pp(colors):
    # accept 'Privacy Policy' and 'Terms Of Service'
    if colors:
        print("The «\033[01;34mmake tunnel\033[0m» service by he1zen networks collects only the essential information")
        print("needed to ensure stable operation and enhance service quality. We prioritize the security")
        print("of your data and do not share it with third parties, except when required by law.")
        print("")
        print("More information can be found here:")
        print(" - https://mishakorzik.github.io/mtunn/privacy-policy.html")
        print(" - https://mishakorzik.github.io/mtunn/terms-of-service.html")
        print("")
        try:
            if str(input("Accept Terms of Service and Privacy Policy? (\033[01;32myes\033[0m/\033[01;31mno\033[0m): ")).lower() != "yes":
                return False
        except:
            return False
        return True
    else:
        print("The «make tunnel» service by he1zen networks collects only the essential information")
        print("needed to ensure stable operation and enhance service quality. We prioritize the security")
        print("of your data and do not share it with third parties, except when required by law.")
        print("")
        print("More information can be found here:")
        print(" - https://mishakorzik.github.io/mtunn/privacy-policy.html")
        print(" - https://mishakorzik.github.io/mtunn/terms-of-service.html")
        print("")
        try:
            if str(input("Accept Terms of Service and Privacy Policy? (yes/no): ")).lower() != "yes":
                return False
        except:
            return False
        return True

def register(stdscr, path, main_server):
    # register to mtunn service
    if curses.has_colors():
        curses.init_color(0, 0, 0, 0)
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_WHITE, 0)
        stdscr.bkgd(' ', curses.color_pair(4))

    line = 4
    stdscr.clear()
    stdscr.addstr(0, 0, "Email Verification", curses.color_pair(2))
    while True:
        stdscr.addstr(2, 0, "Enter your email to verify: ")
        stdscr.refresh()

        curses.echo()
        curses.curs_set(1)
        email = stdscr.getstr(2, 28).decode("utf-8")
        curses.noecho()
        if email in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT] or email == "":
            continue
        else:
            curses.curs_set(0)
            break
    try:
        post = rpost(f"https://{main_server}:5569/auth/check", json_data={"email": email}, timeout=5)["response"]
        if post["status"] == "success":
            if post["message"] == "x01":
                post = rpost(f"https://{main_server}:5569/auth/register", json_data={"email": email}, timeout=5)["response"]
            elif post["message"] == "x03":
                post = rpost(f"https://{main_server}:5569/auth/login", json_data={"email": email}, timeout=5)["response"]
            else:
                line = 6
                stdscr.addstr(4, 0, "Account verification failed!", curses.color_pair(3))
                stdscr.refresh()
                stdscr.getch()
                return

            if post["status"] == "success":
                while True:
                    stdscr.addstr(3, 0, "Enter code from email: ")
                    stdscr.refresh()

                    curses.echo()
                    curses.curs_set(1)
                    code = stdscr.getstr(3, 23).decode("utf-8")
                    curses.noecho()
                    if code in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT] or code == "":
                        continue
                    else:
                        curses.curs_set(0)
                        break
                stdscr.refresh()
                line = 7
                post = rpost(f"https://{main_server}:5569/auth/verify_account", json_data={"email": email, "code": code}, timeout=5)["response"]
                if post["status"] == "success" and "token:" in post["message"]:
                    with open(path, "w") as file:
                        file.write(post["message"].replace("token:", "")+"\n")
                        file.write(email+"\n")
                        file.write(main_server)
                    stdscr.addstr(5, 0, "Successfully authorized!", curses.color_pair(1))
                else:
                    stdscr.addstr(5, 0, "Code verification failed!", curses.color_pair(3))
            else:
                line += 2
                stdscr.addstr(4, 0, post["message"].capitalize(), curses.color_pair(3))
    except Exception as e:
        line += 1
        stdscr.addstr(4, 0, f"Request failed: {str(e)}", curses.color_pair(3))
        line += 1

    stdscr.addstr(line, 0, "Press 'q' to exit.")
    stdscr.refresh()
    while True:
        key = stdscr.getch()
        if key == ord('q'):
            break

def change_quota(stdscr, path):
    # change to new quota
    if curses.has_colors():
        curses.init_color(0, 0, 0, 0)
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_WHITE, 0)
        stdscr.bkgd(' ', curses.color_pair(3))

    curses.curs_set(0)
    stdscr.clear()
    stdscr.refresh()

    default_conn = "10"
    default_tunn = "1"
    default_netw = "50"
    default_prun = "10000-11000"

    inputs = {
        "max tunnel(s)": default_tunn,
        "max connections": default_conn,
        "max GBytes per month": default_netw,
        "allowed port range": default_prun}

    def draw_form(stdscr, selected_row):
        stdscr.clear()
        stdscr.addstr(0, 0, "Configure Quota Settings", curses.A_BOLD)
        stdscr.addstr(2, 0, "it is recommended to change the default allowed ports.")
        stdscr.addstr(3, 0, "Use the ↑ and ↓ keys to select which entry is highlighted.")
        stdscr.addstr(4, 0, "'e' to edit,  'c' to continue,  'q' to quit")
        for idx, (label, value) in enumerate(inputs.items()):
            if idx == selected_row:
                stdscr.addstr(6 + idx, 2, f"{label}{' '*(22-len(label))}: {value}", curses.A_REVERSE)
            else:
                stdscr.addstr(6 + idx, 2, f"{label}{' '*(22-len(label))}: {value}")
        stdscr.refresh()

    def get_user_input(stdscr, prompt):
        try:
            curses.echo()
            curses.curs_set(1)
            stdscr.addstr(11, 2, prompt)
            stdscr.refresh()
            user_input = stdscr.getstr(11, len(prompt) + 2, 30).decode("utf-8")
            curses.curs_set(0)
            curses.noecho()
            stdscr.addstr(11, 2, " " * (len(prompt) + 20))
            return user_input
        except:
            sys.exit(0)

    selected_row = 0
    while True:
        try:
            draw_form(stdscr, selected_row)
            key = stdscr.getch()

            if key == curses.KEY_DOWN and selected_row < len(inputs) - 1:
                selected_row += 1
            elif key == curses.KEY_UP and selected_row > 0:
                selected_row -= 1
            elif key == ord('e'):
                field = list(inputs.keys())[selected_row]
                new_value = get_user_input(stdscr, f"Enter {field}: ")
                if bool(re.fullmatch(r'[0-9,-]+', new_value)):
                    inputs[field] = new_value or inputs[field]
            elif key == ord('c'):
                break
            elif key == ord('q'):
                sys.exit(0)
        except:
            sys.exit(0)

    conn, tunn, netw, prun = (
        int(inputs["max connections"]) if inputs["max connections"] else 10,
        int(inputs["max tunnel(s)"]) if inputs["max tunnel(s)"] else 1,
        int(inputs["max GBytes per month"]) if inputs["max GBytes per month"] else 50,
        inputs["allowed port range"] if inputs["allowed port range"] else "10000-11000")

    if conn < 1 or tunn < 1 or netw < 1:
        stdscr.addstr(11, 0, "Values must be greater than 0", curses.A_BOLD)
        stdscr.getch()
        return

    tta = 0
    for add in prun.split(","):
        if "-" in add:
            p1, p2 = add.split("-")
            if int(p1) > int(p2):
                stdscr.addstr(11, 0, "The ports are incorrect", curses.A_BOLD)
                stdscr.getch()
                sys.exit(0)
            else:
                tta += int(p2) - int(p1)
        else:
            tta += 1

    if tta < 100:
        stdscr.addstr(11, 0, "Minimum 100 ports required", curses.A_BOLD)
        stdscr.getch()
        return

    with open(path, "r") as file:
        data = file.read().splitlines()
        token = data[0]
        main_server = data[2]
    try:
        post = rpost(f"https://{main_server}:5569/auth/count_quota", json_data={"conn": conn, "tunn": tunn, "netw": netw, "prun": tta}, timeout=5)["response"]
    except:
        stdscr.addstr(11, 0, "Failed to connect to server", curses.A_BOLD)
        stdscr.getch()
        return

    netw = netw * 1024 * 1024 * 1024
    if post.get("status") == "success":
        curses.curs_set(1)
        stdscr.clear()
        stdscr.addstr(0, 0, "WARNING.", curses.color_pair(1))
        stdscr.addstr(0, 9, "This will delete your current quota")
        stdscr.addstr(1, 0, f"Total new quota price: {post['message']}")
        stdscr.addstr(3, 0, "To accept new quota type: “            ”")
        stdscr.addstr(3, 27, "yes, accept.", curses.color_pair(2))
        stdscr.addstr(4, 0, "Accept new quota?: ")
        stdscr.refresh()

        curses.echo()
        try:
            key = stdscr.getstr(4, 19).decode("utf-8")
        except:
            sys.exit(0)
        curses.noecho()
        curses.curs_set(0)
        if key.lower() == "yes, accept.":
            try:
                post = rpost(f"https://{main_server}:5569/auth/change_quota", json_data={"token": token, "conn": conn, "tunn": tunn, "netw": netw, "prun": prun}, timeout=5)["response"]
                if post.get("status") == "success":
                    stdscr.addstr(6, 0, "Quota changed successfully.", curses.A_BOLD)
                    stdscr.addstr(7, 0, "Press 'q' to exit.")
                else:
                    stdscr.addstr(6, 0, "Failed to change quota.", curses.A_BOLD)
                    stdscr.addstr(7, 0, str(post["message"]).capitalize(), curses.A_BOLD)
                    stdscr.addstr(8, 0, "Press 'q' to exit.")
            except:
                stdscr.addstr(6, 0, "Could not connect to server", curses.A_BOLD)
                stdscr.addstr(7, 0, "Press 'q' to exit.")
        else:
            stdscr.addstr(6, 0, "Operation canceled.", curses.A_BOLD)
            stdscr.addstr(7, 0, "Press 'q' to exit.")
    else:
        stdscr.addstr(12, 0, "Failed to retrieve quota information", curses.A_BOLD)
        stdscr.addstr(13, 0, "Press 'q' to exit.")
    stdscr.refresh()
    while True:
        key = stdscr.getch()
        if key == ord('q'):
            break

def tunnel_gui(stdscr, protocol):
    # main tunnel gui (only when running tunnel)
    global packet_loss, tunnel_conn, main_worker, tunnel_quota, stop_command, is_running_window
    global saved_network, explore_domain, sum_tunnel_traffic, used_network, max_network, tunnel_two
    dynamic_reconnect = "reconnecting"
    counter = 0
    space = " "*30
    curses.cbreak()
    curses.curs_set(0)
    if curses.has_colors():
        curses.init_color(0, 0, 0, 0)
        curses.init_pair(1, curses.COLOR_GREEN, 0)
        curses.init_pair(2, curses.COLOR_YELLOW, 0)
        curses.init_pair(3, curses.COLOR_CYAN, 0)
        curses.init_pair(4, curses.COLOR_RED, 0)
        curses.init_pair(5, curses.COLOR_BLUE, 0)
        curses.init_pair(6, curses.COLOR_MAGENTA, 0)
        curses.init_pair(7, curses.COLOR_WHITE, 0)
        stdscr.bkgd(' ', curses.color_pair(7))
    stdscr.nodelay(1)
    is_running_window = True
    while main_worker:
        try:
            line = 1
            max_x = stdscr.getmaxyx()[1]
            start_x = max_x - 16
            if counter >= 25:
                counter = 0
                stdscr.clear()
            stdscr.addstr(0, 0, " "*max_x)
            stdscr.addstr(0, 0, "mtunn    ", curses.color_pair(3))
            stdscr.addstr(0, start_x, "(CTRL+C to stop) ")
            stdscr.addstr(line, 0, space*2)
            line += 1
            stdscr.addstr(line, 0, "Status")
            if server_status == "online":
                stdscr.addstr(line, 30, server_status+space, curses.color_pair(1))
            elif server_status == "reconnecting":
                stdscr.addstr(line, 30, dynamic_reconnect+space, curses.color_pair(2))
                dynamic_reconnect += "."
                if len(dynamic_reconnect) >= 16:
                    dynamic_reconnect = "reconnecting"
                time.sleep(0.4)
            else:
                stdscr.addstr(line, 30, server_status+space, curses.color_pair(4))
                time.sleep(0.4)
            line += 1
            stdscr.addstr(line, 0, f"Version                       {version} {build}"+space)
            if server_version != version:
                line += 1
                stdscr.addstr(line, 0, f"Update                        update available ({server_version})"+space, curses.color_pair(2))
            line += 1
            if server_latency == "-":
                stdscr.addstr(line, 0, f"Latency                       -"+space)
            else:
                if float(server_latency.replace("ms", "")) >= 200:
                    stdscr.addstr(line, 0, f"Latency                       {server_latency} (")
                    stdscr.addstr(line, 32+len(server_latency), f"bad", curses.color_pair(4))
                    stdscr.addstr(line, 35+len(server_latency), f")"+space)
                elif float(server_latency.replace("ms", "")) >= 100:
                    stdscr.addstr(line, 0, f"Latency                       {server_latency} (")
                    stdscr.addstr(line, 32+len(server_latency), f"average", curses.color_pair(2))
                    stdscr.addstr(line, 39+len(server_latency), f")"+space)
                else:
                    stdscr.addstr(line, 0, f"Latency                       {server_latency} (")
                    stdscr.addstr(line, 32+len(server_latency), f"good", curses.color_pair(1))
                    stdscr.addstr(line, 36+len(server_latency), f")"+space)
            if server_status == "online":
                if sum_tunnel_traffic > 1024: # KBytes
                    if sum_tunnel_traffic > 1048576: # MBytes
                        if sum_tunnel_traffic > 1073741824: # GBytes
                            if sum_tunnel_traffic > 1099511627776: # TBytes
                                tt = str(round(sum_tunnel_traffic / 1024 / 1024 / 1024 / 1024, 3))+" TB/s"
                            else:
                                tt = str(round(sum_tunnel_traffic / 1024 / 1024 / 1024, 3))+" GB/s"
                        else:
                            tt = str(round(sum_tunnel_traffic / 1024 / 1024, 3))+" MB/s"
                    else:
                        tt = str(round(sum_tunnel_traffic / 1024, 3))+" KB/s"
                else:
                    tt = str(sum_tunnel_traffic)+" B/s"
                line += 1
                stdscr.addstr(line, 0, f"Network usage                 {tt}"+space)
            else:
                if max_network == "-":
                    tt = "-"
                else:
                    tt = "0 B/s"
                sum_tunnel_traffic = 0
                line += 1
                stdscr.addstr(line, 0, f"Network usage                 -"+space)
            if packet_loss >= 100:
                packet_loss = 100
            line += 1
            if int(packet_loss) >= 1:
                stdscr.addstr(line, 0, f"Packet loss                   {str(packet_loss)} percent(%)"+space , curses.color_pair(2))
            else:
                stdscr.addstr(line, 0, f"Packet loss                   {str(packet_loss)} percent(%)"+space)
            line += 1
            stdscr.addstr(line, 0, f"Forwarding")
            stdscr.addstr(line, 30, protocol, curses.color_pair(5))
            stdscr.addstr(line, 30+len(protocol), f"://{explore_domain}:{str(explore_port)}"+space)
            line += 1
            stdscr.addstr(line, 0, f"                               └─ ")
            stdscr.addstr(line, 34, protocol, curses.color_pair(5))
            stdscr.addstr(line, 34+len(protocol), f"://{tunnel_two}          ")
            line += 1
            stdscr.addstr(line, 0, space*2)
            line += 1
            if int(tunnel_conn) >= round(int(max_connections) / 1.4):
                if int(tunnel_conn) >= round(int(max_connections) / 1.05):
                    stdscr.addstr(line, 0, f"Connections                   active, ")
                    stdscr.addstr(line, 38, f"{str(tunnel_conn)}", curses.color_pair(4))
                    stdscr.addstr(line, 38+len(str(tunnel_conn)), f"/{str(max_connections)}"+space)
                else:
                    stdscr.addstr(line, 0, f"Connections                   active, ")
                    stdscr.addstr(line, 38, f"{str(tunnel_conn)}", curses.color_pair(2))
                    stdscr.addstr(line, 38+len(str(tunnel_conn)), f"/{str(max_connections)}"+space)
            else:
                stdscr.addstr(line, 0, f"Connections                   active, ")
                stdscr.addstr(line, 38, f"{str(tunnel_conn)}", curses.color_pair(1))
                stdscr.addstr(line, 38+len(str(tunnel_conn)), f"/{str(max_connections)}"+space)
            line += 1
            stdscr.addstr(line, 0, f"Active tunnels                total, {tunnel_active} ")
            stdscr.addstr(line, 38+len(tunnel_active), f"of ", curses.color_pair(5))
            stdscr.addstr(line, 40+len(tunnel_active), f" {max_tunnels}"+space)
            if compression in ("zlib", "gzip"):
                if saved_network > 1024: # KBytes
                    if saved_network > 1048576: # MBytes
                        if saved_network > 1073741824: # GBytes
                            if saved_network > 1099511627776: # TBytes
                                sn = str(round(saved_network / 1024 / 1024 / 1024 / 1024, 3))+" TBytes"
                            else:
                                sn = str(round(saved_network / 1024 / 1024 / 1024, 3))+" GBytes"
                        else:
                            sn = str(round(saved_network / 1024 / 1024, 3))+" MBytes"
                    else:
                        sn = str(round(saved_network / 1024, 3))+" KBytes"
                else:
                    sn = str(saved_network)+" Bytes"
                line += 1
                stdscr.addstr(line, 0, f"Compressed network            {sn}"+space)
                stdscr.addstr(line, 31+len(sn), f"(")
                stdscr.addstr(line, 32+len(sn), compression, curses.color_pair(5))
                stdscr.addstr(line, 32+len(compression)+len(sn), f")"+space)
            line += 1
            if max_network == "-":
                nl = ""
                un = "-"
                stdscr.addstr(line, 0, f"Network limit                 {un} {nl}"+space)
                line += 1
                if str(tunnel_quota) == "-1":
                    stdscr.addstr(line, 0, f"Update quota                  now, please wait"+space)
                else:
                    stdscr.addstr(line, 0, f"Update quota                  -"+space)
            else:
                if used_network >= max_network-1048576:
                    stop_command = 1
                    main_worker = False
                if used_network > 1024: # KBytes
                    if used_network > 1048576: # MBytes
                        if used_network > 1073741824: # GBytes
                            if used_network > 1099511627776: # TBytes
                                un = str(round(used_network / 1024 / 1024 / 1024 / 1024, 2))+" TBytes"
                            else:
                                un = str(round(used_network / 1024 / 1024 / 1024, 2))+" GBytes"
                        else:
                            un = str(round(used_network / 1024 / 1024, 2))+" MBytes"
                    else:
                        un = str(round(used_network / 1024, 2))+" KBytes"
                else:
                    un = str(used_network)+" Bytes"
                if max_network > 1024: # KBytes
                    if max_network > 1048576: # MBytes
                        if max_network > 1073741824: # GBytes
                            if max_network > 1099511627776: # TBytes
                                nl = "/ "+str(round(max_network / 1024 / 1024 / 1024 / 1024, 2))+" TBytes"
                            else:
                                nl = "/ "+str(round(max_network / 1024 / 1024 / 1024, 2))+" GBytes"
                        else:
                            nl = "/ "+str(round(max_network / 1024 / 1024, 2))+" MBytes"
                    else:
                        nl = "/ "+str(round(max_network / 1024, 2))+" KBytes"
                else:
                    nl = "/ "+str(max_network)+" Bytes"
                if used_network+20971520 >= max_network:
                    stdscr.addstr(line, 0, f"Network limit                 {un} {nl}"+space, curses.color_pair(2))
                else:
                    stdscr.addstr(line, 0, f"Network limit                 {un} {nl}"+space)
                line += 1
                if str(tunnel_quota) == "-1":
                    stdscr.addstr(line, 0, f"Update quota                  now, please wait"+space)
                else:
                    stdscr.addstr(line, 0, f"Update quota                  in {tunnel_quota} day(s)"+space)
            line += 1
            stdscr.addstr(line, 0, space*2)
            stdscr.refresh()
            if packet_loss != 0:
                if server_status == "online":
                    packet_loss = packet_loss - 2
            if server_status in ("offline", "reconnecting"):
                packet_loss = 100
            if packet_loss <= 0:
                packet_loss = 0
            if packet_loss >= 100:
                packet_loss = 100
            counter += 1
            time.sleep(0.1)
        except:
            break
    is_running_window = False

def check_domain(custom_domain):
    # check custom domain if is connected
    global stop_command, main_worker, tunnel_address, tunnel_domain, debug
    counter = 0
    time.sleep(60)
    while main_worker:
        if counter >= 600:
            if support_ipv6 and isinstance(ipaddress.ip_address(tunnel_address), ipaddress.IPv6Address):
                record = resolve_domain(custom_domain, "AAAA")
            else:
                record = resolve_domain(custom_domain, "A")
            if record is not None:
                if record != str(tunnel_address):
                    stop_command = 1
                    main_worker = False
                    loop_command = True
                    time.sleep(0.5)
                    printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] domain not connected")
                    print(f"it was not possible to create a tunnel because the domain on the A or AAAA record\ndoes not point to the ip “"+tunnel_address+"”")
                    sys.exit(0)
            counter += 0
        counter += 1
        time.sleep(1)

def exit_system(signum, frame):
    # fully stop tunnel (CTRL+C)
    global main_worker, packet_loss, stop_command, server_latency, server_status, max_tunnels, tunnel_active, tunnel_quota, max_network, loop_command
    server_latency = "-"
    packet_loss = 100
    max_tunnels = "0"
    tunnel_active = "0"
    tunnel_quota = "-"
    max_network = "-"
    stop_command = 3
    server_status = "offline"
    main_worker = False
    time.sleep(0.5)
    loop_command = True
    #time.sleep(0.5)
    #os.kill(os.getpid(), signal.SIGTERM)

def start_thread(target=None, args=[]):
    # start a new thread
    try:
        threading.Thread(target=target, args=args, daemon=True).start()
        return True
    except:
        return False

def encrypt_message(message):
    # encrypt message using certificate
    global tunnel_cert
    message = str(message)
    with open(tunnel_cert, "rb") as cert_file:
        cert_data = cert_file.read()
    certificate = load_pem_x509_certificate(cert_data, backend=default_backend())
    public_key = certificate.public_key()
    encrypted_message = public_key.encrypt(
        message.encode("utf-8"),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA512()),
            algorithm=hashes.SHA512(),
            label=None
        )
    )
    return base64.urlsafe_b64encode(encrypted_message)

def make_package(target, data):
    # build package from ix and data
    global compression, saved_network
    if isinstance(data, str):
        data = data.encode('utf-8')
    if compression and len(data) >= 256:
        if compression == 'zlib':
            compressed = zlib.compress(data, level=1)
            if len(data) - 30 > len(compressed):
                saved_network += len(data) - len(compressed)
                return str(target).encode('utf-8') + b'\xd6\xae1' + compressed
        elif compression == 'gzip':
            compressed = gzip.compress(data)
            if len(data) - 30 > len(compressed):
                saved_network += len(data) - len(compressed)
                return str(target).encode('utf-8') + b'\xd6\xae2' + compressed
    return str(target).encode('utf-8') + b'\xd6\xae0' + data

def parse_package(package=b''):
    # parse package and decompress
    global saved_network
    d = package.index(b'\xd6\xae')
    c = package[d + 2:d + 3]
    if c == b'1':
        decompressed = zlib.decompress(package[d + 3:])
        saved_network += len(decompressed) - len(package[d + 3:])
        return int(package[0:d]), decompressed
    elif c == b'2':
        decompressed = gzip.decompress(package[d + 3:])
        saved_network += len(decompressed) - len(package[d + 3:])
        return int(package[0:d]), decompressed
    else:
        return int(package[0:d]), package[d + 3:]

def sock_read(sock):
    # read data from local socket
    if sock:
        try: return sock.recv(32768)
        except: return b''
    return b''

def sock_send(sock, data):
    # send data to local socket
    if isinstance(data, str):
        data = data.encode("utf-8")
    if sock:
        try:
            sock.sendall(data)
            return True
        except:
            pass
    return False

_sock_io_map = {}

def read_package(sock):
    # read package from tunnel
    global packet_loss
    if not sock:
        return
    try:
        return _sock_io_map.setdefault(id(sock), SockIO(sock)).recv()
    except:
        packet_loss += 5
        return None

def send_package(sock, ix, data):
    # send package to tunnel
    global packet_loss, cnt_tunnel_traffic, bandwidth
    if not sock:
        return
    sockid = int(id(sock))
    if sockid not in _sock_io_map:
        _sock_io_map[sockid] = SockIO(sock)
    try:
        if ix != 0:
            if bandwidth != -1:
                if cnt_tunnel_traffic > bandwidth:
                    time.sleep(1)
            cnt_tunnel_traffic += len(data)
        return _sock_io_map[sockid].send(make_package(ix, data))
    except:
        packet_loss += 5
    return None

def sock_close(sock, shut=False):
    # close sock connection
    if not sock:
        return
    if shut:
        try:
            sock.shutdown(2)
        except:
            pass
    sock.close()
    sockid = int(id(sock))
    if sockid in _sock_io_map:
        del _sock_io_map[sockid]

class ping:
    @staticmethod
    def ipv4(host):
        # ping tunnel using IPv4 (icmp, tcp)
        server_latency = "-"
        if ping_method == "tcp":
            global current_os
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 4)
                    sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 8)
                    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    if current_os in ("linux", "openbsd", "freebsd", "netbsd"):
                        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
                        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_QUICKACK, 1)
                        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_CORK, 0)
                    else:
                        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                    sock.settimeout(2)
                    sock.connect((host, 5570))
                    sock.send(b'ping')
                    start_time = time.time()
                    if sock.recv(4) == b'pong':
                        server_latency = str(round((time.time() - start_time) * 1000, 1)) + "ms"
                    sock.close()
            except:
                pass
        elif ping_method == "icmp":
            if current_os == "windows":
                try:
                    result = sp.run(["ping", "-4", host, "-w", "3000", "-n", "1"],stdout=sp.PIPE, stderr=sp.PIPE, universal_newlines=True, check=True)
                    ms = re.search(r"time[=<]\s*(\d+)\s*ms", result.stdout)
                    if ms:
                        server_latency = str(round(float(ms.group(1)), 1)) + "ms"
                except:
                    pass
            else:
                try:
                    output = sp.check_output(["ping", "-c", "1", "-W", "3", host],universal_newlines=True, stderr=sp.DEVNULL)
                    ms = re.search(r"time=(\d+\.?\d*) ms", output)
                    if ms:
                        server_latency = str(round(float(ms.group(1)), 1)) + "ms"
                except:
                    pass
        return server_latency

    @staticmethod
    def ipv6(host):
        # ping tunnel using IPv6 (icmp, tcp)
        server_latency = "-"
        if ping_method == "tcp":
            global current_os
            try:
                with socket.socket(socket.AF_INET6, socket.SOCK_STREAM) as sock:
                    sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 4)
                    sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 8)
                    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    if current_os in ("linux", "openbsd", "freebsd", "netbsd"):
                        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
                        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_QUICKACK, 1)
                        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_CORK, 0)
                    else:
                        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                    sock.settimeout(2)
                    sock.connect((host, 5070))
                    sock.send(b'ping')
                    start_time = time.time()
                    if sock.recv(4) == b'pong':
                        server_latency = str(round((time.time() - start_time) * 1000, 1)) + "ms"
                    sock.close()
            except:
                pass
        elif ping_method == "icmp":
            if current_os == "windows":
                try:
                    result = sp.run(["ping", "-6", host, "-w", "3000", "-n", "1"],stdout=sp.PIPE, stderr=sp.PIPE, universal_newlines=True, check=True)
                    ms = re.search(r"time[=<]\s*(\d+)\s*ms", result.stdout)
                    if ms:
                        server_latency = str(round(float(ms.group(1)), 1)) + "ms"
                except:
                    pass
            else:
                try:
                    output = sp.check_output(["ping", "-6", "-c", "1", "-W", "3", host], universal_newlines=True, stderr=sp.DEVNULL)
                    ms = re.search(r"time=(\d+\.?\d*) ms", output)
                    if ms:
                        server_latency = str(round(float(ms.group(1)), 1)) + "ms"
                except:
                    pass
        return server_latency

class Threads:
    def __init__(self, workers):
        self.max_workers = workers
        self.task_queue = queue.Queue()
        self.threads = []
        self._init_threads()

    def _init_threads(self):
        for _ in range(self.max_workers):
            thread = threading.Thread(target=self._worker)
            thread.daemon = True
            thread.start()
            self.threads.append(thread)

    def _worker(self):
        while True:
            data = self.task_queue.get()
            if data is None:
                self.task_queue.task_done()
                break
            func, args, kwargs = data
            try:
                func(*args, **kwargs)
            except Exception as e:
                print(f"Error executing task: {e}")
            finally:
                self.task_queue.task_done()

    def submit(self, func, *args, **kwargs):
        try:
            self.task_queue.put((func, args, kwargs), block=False)
        except queue.Full:
            return False
        return True

    def shutdown(self):
        for _ in range(self.max_workers):
            self.task_queue.put(None)
        for thread in self.threads:
            thread.join()

class PackageIt:
    def __init__(self):
        # creating new buffer
        self.head = b'\xf8Ba'
        self.leng = b'\xf8Lb'
        self.buffer = bytearray()

    def feed(self, data):
        # save data to buffer
        self.buffer.extend(data)

    def recv(self):
        # recv compiled data from buffer
        if len(self.buffer) < 6:
            return None
        hix = self.buffer.find(self.head)
        if hix == -1:
            return None
        lix = self.buffer.find(self.leng, hix + 3)
        if lix == -1:
            return None
        try:
            lns = int(self.buffer[hix + 3: lix])
        except ValueError:
            del self.buffer[:hix + 3]
            return None
        pend = lix + 3 + lns
        if len(self.buffer) < pend:
            return None
        data = self.buffer[lix + 3: pend]
        del self.buffer[:pend]
        return data

    def make(self, data):
        # make special package to communicate with tunnel
        if isinstance(data, str):
            data = data.encode('utf-8')
        return self.head + str(len(data)).encode('utf-8') + self.leng + data

class SockIO:
    def __init__(self, sock):
        # creating new SockIO
        self.pi = PackageIt()

        self.sock = sock
        self.sock.setblocking(True)
        assert sock

    def recv(self):
        # recv data from tunnel
        while True:
            data = self.pi.recv()
            if data is None:
                try:
                    r = self.sock.recv(32800)
                    if not r:
                        return None
                    self.pi.feed(r)
                except (BlockingIOError, socket.timeout):
                    break
            else:
                break
        return data

    def send(self, data):
        # send data to tunnel
        try:
            self.sock.sendall(self.pi.make(data))
            return True
        except (socket.error, BrokenPipeError):
            return False

    def close(self):
        self.sock.close()

class Base:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.starttime = int(time.time())

class Runable(Base):
    _running = False

    def __str__(self):
        import os

    def _run(self):
        pass

    def _start_run(self):
        self._run()
        self._running = False

    def start(self):
        if not self._running:
            self._running = True
            return start_thread(target=self._start_run)

    def stop(self):
        # stop tunnel processes
        self._running = False

    _dog_runing = False
    _dog_last = 0

    def _dog_run(self):
        # tunnel keep-alive checker
        global server_status, server_latency, tunnel_conn, max_network, packet_loss
        self._dog_last = int(time.time())
        while self._dog_runing:
            now = float(time.time())
            if (now - self._dog_last) > 9.1:
                server_status = "offline"
                tunnel_conn = 0
                max_network = "-"
                server_latency = "-"
                self.stop()
            time.sleep(0.5)

    def stop_dog(self):
        # stop tunnel keep-alive checker
        self._dog_runing = False

    def start_dog(self):
        # start tunnel keep-alive checker
        if not self._dog_runing:
            self._dog_runing = True
            start_thread(self._dog_run)

    def feed_dog(self):
        # add time to keep-alive
        self._dog_last = float(time.time())

class SockRunable(Runable):
    _sock = None

    def _run(self):
        pass

    def stop(self):
        if self._sock:
            sock_close(self._sock, True)
            self._sock = None
        super(SockRunable, self).stop()

class Client(SockRunable):
    def __init__(self, **cxt):
        self.colors = cxt.get('colors')
        self.primary = cxt.get('primary')
        self.proxy_bind = cxt.get('proxy_bind')
        self.proxy_port = cxt.get('proxy_port')
        self.target_host = cxt.get('target_host', '127.0.0.1')
        self.target_port = cxt.get('target_port')
        self.allow_tor = cxt.get('allow_tor', 'yes')
        self.allow_vpn = cxt.get('allow_vpn', 'yes')
        self.blacklist = cxt.get('blacklist', [])
        self.whitelist = cxt.get('whitelist', [])
        self.lowdelay = cxt.get('lowdelay', 'no')
        self.compress = cxt.get('compress', 'no')
        self.console = cxt.get('console', 'no')
        self.server = cxt.get('server')
        self.domain = cxt.get('domain', '')
        self.buffer = cxt.get('buffer', 262144)
        self.proto = cxt.get('proto', 'tcp')
        self.token = cxt.get('token')
        self.rate = cxt.get('rate', 3)
        self.arch = cxt.get('arch')
        self.name = cxt.get('name')

        self._client_map = {}
        self._global_lock = threading.Lock()
        self._getmap_lock = threading.Lock()
        self._package = None
        self._secret = None
        self._sock = None

    def _run_con(self, ix, sock):
        # process client connection
        while self._running:
            recv = sock_read(sock)
            if recv:
                send_package(self._sock, ix, recv)
            else:
                send_package(self._sock, -1 * ix, b'close')
                time.sleep(1)
                sock_close(sock)
                break

    def _add_con(self, ix):
        # add new client connection
        global current_os
        try:
            if support_ipv6 and isinstance(ipaddress.ip_address(self.target_host), ipaddress.IPv6Address):
                sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            else:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, max(131072, min(self.buffer // 2, 262144)))
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, max(262144, min(self.buffer, 524288)))
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            if current_os in ("linux", "openbsd", "freebsd", "netbsd"):
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
                sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_QUICKACK, 1)
                sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_CORK, 0)
            else:
                sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            sock.connect((self.target_host, self.target_port))
            if start_thread(self._run_con, [ix, sock]):
                self._client_map[ix] = sock
                return sock
            else:
                return None
        except:
            return None

    def _run_thread_1(self):
        # tunnel primary thread (traffic, keep-alive, stop-command)
        global main_worker, loop_command, stop_command, sum_tunnel_traffic, cnt_tunnel_traffic, is_reconnecting
        while self._running:
            start_time = time.time()
            sum_tunnel_traffic = cnt_tunnel_traffic
            cnt_tunnel_traffic = 0

            if stop_command != 0:
                if stop_command == 2:
                    main_worker = False
                    loop_command = True
                    time.sleep(0.5)
                    printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] all data used")
                elif stop_command == 3:
                    is_reconnecting = False
                elif stop_command == 4:
                    main_worker = False
                    loop_command = True
                    time.sleep(0.5)
                    printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] tunnel stopped from console")
                self.stop()

            send_package(self._sock, 0, b'#')
            time.sleep(max(0, 1.0 - float(time.time() - start_time)))

    def _run_thread_2(self):
        # tunnel secondary thread (ping, updates)
        counter = 0
        global main_worker, loop_command, server_latency, server_status, server_version, server_build
        while self._running:
            if counter >= 3600:
                if check_internet():
                    try:
                        post = rpost(f"https://{self.primary}:5569/c/version", json_data={"type": "latest-stable"}, timeout=5)["response"]
                        server_version = str(post["version"])
                        server_build = str(post["build"])
                    except:
                        verify_server = certs(self.primary, 5)
                        if verify_server["verified"] == "yes":
                            if verify_server["lockis"] != lockis.version():
                                main_worker = False
                                loop_command = True
                                time.sleep(0.5)
                                printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] too old version of «lockis»")
                                self.stop()
                        elif verify_server["verified"] == "no":
                            main_worker = False
                            loop_command = True
                            time.sleep(0.5)
                            printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] failed to verify server")
                            self.stop()
                else:
                    self.stop()
                counter = 0
            if server_status in ("offline", "reconnecting"):
                server_latency = "-"
            else:
                start_time = time.time()
                if support_ipv6 and isinstance(ipaddress.ip_address(tunnel_address), ipaddress.IPv6Address):
                    server_latency = ping.ipv6(tunnel_address)
                else:
                    server_latency = ping.ipv4(tunnel_address)
                if server_latency == "-":
                    if not check_internet():
                        self.stop()
                counter += float(time.time() - start_time)
            counter += 3.0
            time.sleep(3)

    def _packet(self, data):
        # parse and process package
        global tunnel_conn, tunnel_active, tunnel_quota, used_network, packet_loss, cnt_tunnel_traffic, all_conn
        try:
            ix, data = parse_package(data)
            if ix != 0:
                cnt_tunnel_traffic += len(data)
            if ix == 0:
                if data.startswith(b"#"):
                    self.feed_dog()
                    ac, dec, rq, tc = data.decode("utf-8")[1:].split("x")
                    tunnel_conn = int(tc)
                    tunnel_active = str(ac)
                    tunnel_quota = int(rq)
                    used_network = int(dec)
                else:
                    data = self._secret.decrypt(data, ttl=10)
                    if data.startswith(b"conn_rall;"):
                        all_conn = data.decode("utf-8")[10:]
            elif ix > 0:
                with self._getmap_lock:
                    d = self._client_map.get(ix) or self._add_con(ix)
                if d:
                    sock_send(d, data)
            else:
                nix = abs(ix)
                if nix in self._client_map:
                    if not data or data == b'close':
                        d = self._client_map[nix]
                        sock_close(d)
                        del self._client_map[nix]
        except:
            packet_loss += 5

    def _run(self):
        # connect to server and create tunnel
        global is_running_console, is_running_window, server_version, server_build, max_connections, max_network, is_running_first, tunnel_two
        global support_ipv4, support_ipv6, max_tunnels, used_network, packet_loss, server_status, main_worker, loop_command, current_os, is_reconnecting
        if self.console == "yes" and not is_running_console:
            start_thread(target=self.capi)
            is_running_console = True
        tunnel_two = f"{self.target_host}:{self.target_port}"
        is_running_first = False
        try:
            if support_ipv6 and isinstance(ipaddress.ip_address(tunnel_address), ipaddress.IPv6Address):
                if not is_reconnecting:
                    is_reconnecting = True
                else:
                    if check_internet():
                        verify_server = certs(self.primary, 5)
                        if verify_server["verified"] == "yes":
                            if verify_server["lockis"] != lockis.version():
                                main_worker = False
                                loop_command = True
                                time.sleep(0.5)
                                printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] too old version of «lockis»")
                                self.stop()
                        elif verify_server["verified"] == "no":
                            main_worker = False
                            loop_command = True
                            time.sleep(0.5)
                            printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] failed to verify server")
                            self.stop()
                    else:
                        self.stop()
                sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, self.buffer // 2)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.buffer)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                if self.lowdelay == "yes":
                    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                else:
                    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 0)
                if current_os in ("linux", "openbsd", "freebsd", "netbsd"):
                    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
                    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_QUICKACK, 1)
                    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_CORK, 0)
                sock.connect((tunnel_address, 5567))
                self._sock = sock
            else:
                if not is_reconnecting:
                    is_reconnecting = True
                else:
                    if check_internet():
                        verify_server = certs(self.primary, 5)
                        if verify_server["verified"] == "yes":
                            if verify_server["lockis"] != lockis.version():
                                main_worker = False
                                loop_command = True
                                time.sleep(0.5)
                                printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] too old version of «lockis»")
                                self.stop()
                        elif verify_server["verified"] == "no":
                            main_worker = False
                            loop_command = True
                            time.sleep(0.5)
                            printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] failed to verify server")
                            self.stop()
                    else:
                        self.stop()
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, self.buffer // 2)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.buffer)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                if self.lowdelay == "yes":
                    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                else:
                    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 0)
                if current_os in ("linux", "openbsd", "freebsd", "netbsd"):
                    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
                    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_QUICKACK, 1)
                    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_CORK, 0)
                sock.connect((tunnel_address, 5567))
                self._sock = sock
            self.start_dog()
            self._secret = lockis.gkey()
            send_package(sock, 0, encrypt_message(self._secret.decode("utf-8")))
            self._secret = lockis.lockis(self._secret)
            data = json.dumps(
            {
              "tunnel": {
                "buffer": self.buffer,
                "proto": self.proto,
                "port": self.proxy_port
              },
              "network": {
                "compression": self.compress,
                "lowdelay": self.lowdelay,
                "domain": self.domain
              },
              "system": {
                "name": self.name[:30],
                "arch": self.arch[:10]
              },
              "client": {
                "version": version,
                "build": build
              },
              "firewall": {
                "lists": {
                  "blacklist": self.blacklist,
                  "whitelist": self.whitelist
                },
                "services": {
                  "allow-tor": self.allow_tor,
                  "allow-vpn": self.allow_vpn
                },
                "protection": {
                  "rate": self.rate
                }
              },
              "token": encrypt_message(self.token).decode("utf-8"),
            })
            send_package(sock, 0, self._secret.encrypt(data.encode("utf-8")))
            ret = json.loads(self._secret.decrypt(bytes(parse_package(read_package(sock))[1]), ttl=10).decode("utf-8"))
            if ret["status"] == 1:
                self.feed_dog()
                server_status = "online"
                packet_loss = 0
                server_version = str(ret["version"])
                server_build = str(ret["build"])
                max_connections = int(ret["max_conn"])
                max_network = int(ret["max_network"])
                max_tunnels = str(ret["max_tunnels"])
                used_network = int(ret["used_network"])
                if potato_mode:
                    start_thread(target=self._run_thread_1)
                    if debug:
                        printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;34mINFO\033[0m ] connected {str(explore_domain)}:{str(explore_port)} <-> {tunnel_two}")
                    else:
                        print(f"connected {str(explore_domain)}:{str(explore_port)} <-> {tunnel_two}")
                    self._package = Threads(3)
                else:
                    start_thread(target=self._run_thread_1)
                    start_thread(target=self._run_thread_2)
                    if not is_running_window:
                        start_thread(target=lambda: curses.wrapper(tunnel_gui, self.proto))
                    self._package = Threads(5)
            elif ret["status"] == 0:
                main_worker = False
                loop_command = True
                server_status = "offline"
                time.sleep(0.5)
                printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] connection refused by the server")
                self.stop()
            elif ret["status"] == 4:
                main_worker = False
                loop_command = True
                time.sleep(0.5)
                printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] "+str(ret["message"]))
                self.stop()
            del data, ret
        except:
            self.stop()
        while self._running:
            if self._package and (data := read_package(self._sock)) is not None:
                self._package.submit(self._packet, data)

    def stop(self):
        # stop tunnel
        global packet_loss, tunnel_active, tunnel_quota, max_tunnels, max_network, server_latency, server_status, is_reconnecting
        packet_loss = 100
        tunnel_active = "0"
        tunnel_quota = "-"
        max_tunnels = "0"
        max_network = "-"
        server_latency = "-"
        if is_reconnecting and main_worker:
            server_status = "reconnecting"
        else:
            server_status = "offline"
        if self._package is not None:
            self._package.shutdown()
            self._package = None
        if self._secret is not None:
            send_package(self._sock, 0, self._secret.encrypt(b'close_tunnel'))
        self.stop_dog()
        for d in self._client_map.values():
            sock_close(d)
        self._client_map.clear()
        super(Client, self).stop()

    def capi(self):
        # tunnel console and api
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1024)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 2048)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        for port in range(7010, 7091):
            try: sock.bind(("127.0.0.1", int(port)))
            except: pass
        sock.listen(3)
        while True:
            try:
                s, a = sock.accept()
                s.settimeout(60)
                threading.Thread(target=self.sapi, kwargs={"sock": s}, daemon=True).start()
            except:
                pass

    def sapi(self, sock):
        # tunnel console thread (commands)
        global stop_command, all_conn, ping_method, tunnel_address, main_worker, used_network, max_network
        global nat_banned_ips, nat_priory, tunnel_quota, explore_port, explore_domain, tunnel_two, potato_mode
        while True:
            try:
                packet = sock.recv(1024)
                data = json.loads(packet.decode("utf-8"))
            except:
                break
            if data["version"] == "mtunn_cv1.3":
                r = data["command"]["execute"]
                a1 = data["command"].get("args1", "")
                a2 = data["command"].get("args2", "")
                a3 = data["command"].get("args3", "")
                if r == "help":
                    sock.send(b"""\033[01;33mCommands:\033[0m
 network            : current network usage and maximum network capacity
 forward            : show forwarding information for the tunnel
 threads            : show all tunnel running threads
 latency            : ping a tunnel and get the results in ms
 status             : show the current status of the tunnel
 regui              : restart tunnel gui (if is minimal mode disabled)
 quota              : display tunnel days remaining until the next quota
 stop               : force the tunnel to stop immediately

\033[01;33mFirewall:\033[0m
 ban <...>          : ban asn/ip/cidr on tunnel
 unban <...>        : unban asn/ip/cidr on tunnel
 priory <...>       : add or remove priory to ip
 rule <a1> <a2>     : update rule in firewall
 conn a             : show all connections
 list               : list all banned ips

\033[01;33mExamples:\033[0m
 ban AS12345        : blocks asn from tunnel
 ban 8.8.8.8/32     : blocks cidr from tunnel
 unban 8.8.8.8/32   : unblocks ip from tunnel
 priory 8.8.8.8     : adds ip to priority
 rule rate 1        : changes protection rate (0-5)
 rule tor no        : fully blocks tor from tunnel
 rule vpn yes       : fully allows vpn to tunnel
 conn a             : show all connections""")
                elif r == "stop":
                    stop_command = 4
                    time.sleep(0.5)
                elif r == "threads":
                    try:
                        thread_names = [thread.name.split("(", 1)[-1][:-1] if "(" in thread.name else thread.name for thread in threading.enumerate()]
                        if "MainThread" in thread_names:
                            thread_names.remove("MainThread")
                        if "<lambda>" in thread_names:
                            thread_names.remove("<lambda>")
                            thread_names.append("tunnel_gui")
                        sock.send(json.dumps({"status": "success", "total": len(thread_names), "threads": thread_names}).encode("utf-8"))
                    except:
                        sock.send(json.dumps({"status": "error", "message": "failed to get all running threads"}).encode("utf-8"))
                elif r == "regui":
                    if potato_mode:
                        sock.send(json.dumps({"status": "error", "message": "cant run in minimal mode"}).encode("utf-8"))
                    else:
                        main_worker = False
                        is_running_window = False
                        time.sleep(0.2)
                        main_worker = True
                        start_thread(target=lambda: curses.wrapper(tunnel_gui, self.proto))
                        sock.send(json.dumps({"status": "success", "message": "gui restarted"}).encode("utf-8"))
                elif r == "latency":
                    if isinstance(ipaddress.ip_address(tunnel_address), ipaddress.IPv4Address):
                        lat = ping.ipv4(tunnel_address)
                    else:
                        lat = ping.ipv6(tunnel_address)
                    sock.send(json.dumps({"status": "success", "address": str(tunnel_address), "method": str(ping_method), "time": str(lat)}).encode("utf-8"))
                elif r == "forward":
                    try:
                        sock.send(json.dumps({"status": "success", "remote": str(explore_domain)+":"+str(explore_port), "local": str(tunnel_two)}).encode("utf-8"))
                    except:
                        sock.send(json.dumps({"status": "error"}).encode("utf-8"))
                elif r == "status":
                    if "online" in server_status:
                        sock.send(json.dumps({"status": "success", "tunnel": "online"}).encode("utf-8"))
                    elif "offline" in server_status:
                        sock.send(json.dumps({"status": "success", "tunnel": "offline"}).encode("utf-8"))
                    else:
                        sock.send(json.dumps({"status": "success", "tunnel": str(server_status)}).encode("utf-8"))
                elif r == "list":
                    try:
                        sock.send(json.dumps({"status": "success", "list": nat_banned_ips}).encode("utf-8"))
                    except:
                        sock.send(json.dumps({"status": "error", "list": []}).encode("utf-8"))
                elif r == "quota":
                    if str(tunnel_quota) == "-" or str(max_network) == "-":
                        sock.send(json.dumps({"status": "success", "quota": "unknown"}).encode("utf-8"))
                    else:
                        sock.send(json.dumps({"status": "success", "quota": str(tunnel_quota)}).encode("utf-8"))
                elif r == "network":
                    _u = int(used_network)
                    _m = int(max_network)
                    if _u > 1024: # KBytes
                        if _u > 1048576: # MBytes
                            if _u > 1073741824: # GBytes
                                if _u > 1099511627776: # TBytes
                                    _u = str(round((_u / 1024 / 1024 / 1024 / 1024), 2))+" TBytes"
                                else:
                                    _u = str(round((_u / 1024 / 1024 / 1024), 2))+" GBytes"
                            else:
                                 _u = str(round((_u / 1024 / 1024), 2))+" MBytes"
                        else:
                             _u = str(round((_u / 1024), 2))+" KBytes"
                    else:
                        _u = str(round((_u), 2))+" TBytes"
                    if _m > 1024: # KBytes
                        if _m > 1048576: # MBytes
                            if _m > 1073741824: # GBytes
                                if _m > 1099511627776: # TBytes
                                    _m = str(round((_m / 1024 / 1024 / 1024 / 1024), 2))+" TBytes"
                                else:
                                    _m = str(round((_m / 1024 / 1024 / 1024), 2))+" GBytes"
                            else:
                                 _m = str(round((_m / 1024 / 1024), 2))+" MBytes"
                        else:
                             _m = str(round((_m / 1024), 2))+" KBytes"
                    else:
                        _m = str(round((_m), 2))+" Bytes"
                    sock.send(json.dumps({"status": "success", "used": str(_u), "max": str(_m)}).encode("utf-8"))
                elif r.startswith("conn"):
                    if a1 == "all" or a1 == "a":
                        try:
                            wait = 0
                            current_time = time.time()
                            send_package(self._sock, 0, self._secret.encrypt(b"firewall;conn=all"))
                            time.sleep(1)
                            message_sent = False
                            while 7 > wait:
                                if all_conn == "nothing":
                                    if not message_sent:
                                        sock.send(json.dumps({"status": "error", "message": "no connections"}).encode("utf-8"))
                                        message_sent = True
                                    break
                                else:
                                    package = []
                                    list = [value for value in all_conn.split(",") if value]
                                    for add in list:
                                        if add != "":
                                            if "=" in add:
                                                t, ip = add.split("=")
                                                elapsed_time = current_time - float(t)
                                                package.append({"time": f"{int(elapsed_time // 3600):03}:{int((elapsed_time % 3600) // 60):02}:{int(elapsed_time % 60):02}", "ip": ip})
                                    all_conn = ""
                                    if not message_sent:
                                        sock.send(json.dumps({"status": "success", "list": package}).encode("utf-8"))
                                        message_sent = True
                                    break
                                time.sleep(1)
                                wait += 1
                            if not message_sent:
                                sock.send(json.dumps({"status": "error", "message": "no connections"}).encode("utf-8"))
                        except:
                            sock.send(json.dumps({"status": "error", "message": "tunnel error"}).encode("utf-8"))
                    else:
                        sock.send(json.dumps({"status": "error", "message": "unknown args"}).encode("utf-8"))
                elif r.startswith("ban"):
                    try:
                        if a1[:2] != "AS":
                            if "/" not in str(a1):
                                a1 = a1 + "/32"
                        if str(a1) not in nat_banned_ips:
                            send_package(self._sock, 0, self._secret.encrypt(b"firewall;ban="+str(a1).encode("utf-8")))
                            nat_banned_ips.append(str(a1))
                            if a1[:2] == "AS":
                                sock.send(json.dumps({"status": "success", "message": "asn banned"}).encode("utf-8"))
                            else:
                                sock.send(json.dumps({"status": "success", "message": "address banned"}).encode("utf-8"))
                        else:
                            if a1[:2] == "AS":
                                sock.send(json.dumps({"status": "error", "message": "asn already banned"}).encode("utf-8"))
                            else:
                                sock.send(json.dumps({"status": "error", "message": "address already banned"}).encode("utf-8"))
                    except:
                        sock.send(json.dumps({"status": "error", "message": "wrong argument"}).encode("utf-8"))
                elif r.startswith("priory"):
                    try:
                        if is_ip(a1):
                            if "/" not in str(a1):
                                a1 = a1 + "/32"
                            send_package(self._sock, 0, self._secret.encrypt(b"firewall;priory="+str(a1).encode("utf-8")))
                            if str(a1) in nat_priory:
                                nat_priory.remove(str(a1))
                                sock.send(json.dumps({"status": "success", "message": "removed from priory"}).encode("utf-8"))
                            else:
                                nat_priory.append(str(a1))
                                sock.send(json.dumps({"status": "success", "message": "added to priory"}).encode("utf-8"))
                        else:
                            sock.send(json.dumps({"status": "error", "message": "invalid ip address"}).encode("utf-8"))
                    except:
                        sock.send(json.dumps({"status": "error", "message": "wrong argument"}).encode("utf-8"))
                elif r.startswith("unban"):
                    try:
                        if a1 != "":
                            send_package(self._sock, 0, self._secret.encrypt(b"firewall;unban="+str(a1).encode("utf-8")))
                            if str(a1) in nat_banned_ips:
                                nat_banned_ips.remove(str(a1))
                            if str(a1)+"/32" in nat_banned_ips:
                                nat_banned_ips.remove(str(a1)+"/32")
                            if a1[:2] == "AS":
                                sock.send(json.dumps({"status": "success", "message": "asn unbanned"}).encode("utf-8"))
                            else:
                                sock.send(json.dumps({"status": "success", "message": "address unbanned"}).encode("utf-8"))
                        else:
                            sock.send(json.dumps({"status": "error", "message": "unknown arguments"}).encode("utf-8"))
                    except:
                        sock.send(json.dumps({"status": "error", "message": "wrong argument"}).encode("utf-8"))
                elif r.startswith("rule"):
                    try:
                        if a1 in ("tor", "vpn"):
                            if a2 == "yes" or a2 == "no":
                                send_package(self._sock, 0, self._secret.encrypt(b"edit_rule;"+str(a1).encode("utf-8")+b"="+str(a2).encode("utf-8")))
                                sock.send(json.dumps({"status": "success", f"message": f"value {a1} changed to {a2}"}).encode("utf-8"))
                        elif a1 == "rate":
                            if a2 in ("0", "1", "2", "3", "4", "5"):
                                send_package(self._sock, 0, self._secret.encrypt(b"firewall;rate="+a2.encode("utf-8")))
                                sock.send(json.dumps({"status": "success", "message": "rate changed"}).encode("utf-8"))
                            else:
                                sock.send(json.dumps({"status": "error", "message": "wrong firewall rate"}).encode("utf-8"))
                        else:
                            sock.send(json.dumps({"status": "error", "message": "wrong arguments"}).encode("utf-8"))
                    except:
                        sock.send(json.dumps({"status": "error", "message": "wrong argument"}).encode("utf-8"))
                else:
                    sock.send(json.dumps({"status": "error", "message": "unknown command"}).encode("utf-8"))
            elif data["version"] == "mtunn_cch1":
                if data["command"]["execute"] == "forwarding":
                    sock.send(json.dumps({"remote": str(explore_domain)+":"+str(explore_port), "local": str(tunnel_two)}).encode("utf-8"))
            else:
                sock.send(b"x01x07")
        sock.close()

def main():
    # mtunn class with params
    global debug, colors, bandwidth, ping_method, compression, potato_mode, explore_port, explore_domain
    global tunnel_domain, tunnel_address, support_ipv4, support_ipv6, main_worker, packet_loss, current_os
    if colors:
        description = "Using «\033[01;34mmake tunnel\033[0m» you can easily open ports for HTTPS, HTTP and TCP. Use the commands from the help menu to configure the tunnel."
    else:
        description = "Using «make tunnel» you can easily open ports for HTTPS, HTTP and TCP. Use the commands from the help menu to configure the tunnel."
    parser = argparse.ArgumentParser(add_help=False, description=description)
    base_options = parser.add_argument_group("Base options")
    base_options.add_argument("--help", action="help", help="show this help message and exit")
    base_options.add_argument("--update", help="update «make tunnel» to latest version", action="store_true")
    base_options.add_argument("--account", help="sign up or log in to an account on the selected server", action="store_true")
    base_options.add_argument("--version", help="displays the currently installed version of the tunnels", action="store_true")

    tunnel_options = parser.add_argument_group("Other options")
    tunnel_options.add_argument("--debug", help="fully enable debug mode in tunnels", action="store_true")
    tunnel_options.add_argument("--minimal", help="reduces the load on the system in tunnels, good for potatoes", action="store_true")
    tunnel_options.add_argument("--console", help="opens a console to manage active tunnels in the local network", action="store_true")
    tunnel_options.add_argument("--bufsize", metavar="<s>", help="changes the system buffer size to improve performance", type=int)
    tunnel_options.add_argument("--fastrun", metavar="<a>", help="launches a temporary TCP tunnel with short configuration", type=str)
    tunnel_options.add_argument("--config", metavar=" <f>", help="launches a configured tunnel from a configuration file", type=str)
    args = parser.parse_args()
    del description
    if args.debug:
        debug = True
    if args.minimal:
        potato_mode = True
    if args.update:
        # update mtunn to the latest version
        printf(sys.executable+" -m pip install --upgrade mtunn --quiet")
        sp.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "mtunn", "--quiet"])
        printf(sys.executable+" -m pip install --upgrade lockis --quiet")
        sp.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "lockis", "--quiet"])
        printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;34mINFO\033[0m ] successfully updated to the latest version")
        sys.exit(0)
    elif args.version:
        # show current version of mtunn
        if colors and build in ("stable", "nature"):
            print(f"\033[01;32m"+version+" "+build+"\033[0m (python "+str(sys.version_info.major)+"."+str(sys.version_info.minor)+")")
        else:
            print(version+f" "+build+" (python "+str(sys.version_info.major)+"."+str(sys.version_info.minor)+")")
        sys.exit(0)
    elif args.bufsize:
        # change to new buffer size
        is_android: bool = hasattr(sys, "getandroidapilevel")
        if not is_android and current_os in ("linux", "freebsd", "netbsd", "openbsd"):
            if int(args.bufsize) >= 32768 and int(args.bufsize) <= 2097152:
                if os.geteuid() == 0:
                    set_net(int(args.bufsize))
                else:
                    print(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] superuser rights are required")
                    sys.exit(0)
            else:
                printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] invalid buffer size")
                sys.exit(0)
        else:
            printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;34mINFO\033[0m ] your system does not need to change the system buffer")
            sys.exit(0)
    elif args.console:
        available_text = []
        available_port = []

        def console_menu(stdscr, options):
            # console select server menu (only for console)
            curses.curs_set(0)
            selected_index = 0
            while True:
                stdscr.clear()

                stdscr.addstr(1, 2, "Use the ↑ and ↓ keys to select which entry is highlighted.", curses.A_BOLD)
                stdscr.addstr(2, 2, "Please select a remote console to control it.", curses.A_BOLD)
                for i, option in enumerate(options):
                    x = 4
                    y = 4 + i
                    mark = "*" if i == selected_index else " "
                    stdscr.addstr(y, x, f"{mark} {option}")

                stdscr.refresh()
                key = stdscr.getch()

                if key == curses.KEY_UP and selected_index > 0:
                    selected_index -= 1
                elif key == curses.KEY_DOWN and selected_index < len(options) - 1:
                    selected_index += 1
                elif key == ord('\n'):
                    stdscr.refresh()
                    return selected_index

        def console_make_package(port, command):
            # build package and send (only for console)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1024)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 2048)
            sock.connect(("127.0.0.1", port))
            command_parts = command.split(" ")
            j = {"version": "mtunn_cv1.3", "command": {"execute": command_parts[0]}}

            for i in range(1, len(command_parts)):
                j["command"][f"args{i}"] = command_parts[i]
            sock.send(json.dumps(j).encode("utf-8"))
            if command != "stop":
                fragments = []
                while True:
                    chunk = sock.recv(1024)
                    fragments.append(chunk)
                    if len(chunk) < 1024:
                        break
                sock.close()
                return b''.join(fragments).decode("utf-8")
            sock.close()
            return "tunnel \033[01;31mstopped\033[0m"

        def console_check_connection(port):
            # check port for running console
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 128)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 256)
                sock.settimeout(0.1)
                sock.connect(("127.0.0.1", port))
                sock.send(json.dumps({"version": "mtunn_cch1", "command": {"execute": "forwarding"}}).encode("utf-8"))
                r = json.loads(sock.recv(128).decode())
                sock.close()
                return {"remote": r["remote"], "local": r["local"], "console": int(p)}
            except:
                return False

        for p in range(7010, 7071):
            try:
                st = console_check_connection(p)
                if st != False:
                    available_text.append(str(p)+": "+st["remote"]+" <-> "+st["local"])
                    available_port.append(str(p))
            except:
                pass

        if available_text == [] and available_port == []:
            print("\033[01;31mno active tunnel found.\033[0m")
            sys.exit(0)
        port = int(available_port[curses.wrapper(console_menu, available_text)])
        if console_check_connection(port) != False:
            print("Welcome to console v1.3 (stable)")
            print("Type “help” to show all commands.")
            while True:
                try:
                    command = str(input(f"\033[01;32mexecute:\033[0m$ "))
                    if command != "":
                        recv = console_make_package(port, command)
                        if recv == "x01x07":
                            print("\033[01;31mError.\033[0m Your console version is not supported")
                            break
                        else:
                            if command == "stop":
                                print("Connection closed by remote host")
                                break
                            if "{" in recv and "}" in recv:
                                recv = json.loads(recv)
                                if recv["status"] == "success":
                                    print("status  : \033[01;32msuccess\033[0m")
                                    if command == "latency":
                                        print("address : "+str(recv["address"]))
                                        print("method  : "+str(recv["method"]))
                                        print("time    : "+str(recv["time"]))
                                    elif command == "threads":
                                        print("total   : "+str(recv["total"]))
                                        print("threads : ")
                                        for s in sorted(recv["threads"]):
                                            print("  "+str(s))
                                    elif command == "forward":
                                        print("remote  : "+str(recv["remote"]))
                                        print("local   : "+str(recv["local"]))
                                    elif command == "status":
                                        print("tunnel  : "+str(recv["tunnel"]))
                                    elif command == "network":
                                        print("used    : "+str(recv["used"]))
                                        print("max     : "+str(recv["max"]))
                                    elif command == "quota":
                                        print("message : update in "+str(recv["quota"])+" day(s)")
                                    elif command == "list":
                                        if recv["list"] == []:
                                            print("message : list is empty")
                                        else:
                                            for pr in recv["list"]:
                                                print(" "+pr)
                                    elif command[:4] == "conn":
                                        if recv["list"] == []:
                                            print("message : list is empty")
                                        else:
                                            for pr in recv["list"]:
                                                print(pr["time"]+" "+pr["ip"])
                                    else:
                                        print("message : "+recv["message"])
                                else:
                                    print("status  : \033[01;31merror\033[0m")
                                    try:
                                        print("message : "+recv["message"])
                                    except:
                                        pass
                            else:
                                print(recv)
                except:
                    break
        else:
            print(f"no tunnels found")
    elif args.account:
        path = mtunn_path()
        if path == None:
            printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] could not find the directory to store the auth file")
            sys.exit(0)
        if not ipv():
            printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] failed to check ipv* connectivity")
            sys.exit(0)
        token = ""
        main_server = ""
        ee = ""
        try:
            with open(path, "r") as file:
                data = [value for value in file.read().split("\n") if value]
            token = data[0]
            ee = data[1]
            main_server = data[2]
            del data
        except:
            if not tos_pp(colors):
                sys.exit(0)
            tun = []
            hst = []
            r = tunnels()
            for pr in r[0]: tun.append(pr)
            for pr in r[1]: hst.append(pr)
            index = curses.wrapper(menu, tun, 2)
            main_server = hst[index]
            if certs(main_server, 5)["verified"] == "no":
                printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] failed to verify server")
                sys.exit(0)
            if verify_server["lockis"] != lockis.version():
                printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] too old version of «lockis»")
                sys.exit(0)
            curses.wrapper(register, path, main_server)
            try:
                with open(path, "r") as file:
                    data = [value for value in file.read().split("\n") if value]
                token = data[0]
                ee = data[1]
                main_server = data[2]
                del data
            except:
                pass
            if token == "" or main_server == "" or ee == "":
                printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] corrupted auth file")
                if Path(path).exists():
                    os.remove(path)
                sys.exit(0)
        verify_server = certs(main_server, 5)
        if verify_server["verified"] == "yes":
            if verify_server["lockis"] != lockis.version():
                printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] too old version of «lockis»")
                sys.exit(0)
            try:
                message = rpost(f"https://{main_server}:5569/auth/verify_token", json_data={"token": token, "email": ee}, timeout=5)["response"]["message"]
            except:
                printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] failed to check account token")
                sys.exit(0)
            if message != "x03":
                printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] corrupted or wrong auth file, restart please")
                if Path(path).exists():
                    os.remove(path)
                sys.exit(0)
        else:
            printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] failed to update server certificate")
            sys.exit(0)
        index = curses.wrapper(menu, ["View my account", "Change account token", "Change account email", "Change to new quota", "Replenish the balance", "Quit from account", "Delete account"], 1)
        if index == 0:
            curses.wrapper(account, path)
        elif index == 1:
            _t = ""
            _e = ""
            with open(path, "r") as file:
                data = [value for value in file.read().split("\n") if value]
            _t = data[0]
            _e = data[1]
            main_server = data[2]
            del data
            if _t == "" or _e == "":
                printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] invalid auth file")
                sys.exit(0)
            post = rpost(f"https://{main_server}:5569/auth/change_token", json_data={"token": _t, "email": _e}, timeout=5)["response"]
            if post["status"] == "success" and "token:" in post["message"]:
                with open(path, "w") as file:
                    file.write(post["message"].replace("token:", "")+"\n")
                    file.write(_e+"\n")
                    file.write(main_server)
                printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;34mINFO\033[0m ] token changed")
            else:
                printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] "+post["message"])
        elif index == 2:
            curses.wrapper(change_email, path)
        elif index == 3:
            curses.wrapper(change_quota, path)
        elif index == 4:
            with open(path, "r") as file:
                data = [value for value in file.read().split("\n") if value]
            token = data[0]
            email = data[1]
            main_server = data[2]
            del data
            post = rpost(f"https://{main_server}:5569/auth/quota_price", json_data={"token": token, "email": email}, timeout=5)["response"]
            if post:
                printf("total quota price: "+str(round(post["total"], 2))+str(post["symbol"]))
            try:
                sure = str(input("Replenish the balance? (y/n): "))
            except:
                sure = "n"
            if sure == "y" or sure == "Y" or sure == "Yes" or sure == "yes":
                post = rpost(f"https://{main_server}:5569/auth/replenish_balance", json_data={"type": "discord"}, timeout=5)["response"]
                if post["status"] == "success":
                    printf(str(post["message"]))
                else:
                    printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] failed to get payment")
            else:
                printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;34mINFO\033[0m ] cancelled")
        elif index == 5:
            if Path(path).exists():
                os.remove(path)
            printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;34mINFO\033[0m ] success")
        elif index == 6:
            curses.wrapper(delete_account, path)
    elif args.fastrun:
        printf(": press CTRL+C to fully stop tunnel")
        printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;34mINFO\033[0m ] preparation for launch")
        run = None
        protocol = None
        target_port = None
        tunnel_port = None
        is_android: bool = hasattr(sys, 'getandroidapilevel')
        printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;34mINFO\033[0m ] checking your ipv* connectivity ...", False)
        if not ipv():
            printf("\033[01;31mfail\033[0m")
            sys.exit(0)
        printf("\033[01;32mdone\033[0m")
        if not is_android and current_os in ("linux", "freebsd", "netbsd", "openbsd"):
            printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;34mINFO\033[0m ] checking system buffer size")
            r, s = get_net()
            if r != 0 and r < 262144:
                printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;33mWARN\033[0m ] your system has too small recv buffer, which may reduce the tunnel speed")
            if s != 0 and s < 131072:
                printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;33mWARN\033[0m ] your system has too small send buffer, which may reduce the tunnel speed")
        matches = re.findall(r'proto:(\w+)|from:(\d+)|to:(\d+)', str(args.fastrun))
        for match in matches:
            if match[0]: protocol = match[0]
            elif match[1]: target_port = int(match[1])
            elif match[2]: tunnel_port = int(match[2])
        if protocol == None or target_port == None or tunnel_port == None:
            printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] invalid arguments")
            sys.exit(0)
        if protocol not in ("https", "http", "tcp"):
            printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] invalid tunnel protocol")
            sys.exit(0)
        path = mtunn_path()
        printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;34mINFO\033[0m ] obtaining the path to the auth file ...", False)
        if path == None:
            printf("\033[01;31mfail\033[0m")
            sys.exit(0)
        printf("\033[01;32mdone\033[0m")
        if os.path.isfile(path):
            with open(path, "r") as file:
                data = [value for value in file.read().split("\n") if value]
            tt = data[0]
            ee = data[1]
            main_server = data[2]
            del data
        else:
            printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] failed to read authentification file")
            sys.exit(0)
        printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;34mINFO\033[0m ] verifying \033[01;33mtls\033[0m certs and account token ...", False)
        verify_server = certs(main_server, 5)
        if verify_server["verified"] == "no":
            printf("\033[01;31mfail\033[0m")
            printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] failed to check server tls certificate")
            sys.exit(0)
        if verify_server["lockis"] != lockis.version():
            printf("\033[01;31mfail\033[0m")
            printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] too old version of «lockis»")
            sys.exit(0)
        try:
            post = rpost(f"https://{main_server}:5569/auth/verify_token", json_data={"token": tt, "email": ee}, timeout=5)["response"]
        except:
            printf(f"\033[01;31mfail\033[0m")
            printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] failed to connect to the server")
            sys.exit(0)
        if post["message"] != "x03":
            printf(f"\033[01;31mfail\033[0m")
            printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] corrupted or wrong auth file")
            if Path(path).exists():
                os.remove(path)
            sys.exit(0)
        printf("\033[01;32mdone\033[0m")
        if is_android:
            arch = str(platform.uname().machine)
            name = str(getpass.getuser())
        else:
            arch = str(platform.uname().machine)
            name = str(socket.gethostname())
        tunnel_domain = main_server
        printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;34mINFO\033[0m ] resolving current tunnel domain (github)")
        if support_ipv6:
            tunnel_address = resolve_tunnel(tunnel_domain, "AAAA")
        else:
            tunnel_address = resolve_tunnel(tunnel_domain, "A")
        if tunnel_address == None:
            printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] failed to resolve tunnel domain")
            sys.exit(0)
        whitelist = []
        try:
            whitelist.append(rget("https://ipinfo.io/?token=ecbdc84059119b", timeout=5)["response"]["country"])
        except:
            pass
        explore_domain = str(tunnel_domain)
        explore_port = str(tunnel_port)
        arguments = {
            'colors': colors,
            'primary': str(main_server),
            'proxy_bind': '',
            'proxy_port': tunnel_port,
            'target_host': '127.0.0.1',
            'target_port': target_port,
            'allow_tor': 'no',
            'allow_vpn': 'yes',
            'blacklist': [],
            'whitelist': whitelist,
            'lowdelay': 'no',
            'compress': 'no',
            'console': 'no',
            'server': tunnel_domain,
            'domain': tunnel_domain,
            'buffer': 262144,
            'token': tt,
            'proto': protocol,
            'rate': 3,
            'arch': arch,
            'name': name,
        }
        printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;34mINFO\033[0m ] executing tunnel with threads")
        signal.signal(signal.SIGINT, exit_system)
        while main_worker:
            if server_status in ("offline", "reconnecting"):
                if is_running_first:
                    main_worker = True
                    run = Client(**arguments)
                    run.start()
                else:
                    run = Client(**arguments)
                    run.start()
                while run._running:
                    time.sleep(0.1)
                run.stop()
                if loop_command:
                    break
                time.sleep(11)
        sys.exit(0)
    elif args.config:
        printf(": press CTRL+C to fully stop tunnel")
        printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;34mINFO\033[0m ] preparation for launch")
        is_android: bool = hasattr(sys, 'getandroidapilevel')
        run = None
        printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;34mINFO\033[0m ] checking your ipv* connectivity ...", False)
        if not ipv():
            printf(f"\033[01;31mfail\033[0m")
            sys.exit(0)
        printf(f"\033[01;32mdone\033[0m")
        printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;34mINFO\033[0m ] reading tunnel configuration file ...", False)
        try:
            schema = {"proto": {}, "target": {}, "tunnel": {}, "domain": {}, "console": {}, "firewall": {"whitelist": {}, "blacklist": {}, "services": {"vpn": {}, "tor": {}}, "protection": {"level": {}}}, "network": {"lowdelay": {}, "bandwidth": {}, "data": {"compression": {}, "algorithm": {}}, "socket": {"buffer": {}}}, "ping": {"method": {}}}
            if not Path(str(args.config)).exists():
                printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] not config file found")
            cfg = parse_yaml(str(args.config))
            if not validate_config:
                printf(f"\033[01;31mfail\033[0m")
                raise SystemExit
            if not ipaddress.ip_address(str(cfg["target"].split(":")[0])).is_private:
                printf(f"\033[01;31mfail\033[0m")
                printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] non-private ip specified in «target»")
                raise SystemExit
            blist = cfg["firewall"]["blacklist"]
            if not isinstance(blist, list):
                printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;33mWARN\033[0m ] invalid arguments «blacklist» in «firewall», skipping list")
                blist = []
            wlist = cfg["firewall"]["whitelist"]
            if not isinstance(wlist, list):
                printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;33mWARN\033[0m ] invalid arguments «whitelist» in «firewall», skipping list")
                wlist = []
            if cfg["network"]["data"]["compression"]:
                compression = str(cfg["network"]["data"]["algorithm"])
                if compression not in ("zlib", "gzip"):
                    printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;33mWARN\033[0m ] wrong arguments «algorithm» in «data», skipping")
                    compression = "no"
            else:
                compression = "no"
            pm = cfg["ping"]["method"]
            if pm not in ("icmp", "tcp"):
                printf(f"\033[01;31mfail\033[0m")
                printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] bad arguments «method» in «ping»")
                raise SystemExit
            if shutil.which("ping") is None and pm == "icmp":
                printf(f"\033[01;31mfail\033[0m")
                printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;33mWARN\033[0m ] ping command not installed")
                raise SystemExit
            if cfg["network"]["lowdelay"]:
                lowdelay = "yes"
            else:
                lowdelay = "no"
            units = {"B": 1, "KB": 1024, "MB": 1024 ** 2, "GB": 1024 ** 3, "TB": 1024 ** 4}
            if str(cfg["network"]["bandwidth"]) == "nolimit":
                bandwidth = -1
            else:
                if " " in str(cfg["network"]["bandwidth"]):
                    value, from_unit = str(cfg["network"]["bandwidth"]).split(" ")
                else:
                    printf(f"\033[01;31mfail\033[0m")
                    printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] invalid unit of measurement «bandwidth» in «network»")
                    raise SystemExit
                if from_unit not in units:
                    printf(f"\033[01;31mfail\033[0m")
                    printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] unknown unit of measurement “{from_unit}”")
                    raise SystemExit

                bandwidth = int((int(value) * units[from_unit]) / units["B"])
                if bandwidth < 1024:
                    printf(f"\033[01;31mfail\033[0m")
                    printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] too small bandwidth, minimum 1 KB")
                    raise SystemExit
            if " " in str(cfg["network"]["socket"]["buffer"]):
                value, from_unit = str(cfg["network"]["socket"]["buffer"]).split(" ")
            else:
                printf(f"\033[01;31mfail\033[0m")
                printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] invalid unit of measurement «buffer» in «socket»")
                raise SystemExit
            if from_unit not in units:
                printf(f"\033[01;31mfail\033[0m")
                printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] unknown unit of measurement “{from_unit}”")
                raise SystemExit

            buffer = int((int(value) * units[from_unit]) / units["B"])
            if buffer < 262144:
                printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] too small buffer, min 256KB")
                raise SystemExit
            if buffer > 2097152:
                printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] too big buffer, max 2MB")
                raise SystemExit
            protocol = str(cfg["proto"])
            if protocol not in ("https", "http", "tcp"):
                printf(f"\033[01;31mfail\033[0m")
                printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] unknown tunnel protocol")
                raise SystemExit
        except SystemExit:
            sys.exit(0)
        except:
            printf(f"\033[01;31mfail\033[0m")
            sys.exit(0)
        printf(f"\033[01;32mdone\033[0m")
        printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;34mINFO\033[0m ] obtaining the path to the auth file ...", False)
        path = mtunn_path()
        if path == None:
            printf(f"\033[01;31mfail\033[0m")
            sys.exit(0)
        printf(f"\033[01;32mdone\033[0m")
        if os.path.isfile(path):
            with open(path, "r") as file:
                data = [value for value in file.read().split("\n") if value]
            tt = data[0]
            ee = data[1]
            main_server = data[2]
            del data
        else:
            printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] failed to read authentification file")
            sys.exit(0)
        printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;34mINFO\033[0m ] verifying \033[01;33mtls\033[0m certs and account token ...", False)
        verify_server = certs(main_server, 5)
        if verify_server["verified"] == "no":
            printf(f"\033[01;31mfail\033[0m")
            printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] failed to check server tls certificate")
            sys.exit(0)
        if verify_server["lockis"] != lockis.version():
            printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] too old version of «lockis»")
            sys.exit(0)
        ccmp = "no"
        try:
            post = rpost(f"https://{main_server}:5569/auth/verify_token", json_data={"token": tt, "email": ee}, timeout=5)["response"]
        except:
            printf(f"\033[01;31mfail\033[0m")
            printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] failed to connect to the server")
            sys.exit(0)
        if post["message"] != "x03":
            printf(f"\033[01;31mfail\033[0m")
            printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] corrupted or wrong auth file")
            if Path(path).exists():
                os.remove(path)
            sys.exit(0)
        printf(f"\033[01;32mdone\033[0m")
        if not is_android and current_os in ("linux", "freebsd", "netbsd", "openbsd"):
            r, s = get_net()
            if r != 0 and s != 0:
                if r < buffer:
                    printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;33mWARN\033[0m ] your system has too small recv buffer, which may reduce the tunnel speed")
                if s < buffer // 2:
                    printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;33mWARN\033[0m ] your system has too small send buffer, which may reduce the tunnel speed")
        target = cfg["target"]
        target_port = int(target[target.index(":")+1:])
        target_address = target[:target.index(":")]
        if cfg["firewall"]["services"]["tor"] != "allow" and cfg["firewall"]["services"]["tor"] != "deny":
            printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;33mWARN\033[0m ] invalid arguments «tor» in «firewall», using default «false»")
            tor = "no"
        else:
            if cfg["firewall"]["services"]["tor"] == "allow": tor = "yes"
            else: tor = "no"
        if cfg["firewall"]["services"]["vpn"] != "allow" and cfg["firewall"]["services"]["vpn"] != "deny":
            printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;33mWARN\033[0m ] invalid arguments «vpn» in «firewall», using default «false»")
            vpn = "no"
        else:
            if cfg["firewall"]["services"]["vpn"] == "allow": vpn = "yes"
            else: vpn = "no"
        if is_android:
            arch = str(platform.machine())
            name = str(getpass.getuser())
        else:
            arch = str(platform.machine())
            name = str(socket.gethostname())
        tunnel = cfg["tunnel"]
        if tunnel and target:
            ping_method = pm
            del pm
            try:
                tunnel_port = int(tunnel)
            except:
                printf(f"\033[01;36m" + str(time.strftime("%H:%M:%S")) + f"\033[0m [\033[01;31mERROR\033[0m] bad tunnel port in config")
                sys.exit(0)
            tunnel_domain = main_server
            printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;34mINFO\033[0m ] resolving current tunnel domain (github)")
            if support_ipv6:
                tunnel_address = resolve_tunnel(tunnel_domain, "AAAA")
            else:
                tunnel_address = resolve_tunnel(tunnel_domain, "A")
            if tunnel_address == None:
                printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] failed to resolve tunnel domain")
                sys.exit(0)
            custom_domain = cfg["domain"]
            if custom_domain == None or custom_domain == "none":
                custom_domain = str(tunnel_domain)
            else:
                printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;34mINFO\033[0m ] resolving custom domain (dns)")
                if support_ipv6:
                    record = resolve_domain(custom_domain, "AAAA")
                else:
                    record = resolve_domain(custom_domain, "A")
                if record == "":
                    printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] failed to resolve domain")
                    sys.exit(0)
                if record != tunnel_address:
                    printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] domain not connected")
                    printf(f"it was not possible to create a tunnel because the domain on the A or AAAA record\ndoes not point to the ip “"+tunnel_address+"”")
                    sys.exit(0)
            if cfg["console"] != True and cfg["console"] != False:
                printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;33mWARN\033[0m ] invalid arguments in «console», using default «false»")
                console = "no"
            else:
                if cfg["console"]:
                    console = "yes"
                else:
                    console = "no"
            if tunnel_domain != custom_domain:
                start_thread(check_domain, [custom_domain])
            explore_domain = str(custom_domain)
            explore_port = str(tunnel_port)
            arguments = {
                'colors': colors,
                'primary': str(main_server),
                'proxy_bind': "",
                'proxy_port': tunnel_port,
                'target_host': target_address,
                'target_port': target_port,
                'allow_tor': tor,
                'allow_vpn': vpn,
                'blacklist': blist,
                'whitelist': wlist,
                'lowdelay': lowdelay,
                'compress': compression,
                'console': console,
                'server': tunnel_domain,
                'domain': custom_domain,
                'buffer': buffer,
                'token': tt,
                'proto': protocol,
                'rate': int(cfg["firewall"]["protection"]["level"]),
                'arch': arch,
                'name': name,
            }
            printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;34mINFO\033[0m ] executing tunnel with threads")
        else:
            printf(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] bad config file")
            sys.exit(0)

        signal.signal(signal.SIGINT, exit_system)
        while main_worker:
            if server_status in ("offline", "reconnecting"):
                if is_running_first:
                    main_worker = True
                    run = Client(**arguments)
                    run.start()
                else:
                    run = Client(**arguments)
                    run.start()
                while run._running:
                    time.sleep(0.1)
                run.stop()
                if loop_command:
                    break
                time.sleep(11)
        sys.exit(0)
    else:
        parser.print_help()

if __name__ == '__main__':
    init()
    configs()
    main()
else:
    sys.tracebacklimit = 0
    raise ImportError("you can't import this as a module")
