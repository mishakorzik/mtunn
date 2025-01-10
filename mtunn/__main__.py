#!/usr/bin/python3
r"""
                __              __                             .__
  _____ _____  |  | __ ____   _/  |_ __ __  ____   ____   ____ |  |
 /     \\__  \ |  |/ // __ \  \   __\  |  \/    \ /    \_/ __ \|  |
|  Y Y  \/ __ \|    <\  ___/   |  | |  |  /   |  \   |  \  ___/|  |__
|__|_|  (____  /__|_ \\___  >  |__| |____/|___|  /___|  /\___  >____/
      \/     \/     \/    \/                   \/     \/     \/

 Дякую за використання цього модуля для відкриття портів!
 Якщо знайдете хибу у коді будь ласка повідомте! Буду вдячний :D

 Переваги:
  01. Потужний захист від DDoS-атак, включаючи розширені механізми фільтрації трафіку.
  02. Оптимізована багатопотокова обробка для роботи з великими обсягами трафіку.
  03. Інтуїтивно зрозумілий інтерфейс для управління TCP-тунелями та налаштування портів.
  04. Надійна система NAT-пробивання для зручного доступу до пристроїв у локальній мережі.
  05. Автоматичний перезапуск тунелів для забезпечення безперервного з'єднання.
  06. Інтеграція з API для автоматизації створення та управління тунелями.
  07. Можливість роботи з динамічними IP-адресами для гнучкої маршрутизації.
  08. Підтримка роботи через протоколи IPv4 та IPv6 (подвійний стек).
  09. Безпечна консоль для управління активними з'єднаннями та їх статусом у реальному часі.
  10. Підтримка QoS (Quality of Service) для пріоритизації трафіку критичних застосунків.

 he1zen networks.
 copyring © 2024. All rights reserved.
"""

try:
    import subprocess as sp
    import os, sys, time, platform, threading, signal, argparse, curses, shutil, re, base64
    import socket, json, ipaddress, zlib, yaml, requests, itertools, ctypes, gzip, struct
    from cryptography.x509 import load_pem_x509_certificate
    from cryptography.hazmat.primitives.asymmetric import padding
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.serialization import PublicFormat, Encoding
    from cryptography.hazmat.backends import default_backend
    from concurrent.futures import ThreadPoolExecutor
    from pathlib import Path
except Exception as e:
    import subprocess, platform, sys
    if "curses" in str(e):
        if platform.system() == "Windows":
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "windows-curses>=2.4.0"])
                print("“windows-curses” has been successfully installed")
                print("please run «mtunn» again")
            except subprocess.CalledProcessError as e:
                print(f"error occurred while installing “windows-curses”: {e}")
        else:
            print("error occurred module curses not found")
    elif "requests" in str(e):
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "requests>=2.25.0"])
            print("“requests” has been successfully installed")
            print("please run «mtunn» again")
        except subprocess.CalledProcessError as e:
            print(f"error occurred while installing “requests”: {e}")
    elif "yaml" in str(e):
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "PyYAML>=6.0.1"])
            print("“PyYaml” has been successfully installed")
            print("please run «mtunn» again")
        except subprocess.CalledProcessError as e:
            print(f"error occurred while installing “PyYaml”: {e}")
    elif "ipaddress" in str(e):
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "ipaddress>=1.0.21"])
            print("“ipaddress” has been successfully installed")
            print("please run «mtunn» again")
        except subprocess.CalledProcessError as e:
            print(f"error occurred while installing “ipaddress”: {e}")
    elif "cryptography" in str(e):
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "cryptography>=3.2"])
            print("“cryptography” has been successfully installed")
            print("please run «mtunn» again")
        except subprocess.CalledProcessError as e:
            print(f"error occurred while installing “cryptography”: {e}")
    else:
        print(str(e))
    sys.exit(0)

if platform.system() == "Windows":
    current_ss_cert = str(Path(__file__).resolve().parent)+r"\cert.pem"
else:
    current_ss_cert = str(Path(__file__).resolve().parent)+"/cert.pem"
if not os.path.exists(current_ss_cert):
    with open(current_ss_cert, 'w'):
        pass

version = '1.2.3'
build = 'stable'

global debug
global colors
global bandwidth
global latest_conn
global ping_method
global nat_banned_ips
global support_ipv4
global support_ipv6
global compression
global saved_network
global connections
global max_network
global used_network
global stunnel_traffic
global tunnels_hostname
global tunnels_address
global tunnel_traffic
global tunnel_max_c
global tunnel_domain
global tunnel_address
global tunnel_total
global tunnel_conn
global tunnel_one
global tunnel_two
global quota_new
global server_version
global server_build
global old_message
global show_message
global message_one
global message_two
global status
global latency
global pk_loss
global ppp

st_t = 0
debug = True
colors = False
bandwidth = -1
latest_conn = ""
conections = 1
if shutil.which("ping"): ping_method = "icmp"
else: ping_method = "tcp"
tunnel_max_c = "0"
tunnel_total = "0"
saved_network = 0
compression = False
compressed_network = 0
quota_new = "-"
max_network = "-"
used_network = 0
connections = 0
tunnel_conn = 0
tunnel_traffic = 0
stunnel_traffic = 0
tunnels_hostname = []
tunnels_address = []
tunnels_domain = []

def init_colors():
    global colors
    if platform.system() == "Windows":
        if str(os.system('')) == "0":
            colors = True
    elif platform.system() == "Linux":
        colors = True

def print_s(text):
    global debug, colors
    if colors == False:
        text = text.replace("\033[0m", "")
        text = text.replace("\033[01;31m", "")
        text = text.replace("\033[01;32m", "")
        text = text.replace("\033[01;33m", "")
        text = text.replace("\033[01;34m", "")
        text = text.replace("\033[01;35m", "")
        text = text.replace("\033[01;36m", "")
        text = text.replace("\033[01;37m", "")
    if debug == True:
        print(text)

def build_dns_query(domain, record_type):
    transaction_id = 0x1234
    flags = 0x0100
    questions = 1
    answer_rrs = 0
    authority_rrs = 0
    additional_rrs = 0
    header = struct.pack(">HHHHHH", transaction_id, flags, questions, answer_rrs, authority_rrs, additional_rrs)
    domain_parts = domain.split(".")
    query_body = b"".join(struct.pack("B", len(part)) + part.encode() for part in domain_parts) + b"\x00"
    query_type = struct.pack(">H", record_type)

    query_class = struct.pack(">H", 1)
    return header + query_body + query_type + query_class

def parse_dns_response(response):
    transaction_id, flags, questions, answer_rrs, authority_rrs, additional_rrs = struct.unpack(">HHHHHH", response[:12])
    offset = 12
    for _ in range(questions):
        while response[offset] != 0:
            offset += 1
        offset += 5

    results = []
    for _ in range(answer_rrs):
        offset += 2
        record_type, record_class, ttl, data_length = struct.unpack(">HHIH", response[offset:offset + 10])
        offset += 10

        if record_type == 1:  # A record (IPv4)
            ip = ".".join(map(str, response[offset:offset + 4]))
            results.append(ip)
        elif record_type == 28:  # AAAA record (IPv6)
            ip = ":".join(f"{response[offset + i]:02x}{response[offset + i + 1]:02x}" for i in range(0, 16, 2))
            results.append(ip)
        offset += data_length
    return results

def send_dns_query(domain, dns_server, record_type):
    query = build_dns_query(domain, record_type)
    is_ipv6 = ":" in dns_server
    family = socket.AF_INET6 if is_ipv6 else socket.AF_INET
    with socket.socket(family, socket.SOCK_DGRAM) as sock:
        sock.settimeout(5)
        sock.sendto(query, (dns_server, 53))
        response = sock.recvfrom(1024)[0]
    return parse_dns_response(response)

def _tunnels():
    global tunnels_hostname
    global tunnels_address
    global tunnels_domain
    try:
        response = requests.get("https://raw.githubusercontent.com/mishakorzik/mtunn/refs/heads/main/tunnels.json", timeout=10).json()
        hostname = []
        for tunnel in response["tunnels"]:
            latency = -1
            supported_types = ""
            try:
                tunnel_ip = tunnel["ip4"]
                if supported_types == "": supported_types += "ipv4"
                else: supported_types += ",ipv4"
            except:
                pass
            try:
                tunnel_ip = tunnel["ip6"]
                if support_ipv6 != True:
                    tunnel_ip = tunnel["ip4"]
                if supported_types == "": supported_types += "ipv6"
                else: supported_types += ",ipv6"
            except:
                pass
            if support_ipv6 == True:
                tunnels_address.append(tunnel_ip)
            else:
                tunnels_address.append(tunnel["ip4"])
            for _ in range(3):
                is_fail = True
                if "ipv6" in supported_types and support_ipv6 == True:
                    try:
                        latency += float(ping.ipv6(tunnel_ip)[:-2])
                    except:
                        latency -= 1
                else:
                    try:
                        latency += float(ping.ipv4(tunnel_ip)[:-2])
                    except:
                        latency -= 1
            latency = str(round(latency / 3))+"ms"
            tunnels_domain.append(tunnel["hostname"])
            hostname.append(tunnel["hostname"])
            tunnels_hostname.append({"tunnel": tunnel["hostname"], "types": str(supported_types), "latency": str(latency)})
        return (tunnels_hostname, hostname)
    except Exception as e:
        print(e)
        print("tunnel config error")
        sys.exit(0)

def _resolve_tunnel(tunnel, method="A"): # resolve tunnel domain using github
    try:
        get = requests.get("https://raw.githubusercontent.com/mishakorzik/mtunn/refs/heads/main/tunnels.json", timeout=10).json()["tunnels"]
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

def _resolve_domain(domain, method="A"): # resolve domain using dns
    if method == "A":
        for dns in ["8.8.8.8", "1.1.1.1", "9.9.9.9", "208.67.222.222", "94.140.14.1"]:
            try:
                return send_dns_query(domain, dns, 1)[0]
            except:
                pass
    elif method == "AAAA":
        for dns in ["2001:4860:4860::8888", "2606:4700:4700::1111", "2620:fe::fe", "2620:119:35::35", "2a10:50c0::ad1:ff"]:
            try:
                return send_dns_query(domain, dns, 28)[0]
            except:
                pass
    return None

def _certs(main_server): # check server status and ssl certificate
    try:
        post = requests.post(f"https://{main_server}:5569/status", headers=headers, timeout=10, json={"id": 0}, verify=current_ss_cert).json()
        if post["*"] == "ok":
            return True
        else:
            return False
    except requests.exceptions.SSLError:
        try:
            get = requests.get(f"https://raw.githubusercontent.com/mishakorzik/mtunn/refs/heads/pages/certs/{main_server}.txt", timeout=10).text
            with open(current_ss_cert, "w") as file:
                file.write(get)
            post = requests.post(f"https://{main_server}:5569/status", headers=headers, timeout=10, json={"id": 0}, verify=current_ss_cert).json()
            if post["*"] == "ok":
                return True
            else:
                return False
        except:
            return False
    except requests.exceptions.ConnectionError:
        return False

def mtunn_path(): # config file locations
    if platform.system() == "Windows":
        if os.path.exists("C:\\") and os.path.isdir("C:\\"):
            path = "C:\\mtunn-auth.hz"
        elif os.path.exists("D:\\") and os.path.isdir("D:\\"):
            path = "D:\\mtunn-auth.hz"
        elif os.path.exists("E:\\") and os.path.isdir("E:\\"):
            path = "E:\\mtunn-auth.hz"
        elif os.path.exists("F:\\") and os.path.isdir("F:\\"):
            path = "F:\\mtunn-auth.hz"
        elif os.path.exists("G:\\") and os.path.isdir("G:\\"):
            path = "G:\\mtunn-auth.hz"
        return path
    elif platform.system() == "Linux":
        path = str(Path(os.getenv("XDG_CONFIG_HOME", Path.home() / ".config")))
        os.makedirs(path, exist_ok=True)
        return path + "/mtunn-auth.hz"
    elif platform.system() in ("OpenBSD", "FreeBSD", "NetBSD", "Darwin"):
        os.makedirs("/etc", exist_ok=True)
        return "/etc/mtunn-auth.hz"
    else:
        return None

def is_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except:
        return False

def is_root(): # only for windows
    try:
        if ctypes.windll.shell32.IsUserAnAdmin() == 1:
            return True
        else:
            return False
    except:
        return False

def menu(stdscr, options, type):
    if curses.has_colors():
        curses.start_color()
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
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
            stdscr.refresh()
            return selected_index

def account(stdscr, headers, path):
    with open(path, "r") as file:
        data = file.read().split("\n")
        try: data.remove("")
        except: pass
        token = data[0]
        email = data[1]
        main_server = data[2]
    post = requests.post(f"https://{main_server}:5569/auth/regdate", headers=headers, timeout=10, json={"email": email}, verify=current_ss_cert).json()
    if post["status"] == "success" and "rd:" in post["message"]:
        date = post["message"].replace("rd:", "")
    else:
        date = "unknown"
    post = requests.post(f"https://{main_server}:5569/auth/quota", headers=headers, timeout=10, json={"token": token}, verify=current_ss_cert).json()
    if post["status"] == "success":
        payouts = str(post["payouts"])
    else:
        payouts = "?"
    post = requests.post(f"https://{main_server}:5569/auth/get_quota", headers=headers, timeout=10, json={"token": token}, verify=current_ss_cert).json()
    if post["status"] == "success":
        connections, tunnels, network, ports = post["message"].split(" ")
    else:
        connections = "?"
        tunnels = "?"
        network = "?"
        ports = "?"
    spinner = ['⠋', '⠙', '⠹', '⠼', '⠴', '⠦', '⠧', '⠏']
    end_time = time.time() + 5
    curses.curs_set(0)
    stdscr.clear()
    if curses.has_colors():
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    for symbol in itertools.cycle(spinner):
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
    stdscr.addstr(7, 0, f" connections      : {connections}")
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

def delete_account(stdscr, headers, path):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    stdscr.clear()

    stdscr.addstr(0, 0, "WARNING.", curses.color_pair(3))
    stdscr.addstr(0, 9, "Do you really want to delete all accounts without recovery?")
    stdscr.addstr(1, 0, "All your unused quota on this account will be deleted.")
    stdscr.addstr(3, 0, "To delete account type: “                       ”")
    stdscr.addstr(3, 25, "yes, delete my account.", curses.color_pair(2))
    stdscr.addstr(4, 0, "Delete account?: ")
    stdscr.refresh()

    curses.echo()
    try:
        key = stdscr.getstr(4, 17).decode('utf-8')
    except:
        sys.exit(0)
    curses.noecho()
    if key.lower() == "yes, delete my account.":
        try:
            with open(path, "r") as file:
                data = file.read().split("\n")
                token = data[0]
                email = data[1]
                main_server = data[2]

            post = requests.post(f"https://{main_server}:5569/auth/delete_account", headers=headers, timeout=10, json={"token": token, "email": email}, verify=current_ss_cert).json()
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

def change_email(stdscr, headers, path):
    if curses.has_colors():
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)

    stdscr.clear()
    stdscr.addstr(0, 0, "Changing Email...", curses.color_pair(2))

    try:
        with open(path, "r") as file:
            data = file.read().split("\n")
            try: data.remove("")
            except: pass
            token = data[0]
            old_email = data[1]
            main_server = data[2]
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
    try:
        new_email = stdscr.getstr(2, 22).decode('utf-8')
    except:
        sys.exit(0)
    curses.noecho()

    try:
        post = requests.post(f"https://{main_server}:5569/auth/change_email", headers=headers, json={"new_email": new_email, "old_email": old_email, "token": token}, timeout=10, verify=current_ss_cert).json()
        if post["status"] == "success":
            stdscr.addstr(3, 0, "Enter code from email: ")
            stdscr.refresh()

            curses.echo()
            code = stdscr.getstr(3, 23).decode('utf-8')
            curses.noecho()

            post = requests.post(f"https://{main_server}:5569/auth/verify", headers=headers, json={"email": new_email, "code": code}, timeout=10, verify=current_ss_cert).json()
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

    except requests.RequestException as e:
        stdscr.addstr(4, 0, f"Request failed: {str(e)}", curses.color_pair(3))

    stdscr.addstr(6, 0, "Press 'q' to exit.")
    stdscr.refresh()
    while True:
        key = stdscr.getch()
        if key == ord('q'):
            break

def tos_pp(colors):
    if colors == True:
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

def register(stdscr, headers, path, main_server):
    if curses.has_colors():
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
    line = 4
    stdscr.clear()
    stdscr.addstr(0, 0, "Email Verification", curses.color_pair(2))
    while True:
        stdscr.addstr(2, 0, "Enter your email to verify: ")
        stdscr.refresh()

        curses.echo()
        email = stdscr.getstr(2, 28).decode('utf-8')
        curses.noecho()
        if email in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT] or email == "":
            continue
        else:
            break
    try:
        post = requests.post(f"https://{main_server}:5569/auth/check", headers=headers, json={"email": email}, timeout=10, verify=current_ss_cert).json()
        if post["status"] == "success":
            if post["message"] == "x00x00x01":
                post = requests.post(f"https://{main_server}:5569/auth/register", headers=headers, json={"email": email}, timeout=10, verify=current_ss_cert).json()
            elif post["message"] == "x00x01x03":
                post = requests.post(f"https://{main_server}:5569/auth/login", headers=headers, json={"email": email}, timeout=10, verify=current_ss_cert).json()
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
                    code = stdscr.getstr(3, 23).decode('utf-8')
                    curses.noecho()
                    if code in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT] or code == "":
                        continue
                    else:
                        break
                stdscr.refresh()
                line = 7
                post = requests.post(f"https://{main_server}:5569/auth/verify", headers=headers, json={"email": email, "code": code}, timeout=10, verify=current_ss_cert).json()
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
    except requests.RequestException as e:
        stdscr.addstr(4, 0, f"Request failed: {str(e)}", curses.color_pair(3))

    stdscr.addstr(line, 0, "Press 'q' to exit.")
    stdscr.refresh()
    while True:
        key = stdscr.getch()
        if key == ord('q'):
            break
    sys.exit(1)

def cquota(stdscr, headers, path):
    if curses.has_colors():
        curses.start_color()
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
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
            stdscr.addstr(11, 2, prompt)
            stdscr.refresh()
            user_input = stdscr.getstr(11, len(prompt) + 2, 30).decode()
            curses.noecho()
            stdscr.addstr(11, 2, " " * (len(prompt) + 20))
            return user_input
        except:
            sys.exit(0)

    selected_row = 0
    while True:
        draw_form(stdscr, selected_row)
        key = stdscr.getch()

        if key == curses.KEY_DOWN and selected_row < len(inputs) - 1:
            selected_row += 1
        elif key == curses.KEY_UP and selected_row > 0:
            selected_row -= 1
        elif key == ord('e'):
            field = list(inputs.keys())[selected_row]
            new_value = get_user_input(stdscr, f"Enter {field}: ")
            inputs[field] = new_value or inputs[field]
        elif key == ord('c'):
            break
        elif key == ord('q'):
            exit(255)

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
        post = requests.post(f"https://{main_server}:5569/auth/count_quota", headers=headers, timeout=10, json={"conn": conn, "tunn": tunn, "netw": netw, "prun": tta}, verify=current_ss_cert).json()
    except requests.RequestException:
        stdscr.addstr(11, 0, "Failed to connect to server", curses.A_BOLD)
        stdscr.getch()
        return

    netw = netw * 1024 * 1024 * 1024
    if post.get("status") == "success":
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
            key = stdscr.getstr(4, 19).decode('utf-8')
        except:
            sys.exit(0)
        curses.noecho()
        if key.lower() == "yes, accept.":
            try:
                post = requests.post(f"https://{main_server}:5569/auth/change_quota", headers=headers, timeout=10, json={"token": token, "conn": conn, "tunn": tunn, "netw": netw, "prun": prun}, verify=current_ss_cert).json()
                if post.get("status") == "success":
                    stdscr.addstr(6, 0, "Quota changed successfully.", curses.A_BOLD)
                    stdscr.addstr(7, 0, "Press 'q' to exit.")
                else:
                    stdscr.addstr(6, 0, "Failed to change quota.", curses.A_BOLD)
                    stdscr.addstr(7, 0, str(post["message"]).capitalize(), curses.A_BOLD)
                    stdscr.addstr(8, 0, "Press 'q' to exit.")
            except requests.RequestException:
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

pk_loss = 0
explore_port = 0
explore_domain = ""
tunnel_one = ''
tunnel_two = ''
server_build = ''
server_version = ''
headers = {"User-Agent": f"request/{requests.__version__} (mtunn v{version} {build}; {str(platform.python_version())}) {str(platform.machine())}"}
latency = '-'
status = '\033[01;31moffline\033[0m'
show_message = True

class units:
    def count(value):
        number, unit = value.split()
        return int(number) * {"B": 1, "KB": 1024, "MB": 1048576, "GB": 1073741824}[unit]

def update_msg(stdscr, protocol):
    global pk_loss
    global pk_colr
    global tunnel_conn
    global show_message
    global saved_network
    global explore_domain
    global stunnel_traffic
    global used_network
    global max_network
    global quota_new
    global st_t
    if curses.has_colors():
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.curs_set(0)
    stdscr.nodelay(True)
    space = " "*30
    while show_message:
        try:
            line = 2
            max_y, max_x = stdscr.getmaxyx()
            del max_y
            start_x = max_x - 20
            stdscr.addstr(0, 0, " "*max_x)
            stdscr.addstr(0, 0, "mtunn    ", curses.color_pair(3))
            stdscr.addstr(0, start_x, "(press 'q' to close) ")
            if status == "online":
                stdscr.addstr(line, 0, f"Status")
                stdscr.addstr(line, 30, status+space, curses.color_pair(1))
            else:
                stdscr.addstr(line, 0, f"Status")
                stdscr.addstr(line, 30, status+space, curses.color_pair(4))
            line += 1
            stdscr.addstr(line, 0, f"Version                       {version} {build}"+space)
            if server_version != version:
                line += 1
                stdscr.addstr(line, 0, f"Update                        update available ({server_version})"+space, curses.color_pair(2))
            line += 1
            if latency == "-":
                stdscr.addstr(line, 0, f"Latency                       -"+space)
            else:
                if float(latency.replace("ms", "")) >= 200:
                    stdscr.addstr(line, 0, f"Latency                       {latency} (")
                    stdscr.addstr(line, 32+len(latency), f"bad", curses.color_pair(4))
                    stdscr.addstr(line, 35+len(latency), f")"+space)
                elif float(latency.replace("ms", "")) >= 100:
                    stdscr.addstr(line, 0, f"Latency                       {latency} (")
                    stdscr.addstr(line, 32+len(latency), f"average", curses.color_pair(2))
                    stdscr.addstr(line, 39+len(latency), f")"+space)
                else:
                    stdscr.addstr(line, 0, f"Latency                       {latency} (")
                    stdscr.addstr(line, 32+len(latency), f"good", curses.color_pair(1))
                    stdscr.addstr(line, 36+len(latency), f")"+space)
            if status == "online":
                if stunnel_traffic > 1024: # KBytes
                    if stunnel_traffic > 1048576: # MBytes
                        if stunnel_traffic > 1073741824: # GBytes
                            if stunnel_traffic > 1099511627776: # TBytes
                                tt = str(round(stunnel_traffic / 1024 / 1024 / 1024 / 1024, 3))+" TB/s"
                            else:
                                tt = str(round(stunnel_traffic / 1024 / 1024 / 1024, 3))+" GB/s"
                        else:
                            tt = str(round(stunnel_traffic / 1024 / 1024, 3))+" MB/s"
                    else:
                        tt = str(round(stunnel_traffic / 1024, 3))+" KB/s"
                else:
                    tt = str(stunnel_traffic)+" B/s"
                line += 1
                stdscr.addstr(line, 0, f"Network usage                 {tt}"+space)
            else:
                if max_network == "-":
                    tt = "-"
                else:
                    tt = "0 B/s"
                stunnel_traffic = 0
                line += 1
                stdscr.addstr(line, 0, f"Network usage                 -"+space)
            if pk_loss >= 100:
                pk_loss = 100
            line += 1
            if int(pk_loss) >= 1:
                stdscr.addstr(line, 0, f"Packet loss                   {str(pk_loss)} percent(%)"+space , curses.color_pair(2))
            else:
                stdscr.addstr(line, 0, f"Packet loss                   {str(pk_loss)} percent(%)"+space)
            line += 1
            stdscr.addstr(line, 0, f"Forwarding")
            stdscr.addstr(line, 30, protocol, curses.color_pair(5))
            stdscr.addstr(line, 30+len(protocol), f"://{explore_domain}:{str(explore_port)}"+space)
            line += 1
            stdscr.addstr(line, 0, f"                               └─ ")
            stdscr.addstr(line, 34, protocol, curses.color_pair(5))
            stdscr.addstr(line, 34+len(protocol), f"://{tunnel_two}          ")
            line += 1
            stdscr.addstr(line, 0, f"                                                       ")
            line += 1
            if int(tunnel_conn) >= round(int(connections) / 1.4):
                if int(tunnel_conn) >= round(int(connections) / 1.05):
                    stdscr.addstr(line, 0, f"Connections                   active, ")
                    stdscr.addstr(line, 38, f"{str(tunnel_conn)}", curses.color_pair(4))
                    stdscr.addstr(line, 38+len(str(tunnel_conn)), f"/{str(connections)}"+space)
                else:
                    stdscr.addstr(line, 0, f"Connections                   active, ")
                    stdscr.addstr(line, 38, f"{str(tunnel_conn)}", curses.color_pair(2))
                    stdscr.addstr(line, 38+len(str(tunnel_conn)), f"/{str(connections)}"+space)
            else:
                stdscr.addstr(line, 0, f"Connections                   active, ")
                stdscr.addstr(line, 38, f"{str(tunnel_conn)}", curses.color_pair(1))
                stdscr.addstr(line, 38+len(str(tunnel_conn)), f"/{str(connections)}"+space)
            line += 1
            stdscr.addstr(line, 0, f"Active tunnels                total, {tunnel_total} ")
            stdscr.addstr(line, 38+len(tunnel_total), f"of ", curses.color_pair(5))
            stdscr.addstr(line, 40+len(tunnel_total), f" {tunnel_max_c}"+space)
            if compression in ["zlib", "gzip"]:
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
                if str(quota_new) == "-1":
                    stdscr.addstr(line, 0, f"Update quota                  now, please wait"+space)
                else:
                    stdscr.addstr(line, 0, f"Update quota                  -"+space)
            else:
                if used_network >= max_network-1048576:
                    st_t = 1
                    show_message = False
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
                if str(quota_new) == "-1":
                    stdscr.addstr(line, 0, f"Update quota                  now, please wait"+space)
                else:
                    stdscr.addstr(line, 0, f"Update quota                  in {quota_new} day(s)"+space)
            line += 1
            stdscr.addstr(line, 0, f"                                                       ")
            stdscr.refresh()
            key = stdscr.getch()
            if key == ord('q'):
                show_message = False
        except curses.error:
            print_s(f"\033[01;36m" + str(time.strftime("%H:%M:%S")) + f"\033[0m [\033[01;31mERROR\033[0m] failed to display the window")
            break

def count_network():
    global stunnel_traffic
    global tunnel_traffic
    global used_network
    while show_message:
        stunnel_traffic = tunnel_traffic
        tunnel_traffic = 0
        time.sleep(1)

def rupdate_msg(protocol):
    curses.wrapper(update_msg, protocol)

def check_domain(custom_domain):
    time.sleep(300)
    global st_t
    global show_message
    global tunnel_address
    global tunnel_domain
    while show_message:
        if tunnel_domain != custom_domain:
            if support_ipv6 == True and isinstance(ipaddress.ip_address(tunnel_address), ipaddress.IPv4Address) == False:
                record = _resolve_domain(custom_domain, "AAAA")
            else:
                record = _resolve_domain(custom_domain, "A")
            if str(record) != str(tunnel_address):
                st_t = 2
                show_message = False
                time.sleep(1)
                print(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] domain not connected")
                print(f"it was not possible to create a tunnel because the domain on the A or AAAA record\ndoes not point to the ip “"+tunnel_address+"”")
                sys.exit(0)
        time.sleep(300)

def update_pk():
    global pk_loss
    global show_message
    while show_message:
        if pk_loss != 0:
             if "online" in status:
                pk_loss = pk_loss - 1
        if "offline" in status:
            pk_loss = 100
        if pk_loss <= 0:
            pk_loss = 0
        if pk_loss >= 100:
            pk_loss = 100
        time.sleep(0.1)

def ping_host():
    global pk_loss
    global latency
    global show_message
    global tunnel_max_c
    time.sleep(2)
    while show_message:
        if "offline" in status:
            latency = "-"
        else:
            if support_ipv6 == True and isinstance(ipaddress.ip_address(tunnel_address), ipaddress.IPv4Address) == False:
                latency = ping.ipv6(tunnel_address)
            else:
                latency = ping.ipv4(tunnel_address)
            time.sleep(3)

def print_it(*args):
    import datetime
    print(datetime.datetime.now(), *args)

def _exit_system(code=0):
    try:
        global status
        global show_message
        global latency
        global pk_loss
        latency = "-"
        pk_loss = 100
        status = "offline"
        time.sleep(2)
        show_message = False
        time.sleep(1)
        os.system("kill -9 "+str(os.getpid()))
        os._exit(code)
    except:
        pass

def exit_system(code=0):
    start_thread(_exit_system, args=[code])

def int_time():
    return int(time.time())

def start_thread(target=None, args=[]):
    try:
        threading.Thread(target=target, args=args, daemon=True).start()
        return True
    except:
        return False

def encrypt_message(message):
    message = str(message)
    with open(current_ss_cert, "rb") as cert_file:
        cert_data = cert_file.read()
    certificate = load_pem_x509_certificate(cert_data, backend=default_backend())
    public_key = certificate.public_key()
    encrypted_message = public_key.encrypt(
        message.encode('utf-8'),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted_message

def make_package(target, data):
    global compression, saved_network
    if isinstance(data, str):
        data = data.encode()
    comp = b'0'
    if len(data) >= 256:
        if compression == "zlib":
            compress = zlib.compress(data, level=1)
            if len(data)-10 > len(compress)+10:
                saved_network += len(data) - len(compress)
                data = compress
                comp = b'1'
        elif compression == "gzip":
            compress = gzip.compress(data)
            if len(data)-10 > len(compress)+10:
                saved_network += len(data) - len(compress)
                data = compress
                comp = b'2'
    return str(target).encode() + b'L' + comp + b'F' + data

def parse_package(package=b''):
    global saved_network
    d = package.index(b'L')
    t = int(package[0:d])
    c = package.index(b'F')
    comp = package[d + 1:c]
    data = package[c + 1:]
    if comp == b'1':
        decompress = zlib.decompress(data)
        saved_network += len(decompress) - len(data)
        data = decompress
    elif comp == b'2':
        decompress = gzip.decompress(data)
        saved_network += len(decompress) - len(data)
        data = decompress
    return t, data

def sock_read(sock, buffer):
    global pk_loss
    recv = b''
    if sock:
        try: recv = sock.recv(buffer)
        except: pass
    return recv

def sock_send(sock, data, lk):
    global pk_loss
    if isinstance(data, str):
        data = data.encode()
    if sock:
        try:
            with lk:
                sock.sendall(memoryview(data))
            return True
        except:
            return False
    return False

_sock_io_map = {}

def read_package(sock, buffer=units.count("16 KB")):
    global pk_loss
    global tunnel_traffic
    global bandwidth
    if not sock:
        return
    if bandwidth != -1:
        if tunnel_traffic > bandwidth:
            time.sleep(1)
    sockid = int(id(sock))
    if sockid not in _sock_io_map:
        _sock_io_map[sockid] = SockIO(sock)
    try:
        package = _sock_io_map[sockid].recv(buffer)
        if not package:
            return None
        data = parse_package(package)
        if data[0] != 0:
            tunnel_traffic += len(package)
        if data:
            return data[0], data[1]
    except:
        pk_loss += 5
    return None

def send_package(sock, ix, data):
    global pk_loss
    global tunnel_traffic
    global bandwidth
    if not sock:
        return
    if bandwidth != -1 and ix != 0:
        if tunnel_traffic > bandwidth:
            time.sleep(1)
    sockid = int(id(sock))
    if sockid not in _sock_io_map:
        _sock_io_map[sockid] = SockIO(sock)
    try:
        package = make_package(ix, data)
        if ix != 0:
            tunnel_traffic += len(package)
        return _sock_io_map[sockid].send(package)
    except:
        pk_loss += 5
    return None

def sock_close(sock, shut=False):
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
    global ping_method
    def ipv4(host, timeout=3):
        latency = "-"
        if ping_method == "tcp":
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.settimeout(timeout)
                    start_time = time.time()
                    sock.connect((host, 5570))
                    sock.send(b'i')
                    if sock.recv(1) == b'o':
                        latency = str(round(((time.time() - start_time) / 3) * 1000, 1)) + "ms"
                    sock.close()
            except:
                pass
        elif ping_method == "icmp":
            if platform.system() == "Windows":
                try:
                    result = sp.run(["ping", "-4", host, "-w", str(timeout)+"000", "-n", "1"], capture_output=True, text=True, check=True)
                    ms = re.search(r"time[=<]\s*(\d+)\s*ms", result.stdout)
                    if ms:
                        latency = str(round(float(ms.group(1)), 1)) + "ms"
                except:
                    pass
            else:
                try:
                    output = sp.check_output(["ping", "-c", "1", "-W", str(timeout), host], universal_newlines=True)
                    ms = re.search(r"time=(\d+\.?\d*) ms", output)
                    if ms:
                        latency = str(round(float(ms.group(1)), 1)) + "ms"
                except:
                    pass
        return latency

    def ipv6(host, port=5570, timeout=3):
        latency = "-"
        if ping_method == "tcp":
            try:
                for _, _, _, _, sockaddr in socket.getaddrinfo(host, 5570, socket.AF_INET6, socket.SOCK_STREAM):
                    with socket.socket(socket.AF_INET6, socket.SOCK_STREAM) as sock:
                        sock.settimeout(timeout)
                        start_time = time.time()
                        sock.connect(sockaddr)
                        sock.send(b'i')
                        if sock.recv(1) == b'o':
                            latency = str(round(((time.time() - start_time) / 3) * 1000, 1)) + "ms"
                        sock.close()
            except:
                pass
        elif ping_method == "icmp":
            if platform.system() == "Windows":
                try:
                    result = sp.run(["ping", "-6", host, "-w", str(timeout)+"000", "-n", "1"], capture_output=True, text=True, check=True)
                    ms = re.search(r"time[=<]\s*(\d+)\s*ms", result.stdout)
                    if ms:
                        latency = str(round(float(ms.group(1)), 1)) + "ms"
                except:
                    pass
            else:
                try:
                    output = sp.check_output(["ping6", "-c", "1", "-W", str(timeout), host], universal_newlines=True)
                    ms = re.search(r"time=(\d+\.?\d*) ms", output)
                    if ms:
                        latency = str(round(float(ms.group(1)), 1)) + "ms"
                except:
                    pass
        return latency

class PackageIt(object):
    head = b'DH'  # 2 bytes
    leng = b':'   # 1 byte
    buffer = bytearray()

    def feed(self, data):
        if isinstance(data, str):
            data = data.encode()
        self.buffer.extend(data)

    def recv(self):
        hix = self.buffer.find(self.head)
        if hix >= 0:
            lix = self.buffer.find(self.leng, hix + 2)
            if lix > 0:
                try:
                    lns = int(self.buffer[hix + 2: lix])
                    pend = lix + 1 + lns
                    if len(self.buffer) >= pend:
                        data = self.buffer[lix + 1:pend]
                        del self.buffer[:pend]
                        return data
                except ValueError:
                    del self.buffer[:hix + 2]
        return None

    def make(self, data):
        if isinstance(data, str):
            data = data.encode()
        return self.head + str(len(data)).encode() + self.leng + data

class SockIO(object):
    def __init__(self, sock):
        self.pi = PackageIt()

        self.recv_lock = threading.Lock()
        self.send_lock = threading.Lock()

        self.sock = sock
        self.sock.setblocking(True)
        self.sock.settimeout(0.5)
        assert sock

    def recv(self, buffer):
        with self.recv_lock:
            while True:
                data = self.pi.recv()
                if data is None:
                    try:
                        r = self.sock.recv(buffer)
                        if not r:
                            return None
                        self.pi.feed(r)
                    except (BlockingIOError, socket.timeout):
                        break
                else:
                    break
            return data

    def send(self, data):
        pack = self.pi.make(data)
        with self.send_lock:
            try:
                self.sock.sendall(memoryview(pack))
                return True
            except (socket.error, BrokenPipeError):
                return False

    def close(self):
        self.sock.close()

class Base(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.starttime = int_time()

class Runable(Base):
    _thread = None
    _running = False

    def __str__(self):
        import os

    def _log(self, msg, *args):
        print_it(self, msg, *args)

    def _run(self):
        pass

    def _start_run(self):
        self._run()
        self._running = False

    def start(self):
        if not self._running:
            self._running = True
            th = start_thread(target=self._start_run)
            self._thread = th
            return th

    def stop(self):
        self._running = False

    _dog_runing = False
    _dog_last = 0

    def _dog_run(self):
        global status, latency, tunnel_conn, max_network, pk_loss
        self._dog_last = int_time()
        while self._dog_runing:
            now = int_time()
            if (now - self._dog_last) > 7:
                status = "offline"
                tunnel_conn = 0
                max_network = '-'
                latency = '-'
                self.stop()
            time.sleep(1)

    def stop_dog(self):
        self._dog_runing = False

    def start_dog(self):
        self._dog_runing = True
        start_thread(self._dog_run)

    def feed_dog(self):
        self._dog_last = int_time()

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
    proxy_port = 10000
    proxy_bind = '0.0.0.0'
    additional = False
    reconnect = 'no'
    domain = ''
    proto = ''
    name = ''
    _lock = threading.Lock()
    _athread = None
    _client_map = {}
    if platform.system() in ("OpenBSD", "FreeBSD", "NetBSD", "Linux"): additional = True

    def _run_con(self, ix, sock):
        buffer_size = units.count("8 KB")
        while self._running:
            recv = sock_read(sock, buffer_size)
            if recv:
                if len(recv) == buffer_size:
                    if buffer_size + units.count("8 KB") >= units.count("512 KB"):
                        buffer_size = units.count("512 KB")
                    else:
                        buffer_size += units.count("8 KB")
                else:
                    if buffer_size - units.count("2 KB") >= units.count("8 KB"):
                        buffer_size -= units.count("2 KB")
                    else:
                        buffer_size = units.count("8 KB")
                send_package(self._sock, ix, recv)
            else:
                try: send_package(self.sock, -1 * ix, b'close')
                except: pass
                time.sleep(1)
                sock_close(sock)
                break

    def _add_con(self, ix):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, 96)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, units.count("512 KB"))
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, units.count("512 KB"))
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            if self.additional:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
                sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_CORK, 0)
                if self.low_delay == "yes":
                    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_QUICKACK, 1)
                    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                else:
                    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_QUICKACK, 0)
                    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 0)
            else:
                if self.low_delay == "yes":
                    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                else:
                    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 0)
            sock.connect((self.target_host, self.target_port), )
            self._client_map[ix] = {'sock': sock, 'lock': threading.Lock(), 'th': start_thread(target=self._run_con, args=[ix, sock])}
            return self._client_map[ix]
        except:
            pass

    def _del_con(self, data, ix):
        with self._lock:
            nix = abs(ix)
            if nix in self._client_map:
                if not data or data == b'close':
                    d = self._client_map[nix]
                    sock_close(d['sock'])
                    del self._client_map[nix]

    def _run_ucheck(self):
        time.sleep(300)
        global server_build
        global server_version
        while self._running:
            try:
                post = requests.post(f"http://{self.primary}:5569/version", headers=headers, timeout=10, json={"type": "latest"}, verify=current_ss_cert).json()
                server_version = str(post["version"])
                server_build = str(post["build"])
            except:
                time.sleep(30)
            time.sleep(600)

    def _run_ping(self):
        global st_t
        while self._running:
            send_package(self._sock, 0, b'p;')
            if st_t == 1:
                print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] all data used.")
                self.stop(False)
                break
            elif st_t == 2:
                self.stop()
                break
            time.sleep(1)

    def _run(self):
        if self.console == "yes":
            start_thread(target=self.remote)
            self.console = "no"
        global status, tunnel_two, compression
        global server_version, server_build, connections, tunnel_max_c, tunnel_total, saved_network
        global used_network, max_network, tunnel_traffic, tunnel_conn, latest_conn, quota_new
        compression = self.compress
        tunnel_two = f"{self.target_host}:{self.target_port}"
        self.start_dog()
        try:
            if support_ipv6 == True and isinstance(ipaddress.ip_address(tunnel_address), ipaddress.IPv4Address) == False:
                if self.reconnect == "no":
                    print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;34mINFO\033[0m ] \033[01;32mconnecting\033[0m with IPv6")
                    self.reconnect = "yes"
                else:
                    print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;34mINFO\033[0m ] \033[01;33mreconnecting\033[0m with IPv6")
                sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
                sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_UNICAST_HOPS, 96)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, units.count("512 KB"))
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, units.count("512 KB"))
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                if self.additional:
                    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
                    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_CORK, 0)
                    if self.low_delay == "yes":
                        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_QUICKACK, 1)
                        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                    else:
                        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_QUICKACK, 0)
                        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 0)
                else:
                    if self.low_delay == "yes":
                        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                    else:
                        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 0)
                sock.connect((tunnel_address, 5567))
                self._sock = sock
            else:
                if self.reconnect == "no":
                    print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;34mINFO\033[0m ] \033[01;32mconnecting\033[0m with IPv4")
                    self.reconnect = "yes"
                else:
                    print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;34mINFO\033[0m ] \033[01;33mreconnecting\033[0m with IPv4")
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, 96)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, units.count("512 KB"))
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, units.count("512 KB"))
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                if self.additional:
                    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
                    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_CORK, 0)
                    if self.low_delay == "yes":
                        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_QUICKACK, 1)
                        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                    else:
                        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_QUICKACK, 0)
                        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 0)
                else:
                    if self.low_delay == "yes":
                        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                    else:
                        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 0)
                sock.connect((tunnel_address, 5567))
                self._sock = sock
            sd = {
                'version': version,
                'system': {'name': base64.b64encode(encrypt_message(self.name[:25])).decode(), 'arch': base64.b64encode(encrypt_message(self.arch[:10].lower())).decode()},
                'tunnel': {'proto': base64.b64encode(encrypt_message(self.proto)).decode(), 'domain': base64.b64encode(encrypt_message(self.domain)).decode(), 'compression': self.compress, 'low-delay': self.low_delay},
                'firewall': {'rate': self.rate, 'blacklist': self.blacklist, 'whitelist': self.whitelist, 'tor': self.allow_tor, 'vpn': self.allow_vpn},
                'token': base64.b64encode(encrypt_message(self.token)).decode(),
                'port': base64.b64encode(encrypt_message(self.proxy_port)).decode(),
            }
            self.feed_dog()
            send_package(sock, 0, json.dumps(sd))
            time.sleep(1)
            ret = json.loads(read_package(sock)[1])
            if ret["status"] == 1:
                status = "online"
                server_version = str(ret['version'])
                server_build = str(ret['build'])
                tunnel_max_c = str(ret["max_tunnels"])
                used_network = int(ret["used_network"])
                max_network = int(ret["max_network"])
                connections = int(ret["connections"])
                self._athread = ThreadPoolExecutor(max_workers=50+(connections*2))
                start_thread(target=rupdate_msg, args=[self.proto])
                start_thread(target=count_network)
                start_thread(target=update_pk)
                start_thread(target=ping_host)
            elif ret["status"] == 0:
                status = "offline"
                self.stop()
            elif ret["status"] == 4:
                if debug == True:
                    print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] "+str(ret["message"]))
                else:
                    print(str(ret["message"]))
                self.stop()
                exit_system()
                time.sleep(2)
        except:
            status = "offline"
            self.stop()
        self.feed_dog()
        start_thread(target=self._run_ucheck)
        start_thread(target=self._run_ping)
        while self._running:
            try:
                recv = read_package(self._sock)
                if recv:
                    ix, data = recv
                    if ix == 0:
                        if data.startswith(b";"):
                            self.feed_dog()
                            ac, dec, rq, tc = data.decode().replace(";", "").split("/")
                            tunnel_conn = int(tc)
                            tunnel_total = str(ac)
                            quota_new = int(rq)
                            used_network = int(dec)
                        elif data.startswith(b"re;"):
                            latest_conn = data.decode().replace("re;", "")
                    elif ix > 0:
                        if ix not in self._client_map: d = self._add_con(ix)
                        else: d = self._client_map[ix]
                        if d:
                            self._athread.submit(sock_send, d['sock'], data, d['lock'])
                    else:
                        self._athread.submit(self._del_con, data, ix)
            except:
                continue

    def stop(self, s=True):
        global connections
        if s == True:
            send_package(self._sock, 0, b'c;')
        self.stop_dog()
        for d in self._client_map.values():
            sock_close(d['sock'])
        self._client_map.clear()
        if self._athread != None: self._athread.shutdown(wait=False)
        super(Client, self).stop()

    def remote(self):
        global st_t
        global latest_conn
        global ping_method
        global tunnel_address
        global show_message
        global used_network
        global max_network
        global quota_new

        nat_priory = []
        nat_banned_ips = []

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        for port in range(7010, 7091):
            try:
                s.bind(("127.0.0.1", int(port)))
            except:
                pass
        s.listen(1)
        while True:
            run = False
            try:
                sock, addr = s.accept()
                packet = sock.recv(256)
                data = json.loads(packet.decode())
                run = True
            except:
                pass
            if run == True:
                if data["version"] == "mtunn_cv1.0":
                    r = data["command"]
                    if r == "help":
                        sock.send(b"""\033[01;33mCommands:\033[0m
 connection         : show the latest or currently active tunnel connections
 network            : current network usage and maximum network capacity
 forward            : show forwarding information for the tunnel
 latency            : ping a tunnel and get the results in ms
 status             : show the current status of the tunnel
 quota              : display tunnel days remaining until the next quota
 stop               : force the tunnel to stop immediately

\033[01;33mFirewall:\033[0m
 ban <range/ip>     : ban ip/cidr on tunnel
 unban <range/ip>   : unban ip/cidr on tunnel
 priory <range/ip>  : add or remove priory to ip
 rule <a1> <a2>     : update rule in firewall
 list               : list all banned ips

\033[01;33mExamples:\033[0m
 ban 8.8.8.8/32     : specify ip or cidr to block
 unban 8.8.8.8/32   : specify ip or cidr to unblock
 priory 8.8.8.8/32  : adds ip or cidr to priority
 rule rate 1        : change rate in firewall only numbers 0-3
 rule tor no        : block or unblock tor/vpn only (yes/no)""")
                    elif r == 'stop':
                        show_message = False
                        time.sleep(1)
                        print(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;34mINFO\033[0m ] a tunnel stop command was received from the console")
                        st_t = 2
                    elif r == 'latency':
                        if isinstance(ipaddress.ip_address(tunnel_address), ipaddress.IPv4Address) == True:
                            lat = ping.ipv4(tunnel_address)
                        else:
                            lat = ping.ipv6(tunnel_address)
                        sock.send(b'address='+str(tunnel_address).encode('utf-8')+b'\nmethod='+str(ping_method).encode('utf-8')+b'\ntime='+str(lat).encode('utf-8'))
                    elif r == 'forward':
                        sock.send(str(explore_domain).encode('utf-8')+b':'+str(explore_port).encode('utf-8')+b' <-> '+str(tunnel_two).encode('utf-8'))
                    elif r == 'status':
                        if "online" in status:
                            sock.send(b'\033[01;32monline\033[0m')
                        elif "offline" in status:
                            sock.send(b'\033[01;31moffline\033[0m')
                        else:
                            sock.send(status.encode('utf-8'))
                    elif r == 'list':
                        if nat_banned_ips == []:
                            sock.send(b'nothing')
                        else:
                            banned = "banned ips or asn:"
                            for pr in nat_banned_ips:
                                banned = banned + f"\n" + pr
                            sock.send(banned.encode('utf-8'))
                    elif r == 'quota':
                        if str(quota_new) == "-" or str(max_network) == "-":
                            sock.send(b'quota is unknown')
                        else:
                            sock.send(b"in "+str(quota_new).encode("utf-8")+b" day(s)")
                    elif r == 'network':
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
                        sock.send(b'used '+str(_u).encode('utf-8')+b' of '+str(_m).encode('utf-8'))
                    elif r.startswith('connection'):
                        try:
                            wait = 0
                            send_package(self._sock, 0, b'e.n;conn=latest')
                            while 7 > wait:
                                if latest_conn != "nothing" and "." in latest_conn:
                                    package = "recent or active connections"
                                    list = latest_conn.split(",")
                                    try: list.remove("")
                                    except: pass
                                    try: list.remove("")
                                    except: pass
                                    for add in list:
                                        if add != "":
                                            package += "\n " + add
                                    latest_conn = ""
                                    sock.send(package.encode('utf-8'))
                                    break
                                time.sleep(1)
                                wait += 1
                            sock.send(b'no recent or active ips')
                        except:
                            sock.send(b'tunnel error')
                    elif r.startswith('ban'):
                        try:
                            _, ip = r.split(" ")
                            if ip[:2] != "AS":
                                if "/" not in str(ip):
                                    ip = ip + "/32"
                            if str(ip) not in nat_banned_ips:
                                send_package(self._sock, 0, b'e.n;ban='+str(ip).encode('utf-8'))
                                nat_banned_ips.append(str(ip))
                                if ip[:2] == "AS":
                                    sock.send(b'banned asn: '+ip.encode('utf-8'))
                                else:
                                    sock.send(b'banned ip: '+ip.encode('utf-8'))
                            else:
                                sock.send(b'already banned')
                        except:
                            sock.send(b'\033[01;31mwrong arguments\033[0m')
                    elif r.startswith('priory'):
                        try:
                            _, ip = r.split(" ")
                            if is_ip(ip) == True:
                                if "/" not in str(ip):
                                    ip = ip + "/32"
                                send_package(self._sock, 0, b'e.n;priory='+str(ip).encode('utf-8'))
                                if str(ip) in nat_priory:
                                    nat_priory.remove(str(ip))
                                    sock.send(b'removed ip: '+ip.encode('utf-8'))
                                else:
                                    nat_priory.append(str(ip))
                                    sock.send(b'added ip: '+ip.encode('utf-8'))
                            else:
                                sock.send(b'invalid ip')
                        except:
                            sock.send(b'\033[01;31mwrong arguments\033[0m')
                    elif r.startswith('unban'):
                        try:
                            _, ip = r.split(" ")
                            send_package(self._sock, 0, b'e.n;unban='+str(ip).encode('utf-8'))
                            try: nat_banned_ips.remove(str(ip))
                            except: pass
                            if ip[:2] == "AS":
                                sock.send(b'unbanned asn: '+ip.encode('utf-8'))
                            else:
                                sock.send(b'unbanned ip: '+ip.encode('utf-8'))
                        except:
                            sock.send(b'\033[01;31mwrong arguments\033[0m')
                    elif r.startswith('rule'):
                        try:
                            _, var, bool = r.split(" ")
                            if var in ["tor", "vpn"]:
                                if bool == "yes" or bool == "no":
                                    send_package(self._sock, 0, b'e.r;'+str(var).encode('utf-8')+b'='+str(bool).encode('utf-8'))
                                    sock.send(str(var).encode('utf-8')+b' = '+str(bool).encode('utf-8'))
                            elif var == "rate":
                                if bool in ("0", "1", "2", "3", "4", "5"):
                                    send_package(self._sock, 0, b'e.n;rate='+bool.encode('utf-8'))
                                    sock.send(b'\033[01;32msuccess\033[0m')
                                else:
                                    sock.send(b'\033[01;31mwrong\033[0m firewall rate')
                            else:
                                sock.send(b'\033[01;31mwrong arguments\033[0m')
                        except:
                            sock.send(b'\033[01;31mwrong arguments\033[0m')
                elif data["version"] == "mtunn_cv1.0api":
                    r = data["command"]
                    if r == 'stop':
                        show_message = False
                        time.sleep(1)
                        print(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;34mINFO\033[0m ] a tunnel stop command was received from the console")
                        st_t = 2
                    elif r == 'latency':
                        if isinstance(ipaddress.ip_address(tunnel_address), ipaddress.IPv4Address) == True:
                            lat = ping.ipv4(tunnel_address)
                        else:
                            lat = ping.ipv6(tunnel_address)
                        sock.send(json.dumps({"address": str(tunnel_address), "method": str(ping_method), "time": str(lat)}).encode())
                    elif r == 'forward':
                        sock.send(json.dumps({"remote": str(explore_domain)+b":"+str(explore_port), "local": str(tunnel_two)}))
                    elif r == 'status':
                        if "online" in status:
                            sock.send(json.dumps({"status": "online"}).encode())
                        elif "offline" in status:
                            sock.send(json.dumps({"status": "offline"}).encode())
                        else:
                            sock.send(json.dumps({"status": str(status)}).encode())
                    elif r == 'list':
                        if nat_banned_ips == []:
                            sock.send(json.dumps({"list": ""}).encode())
                        else:
                            nb = ""
                            for add in nat_banned_ips:
                                nb += "," + add
                            sock.send(json.dumps({"list": nb.replace(",", "", 1)}).encode())
                    elif r == 'quota':
                        if str(quota_new) == "-" or str(max_network) == "-":
                            sock.send(json.dumps({"quota": "unknown"}).encode())
                        else:
                            sock.send(json.dumps({"quota": str(quota_new)}).encode())
                    elif r == 'network':
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
                        sock.send(json.dumps({"used": str(_u), "max": str(_m)}).encode())
                    elif r.startswith('connection'):
                        try:
                            wait = 0
                            noerr = 1
                            send_package(self._sock, 0, b'e.n;conn=latest')
                            while 7 > wait:
                                if latest_conn != "nothing" and "." in latest_conn:
                                    list = latest_conn.split(",")
                                    try: list.remove("")
                                    except: pass
                                    try: list.remove("")
                                    except: pass
                                    noerr = 0
                                    sock.send(json.dumps({"status": "success", "list": list}).encode())
                                    break
                                time.sleep(1)
                                wait += 1
                            if noerr == 1:
                                sock.send(json.dumps({"status": "error", "message": "no recent or active ips"}).encode())
                        except:
                            sock.send(json.dumps({"status": "error", "message": "wrong arguments"}).encode())
                    elif r.startswith('ban'):
                        try:
                            _, ip = r.split(" ")
                            if ip[:2] != "AS":
                                if "/" not in str(ip):
                                    ip = ip + "/32"
                            if str(ip) not in nat_banned_ips:
                                send_package(self._sock, 0, b'e.n;ban='+str(ip).encode('utf-8'))
                                nat_banned_ips.append(str(ip))
                                if ip[:2] == "AS":
                                    sock.send(json.dumps({"status": "success", "message": "asn banned"}).encode())
                                else:
                                    sock.send(json.dumps({"status": "success", "message": "address banned"}).encode())
                            else:
                                if ip[:2] == "AS":
                                    sock.send(json.dumps({"status": "error", "message": "asn already banned"}).encode())
                                else:
                                    sock.send(json.dumps({"status": "error", "message": "address already banned"}).encode())
                        except:
                            sock.send(json.dumps({"status": "error", "message": "wrong argument"}).encode())
                    elif r.startswith('priory'):
                        try:
                            _, ip = r.split(" ")
                            if is_ip(ip) == True:
                                if "/" not in str(ip):
                                    ip = ip + "/32"
                                send_package(self._sock, 0, b'e.n;priory='+str(ip).encode('utf-8'))
                                if str(ip) in nat_priory:
                                    nat_priory.remove(str(ip))
                                    sock.send(json.dumps({"status": "success", "message": "removed from priory"}).encode())
                                else:
                                    nat_priory.append(str(ip))
                                    sock.send(json.dumps({"status": "success", "message": "added to priory"}).encode())
                            else:
                                sock.send(json.dumps({"status": "error", "message": "invalid ip address"}).encode())
                        except:
                            sock.send(json.dumps({"status": "error", "message": "wrong argument"}).encode())
                    elif r.startswith('unban'):
                        try:
                            _, ip = r.split(" ")
                            send_package(self._sock, 0, b'e.n;unban='+str(ip).encode('utf-8'))
                            try: nat_banned_ips.remove(str(ip))
                            except: pass
                            if ip[:2] == "AS":
                                sock.send(json.dumps({"status": "success", "message": "asn unbanned"}).encode())
                            else:
                                sock.send(json.dumps({"status": "success", "message": "address unbanned"}).encode())
                        except:
                            sock.send(json.dumps({"status": "error", "message": "wrong argument"}).encode())
                    elif r.startswith('rule'):
                        try:
                            _, var, bool = r.split(" ")
                            if var in ["tor", "vpn"]:
                                if bool == "yes" or bool == "no":
                                    send_package(self._sock, 0, b'e.r;'+str(var).encode('utf-8')+b'='+str(bool).encode('utf-8'))
                                    sock.send(json.dumps({"status": "success", f"message": f"value {var} changed to {bool}"}).encode())
                            elif var == "rate":
                                if bool in ("0", "1", "2", "3", "4", "5"):
                                    send_package(self._sock, 0, b'e.n;rate='+bool.encode('utf-8'))
                                    sock.send(json.dumps({"status": "success", "message": "rate changed"}).encode())
                                else:
                                    sock.send(json.dumps({"status": "error", "message": "wrong firewall rate"}).encode())
                            else:
                                sock.send(json.dumps({"status": "error", "message": "wrong arguments"}).encode())
                        except:
                            sock.send(json.dumps({"status": "error", "message": "wrong argument"}).encode())
                elif data["version"] == "mtunn_cch1":
                    if data["command"] == "forwarding":
                        sock.send(str(explore_domain).encode('utf-8')+b':'+str(explore_port).encode('utf-8')+b' <-> '+str(tunnel_two).encode('utf-8'))
                else:
                    sock.send(b'x01x07')
                sock.close()

def main():
    global colors
    global bandwidth
    global ping_method
    global compression
    global explore_port
    global explore_domain
    global tunnel_domain
    global tunnel_address
    global support_ipv4
    global support_ipv6
    global show_message
    global pk_loss
    if colors == True:
        description = "Using «\033[01;34mmake tunnel\033[0m» you can easily open ports for HTTP and TCP. Use the commands from the help menu to configure the tunnel. If you find it difficult to understand these commands, you can refer to our documentation at <\033[01;33mgithub.com/mishakorzik/mtunn\033[0m>, where it is explained in detail how to use it."
    else:
        description = "Using «make tunnel» you can easily open ports for HTTP and TCP. Use the commands from the help menu to configure the tunnel. If you find it difficult to understand these commands, you can refer to our documentation at <github.com/mishakorzik/mtunn>, where it is explained in detail how to use it."
    parser = argparse.ArgumentParser(add_help=True, description=description)
    parser.add_argument('--nodebug', help='completely disables the debug mode', action='store_true')
    parser.add_argument('--version', help='displays the currently installed version of the tunnels', action='store_true')
    parser.add_argument('--account', help='sign up or log in to an account on the selected server', action='store_true')
    parser.add_argument('--console', help='opens a console to manage active tunnels in the local network', action='store_true')
    parser.add_argument('--fastrun', metavar='<args>', help='launches a temporary TCP tunnel with short configuration', type=str)
    parser.add_argument('--config', metavar=' <file>', help='launches a configured tunnel from a configuration file', type=str)
    args = parser.parse_args()
    del description
    if args.nodebug:
        global debug
        debug = False
    if args.version:
        print(version+" "+build)
    elif args.console:
        available_text = []
        available_port = []

        def console_menu(stdscr, options):
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

        def console_make_package(command, port):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(("127.0.0.1", port))
            s.send(json.dumps({"version": "mtunn_cv1.0", "command": command}).encode('utf-8'))
            if command != "stop":
                fragments = []
                while True:
                    chunk = s.recv(1024)
                    fragments.append(chunk)
                    if len(chunk) < 1024:
                        break
                s.close()
                return b''.join(fragments).decode()
            return "tunnel \033[01;31mstopped\033[0m"

        def console_check_connection(port):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.1)
                s.connect(("127.0.0.1", port))
                s.send(json.dumps({"version": "mtunn_cch1", "command": "forwarding"}).encode('utf-8'))
                r = s.recv(96).decode()
                s.close()
                return r
            except:
                return False

        for p in range(7010, 7091):
            try:
                st = console_check_connection(p)
                if st != False and " <-> " in st:
                    available_text.append(str(p) + ": " + str(st))
                    available_port.append(str(p))
            except:
                pass

        if available_text == [] and available_port == []:
            print("\033[01;31mno active tunnel found.\033[0m")
            sys.exit(0)
        port = int(available_port[curses.wrapper(console_menu, available_text)])
        if console_check_connection(port) != False:
            print("Welcome to console v1.1 (stable)")
            print("Type “help” to show all commands.")
            while True:
                try:
                    command = str(input(f"\033[01;32mexecute:\033[0m$ "))
                    if command != "":
                        recv = console_make_package(command, port)
                        if recv == "x01x07":
                            print("\033[01;31mError.\033[0m Your console version is not supported")
                            break
                        else:
                            if command == "stop":
                                print("Connection closed by remote host")
                                break
                            print(recv)
                except:
                    break
        else:
            print(f"no tunnels found")
    elif args.account:
        is_android: bool = hasattr(sys, 'getandroidapilevel')
        if is_android == False:
            if is_root() == False and platform.system() == "Windows":
                print(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] superuser rights are required.")
                sys.exit(0)
        support_ipv4 = False
        support_ipv6 = False
        try: requests.get("http://ipv4.lookup.test-ipv6.com/ip/", timeout=5); support_ipv4 = True
        except:
            try: requests.get("http://v4.ipv6-test.com/api/myip.php", timeout=5); support_ipv4 = True
            except: pass
        try: requests.get("http://ipv6.lookup.test-ipv6.com/ip/", timeout=5); support_ipv6 = True
        except:
            try: requests.get("http://v6.ipv6-test.com/api/myip.php", timeout=5); support_ipv6 = True
            except: pass
        path = mtunn_path()
        if path == None:
            print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] could not find the directory to store the auth file")
            sys.exit(8)
        token = ""
        main_server = ""
        try:
            with open(path, "r") as file:
                data = file.read().split("\n")
                try: data.remove("")
                except: pass
                token = data[0]
                ee = data[1]
                main_server = data[2]
            if _certs(main_server) == True:
                if token == "" or main_server == "":
                    print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] corrupted auth file, restart please")
                    try: os.remove(path)
                    except: pass
                    sys.exit(0)
                else:
                    post = requests.post(f"https://{main_server}:5569/auth/vtoken", headers=headers, timeout=10, json={"token": token, "email": ee}, verify=current_ss_cert).json()
                    if post["message"] != "x00x01x03":
                         print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] corrupted or wrong auth file")
                         try: os.remove(path)
                         except: pass
                         sys.exit(0)
        except:
            if tos_pp(colors) == False:
                sys.exit(0)
            tun = []
            hst = []
            r = _tunnels()
            for pr in r[0]:
                tun.append(pr)
            for pr in r[1]:
                hst.append(pr)
            index = curses.wrapper(menu, tun, 2)
            main_server = hst[index]
            if _certs(main_server) == False:
                print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] failed to verify server")
                sys.exit(9)
            curses.wrapper(register, headers, path, main_server)
        index = curses.wrapper(menu, ["View my account", "Change account token", "Change account email", "Change to new quota", "Replenish the balance", "Quit from account", "Delete account"], 1)
        if index == 0:
            curses.wrapper(account, headers, path)
        elif index == 1:
            _t = ""
            _e = ""
            with open(path, "r") as file:
                data = file.read().split("\n")
                try: data.remove("")
                except: pass
                _t = data[0]
                _e = data[1]
                main_server = data[2]
            if _t == "" or _e == "":
                print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] invalid auth file")
                sys.exit(0)
            post = requests.post(f"https://{main_server}:5569/auth/ctoken", headers=headers, timeout=10, json={"token": _t, "email": _e}, verify=current_ss_cert).json()
            if post["status"] == "success" and "token:" in post["message"]:
                with open(path, "w") as file:
                    file.write(post["message"].replace("token:", "")+"\n")
                    file.write(_e+"\n")
                    file.write(main_server)
                print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;34mINFO\033[0m ] token changed")
            else:
                print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] "+post["message"])
        elif index == 2:
            curses.wrapper(change_email, headers, path)
        elif index == 3:
            curses.wrapper(cquota, headers, path)
        elif index == 4:
            with open(path, "r") as file:
                data = file.read().split("\n")
                try: data.remove("")
                except: pass
                token = data[0]
                main_server = data[2]
            post = requests.post(f"https://{main_server}:5569/auth/quota_price", headers=headers, timeout=10, json={"token": token}, verify=current_ss_cert).json()
            if post:
                print_s("total quota price: "+str(round(post["total"], 2))+str(post["symbol"]))
            sure = str(input("Replenish the balance? (y/n): "))
            if sure == "y" or sure == "Y" or sure == "Yes" or sure == "yes":
                post = requests.post(f"https://{main_server}:5569/auth/rb", headers=headers, timeout=10, json={"*": ""}, verify=current_ss_cert).json()
                if post["status"] == "success":
                    print_s(str(post["message"]))
                else:
                    print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] failed to get payment")
            else:
                print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;34mINFO\033[0m ] cancelled")
        elif index == 5:
            try: os.remove(path)
            except: pass
            print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;34mINFO\033[0m ] success")
        elif index == 6:
            curses.wrapper(delete_account, headers, path)
    elif args.fastrun:
        is_android: bool = hasattr(sys, 'getandroidapilevel')
        if is_android == False:
            if is_root() == False and platform.system() == "Windows":
                print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] superuser rights are required.")
                sys.exit(0)
        support_ipv4 = False
        support_ipv6 = False
        try: requests.get("http://ipv4.lookup.test-ipv6.com/ip/", timeout=5); support_ipv4 = True
        except:
            try: requests.get("http://v4.ipv6-test.com/api/myip.php", timeout=5); support_ipv4 = True
            except: pass
        try: requests.get("http://ipv6.lookup.test-ipv6.com/ip/", timeout=5); support_ipv6 = True
        except:
            try: requests.get("http://v6.ipv6-test.com/api/myip.php", timeout=5); support_ipv6 = True
            except: pass
        run = None
        protocol = None
        target_port = None
        tunnel_port = None
        print_s(": press CTRL+C to fully stop tunnel")
        print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;34mINFO\033[0m ] preparation for launch")
        if int(os.cpu_count()) == 1:
            print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;33mWARN\033[0m ] your processor only has 1 core which may have a high load.")
        matches = re.findall(r'proto:(\w+)|from:(\d+)|to:(\d+)', str(args.fastrun))
        for match in matches:
            if match[0]: protocol = match[0]
            elif match[1]: target_port = int(match[1])
            elif match[2]: tunnel_port = int(match[2])
        if protocol == None or target_port == None or tunnel_port == None:
            print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] invalid arguments")
            sys.exit(0)
        if protocol != "tcp" and protocol != "http" and protocol != "https":
            print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] invalid tunnel protocol")
            sys.exit(0)
        path = mtunn_path()
        if path == None:
            print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] could not find the directory to store the auth file")
            sys.exit(8)
        if os.path.isfile(path):
            with open(path, "r") as file:
                data = file.read().split("\n")
                try: data.remove("")
                except: pass
                tt = data[0]
                ee = data[1]
                main_server = data[2]
        else:
            print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] failed to run tunnel. No auth file")
            sys.exit(0)
        if _certs(main_server) == False:
            print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] failed to check server ssl")
            sys.exit(0)
        try:
            post = requests.post(f"https://{main_server}:5569/auth/vtoken", headers=headers, timeout=10, json={"token": tt, "email": ee}, verify=current_ss_cert).json()
            if post["message"] != "x00x01x03":
                print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] corrupted or wrong auth file")
                try: os.remove(path)
                except: pass
                sys.exit(0)
        except SystemExit:
            sys.exit(0)
        except:
            print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] failed to connect to the server")
            sys.exit(0)
        if is_android == True:
            import getpass
            arch = str(platform.uname().machine)
            name = str(getpass.getuser())
        else:
            arch = str(platform.uname().machine)
            name = str(socket.gethostname())
        tunnel_domain = main_server
        if support_ipv6 == True:
            tunnel_address = _resolve_tunnel(tunnel_domain, "AAAA")
        else:
            tunnel_address = _resolve_tunnel(tunnel_domain, "A")
        if tunnel_address == None:
            print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] failed to resolve tunnel domain")
            sys.exit(0)
        whitelist = []
        try:
            whitelist.append(requests.get("https://ipinfo.io/?token=ecbdc84059119b", timeout=10).json()["country"])
        except:
            pass
        explore_domain = str(tunnel_domain)
        explore_port = str(tunnel_port)
        arguments = {
            'colors': colors,
            'primary': str(main_server),
            'proxy_bind': "",
            'proxy_port': tunnel_port,
            'target_host': "127.0.0.1",
            'target_port': target_port,
            'low_delay': "no",
            'allow_tor': "no",
            'allow_vpn': "yes",
            'blacklist': [],
            'whitelist': whitelist,
            'compress': "no",
            'console': "no",
            'server': tunnel_domain,
            'domain': tunnel_domain,
            'token': tt,
            'proto': protocol,
            'rate': 3,
            'arch': arch,
            'name': name,
        }
        print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;34mINFO\033[0m ] executing tunnel with threads")
        run = Client(**arguments)
        def stop(a, b):
            run.stop()

        signal.signal(signal.SIGINT, exit_system)
        if run:
            while show_message:
                if "offline" in status:
                    try:
                        show_message = False
                        time.sleep(2)
                        show_message = True
                    except:
                        run.stop()
                        sys.exit(1)
                    run.start()
                    try:
                        while run._running:
                            time.sleep(1)
                    except:
                        run.stop()
                        sys.exit(1)
                    time.sleep(2)
    elif args.config:
        is_android: bool = hasattr(sys, 'getandroidapilevel')
        if is_android == False:
            if is_root() == False and platform.system() == "Windows":
                print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] superuser rights are required.")
                sys.exit(0)
        support_ipv4 = False
        support_ipv6 = False
        try: requests.get("http://ipv4.lookup.test-ipv6.com/ip/", timeout=5); support_ipv4 = True
        except:
            try: requests.get("http://v4.ipv6-test.com/api/myip.php", timeout=5); support_ipv4 = True
            except: pass
        try: requests.get("http://ipv6.lookup.test-ipv6.com/ip/", timeout=5); support_ipv6 = True
        except:
            try: requests.get("http://v6.ipv6-test.com/api/myip.php", timeout=5); support_ipv6 = True
            except: pass
        run = None
        print_s(": press CTRL+C to fully stop tunnel")
        print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;34mINFO\033[0m ] preparation for launch")
        if int(os.cpu_count()) == 1:
            print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;33mWARN\033[0m ] your processor only has 1 core which may have a high load.")
        try:
            with open(str(args.config)) as file:
                cfg = yaml.load(file, Loader=yaml.FullLoader)
        except:
            print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] no config file.")
            sys.exit(7)
        try: cfg["proto"]
        except:
            print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] not enough arguments «proto»")
            sys.exit(7)
        path = mtunn_path()
        if path == None:
            print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] could not find the directory to store the auth file")
            sys.exit(8)
        if os.path.isfile(path):
            with open(path, "r") as file:
                data = file.read().split("\n")
                try: data.remove("")
                except: pass
                tt = data[0]
                ee = data[1]
                main_server = data[2]
        else:
            print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] failed to run tunnel. No auth file")
            sys.exit(0)
        if _certs(main_server) == False:
            print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] failed to check server ssl")
            sys.exit(0)
        print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;34mINFO\033[0m ] checking account token")
        ccmp = "no"
        try:
            post = requests.post(f"https://{main_server}:5569/auth/vtoken", headers=headers, timeout=10, json={"token": tt, "email": ee}, verify=current_ss_cert).json()
            if post["message"] != "x00x01x03":
                print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] corrupted or wrong auth file")
                try: os.remove(path)
                except: pass
                sys.exit(0)
        except:
            print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] failed to connect to the server")
            sys.exit(0)
        print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;34mINFO\033[0m ] reading config's files")
        try:
            json.dumps(cfg["firewall"])
            json.dumps(cfg["network"])
            json.dumps(cfg["ping"])
        except:
            print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] corrupted or invalid configuration file")
            sys.exit(7)
        try: int(cfg["tunnel"])
        except:
            print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] wrong or not enough arguments «tunnel»")
            sys.exit(7)
        try:
            h, p = cfg["target"].split(":")
            p = int(p)
            if ipaddress.ip_address(h).is_private == False:
                print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] non-private ip specified in «target»")
                sys.exit(7)
        except (TypeError, ValueError):
            print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] wrong or not enough arguments «target»")
            sys.exit(7)
        try: cfg["domain"]
        except:
            print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] not enough arguments «domain»")
            sys.exit(7)
        try: cfg["console"]
        except:
            print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] not enough arguments «console»")
            sys.exit(7)
        try: int(cfg["firewall"]["protection"]["level"])
        except:
            print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] wrong or not enough arguments «rate» in «firewall»")
            sys.exit(7)
        try: cfg["firewall"]["services"]["vpn"]
        except:
            print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] not enough arguments «vpn» in «firewall»")
            sys.exit(7)
        try: cfg["firewall"]["services"]["tor"]
        except:
            print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] not enough arguments «tor» in «firewall»")
            sys.exit(7)
        try:
            if isinstance(cfg["firewall"]["blacklist"], list):
                blist = cfg["firewall"]["blacklist"]
            else:
                print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;33mWARN\033[0m ] invalid arguments «blist» in «firewall», skipping list")
                blist = []
        except:
            print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;33mWARN\033[0m ] wrong or not enough arguments «blist» in «firewall»")
            blist = []
        try:
            if isinstance(cfg["firewall"]["whitelist"], list):
                wlist = cfg["firewall"]["whitelist"]
            else:
                print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;33mWARN\033[0m ] invalid arguments «wlist» in «firewall», skipping list")
                wlist = []
        except:
            print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;33mWARN\033[0m ] wrong or not enough arguments «wlist» in «firewall»")
            wlist = []
        try:
            compression = cfg["network"]["data"]["compression"]
            if compression == True:
                compression = str(cfg["network"]["data"]["algorithm"])
                if compression not in ["zlib", "gzip"]:
                    print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;33mWARN\033[0m ] wrong arguments «algorithm» in «data»")
                    compression = ""
        except:
            print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;33mWARN\033[0m ] not enough or wrong arguments «compression» in «data»")
            compression = ""
        try:
            if cfg["network"]["low-delay"] == True:
                low_delay = "yes"
            else:
                low_delay = "no"
        except:
            print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;33mWARN\033[0m ] not enough arguments «low-delay» in «network», using default «false»")
            low_delay = "no"
        try: str(cfg["network"]["bandwidth"])
        except:
            print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;33mWARN\033[0m ] not enough arguments «bandwidth» in «network», using default «nolimit»")
            bandwidth = -1
        try:
            pm = cfg["ping"]["method"]
            if pm != "icmp" and pm != "tcp":
                if shutil.which("ping"):
                    print_s(f"\033[01;36m" + str(time.strftime("%H:%M:%S")) + f"\033[0m [\033[01;33mWARN\033[0m ] bad arguments «method» in «ping», using icmp method.")
                    pm = "tcp"
                else:
                    print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;33mWARN\033[0m ] bad arguments «method» in «ping», using tcp method.")
                    pm = "tcp"
            if shutil.which("ping") is None and pm == "icmp":
                print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;33mWARN\033[0m ] ping command not installed, using tcp method.")
                pm = "tcp"
        except:
            if shutil.which("ping"):
                pm = "icmp"
            else:
                pm = "tcp"
        try:
            if str(cfg["network"]["bandwidth"]) == "nolimit":
                bandwidth = -1
            else:
                if " " in str(cfg["network"]["bandwidth"]) and str(cfg["network"]["bandwidth"])[-1:] == "s":
                    value, from_unit = str(cfg["network"]["bandwidth"]).split(" ")
                else:
                    print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] invalid unit of measurement «bandwidth» in «network»")
                    raise SystemExit
                units = {
                    "kbits": (10 ** 3) / 8,
                    "mbits": (10 ** 6) / 8,
                    "gbits": (10 ** 9) / 8,
                    "tbits": (10 ** 12) / 8,

                    "bytes": 1,
                    "kbytes": 1024,
                    "mbytes": 1024 ** 2,
                    "gbytes": 1024 ** 3,
                    "tbytes": 1024 ** 4
                }
                if from_unit not in units:
                    print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] unknown unit of measurement “{from_unit}”")
                    raise SystemExit

                bandwidth = int((int(value) * units[from_unit]) / units["bytes"])
                if bandwidth < 1024:
                    print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] too small bandwidth, min 1 kbytes or 8 kbits")
                    raise SystemExit
        except (NameError, ValueError, KeyError):
            print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] failed to measure units «bandwidth» in «network»")
            sys.exit(7)
        except SystemExit:
            sys.exit(7)
        target = cfg["target"]
        target_port = int(target[target.index(":")+1:])
        target_address = target[:target.index(":")]
        if cfg["firewall"]["services"]["tor"] != "allow" and cfg["firewall"]["services"]["tor"] != "deny":
            print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;33mWARN\033[0m ] invalid arguments «tor» in «firewall», using default «false»")
            tor = "no"
        else:
            if cfg["firewall"]["services"]["tor"] == "allow": tor = "yes"
            else: tor = "no"
        if cfg["firewall"]["services"]["vpn"] != "allow" and cfg["firewall"]["services"]["vpn"] != "deny":
            print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;33mWARN\033[0m ] invalid arguments «vpn» in «firewall», using default «false»")
            vpn = "no"
        else:
            if cfg["firewall"]["services"]["vpn"] == "allow": vpn = "yes"
            else: vpn = "no"
        if is_android == True:
            import getpass
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
                print_s(f"\033[01;36m" + str(time.strftime("%H:%M:%S")) + f"\033[0m [\033[01;31mERROR\033[0m] bad tunnel port in config")
                sys.exit(0)
            tunnel_domain = main_server
            print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;34mINFO\033[0m ] resolving tunnel domain")
            if support_ipv6 == True:
                tunnel_address = _resolve_tunnel(tunnel_domain, "AAAA")
            else:
                tunnel_address = _resolve_tunnel(tunnel_domain, "A")
            if tunnel_address == None:
                print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] failed to resolve tunnel domain")
                sys.exit(0)
            custom_domain = cfg["domain"]
            if custom_domain == None or custom_domain == "none":
                custom_domain = str(tunnel_domain)
            else:
                print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;34mINFO\033[0m ] resolving custom domain")
                if support_ipv6 == True:
                    record = _resolve_domain(custom_domain, "AAAA")
                else:
                    record = _resolve_domain(custom_domain, "A")
                if record == None:
                    print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] failed to resolve domain")
                    sys.exit(0)
                if record != tunnel_address:
                    print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] domain not connected")
                    print_s(f"it was not possible to create a tunnel because the domain on the A or AAAA record\ndoes not point to the ip “"+tunnel_address+"”")
                    sys.exit(0)
            start_thread(check_domain, [custom_domain])
            protocol = str(cfg["proto"])
            if protocol != "tcp" and protocol != "http" and protocol != "https":
                print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] unknown tunnel protocol")
                sys.exit(0)
            if cfg["console"] != True and cfg["console"] != False:
                print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;33mWARN\033[0m ] invalid arguments in «console», using default «false»")
                console = "no"
            else:
                if cfg["console"] == True: console = "yes"
                else: console = "no"
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
                'low_delay': low_delay,
                'allow_vpn': vpn,
                'blacklist': blist,
                'whitelist': wlist,
                'compress': compression,
                'console': console,
                'server': tunnel_domain,
                'domain': custom_domain,
                'token': tt,
                'proto': protocol,
                'rate': int(cfg["firewall"]["protection"]["level"]),
                'arch': arch,
                'name': name,
            }
            print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;34mINFO\033[0m ] executing tunnel with threads")
            run = Client(**arguments)
        else:
            print_s(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] bad config file")
            sys.exit(7)

        def stop(a, b):
            run.stop()

        signal.signal(signal.SIGINT, exit_system)
        if run:
            while show_message:
                if "offline" in status:
                    try:
                        show_message = False
                        time.sleep(2)
                        show_message = True
                    except:
                        run.stop()
                        sys.exit(1)
                    run.start()
                    try:
                        while run._running:
                            time.sleep(1)
                    except:
                        run.stop()
                        sys.exit(1)
                    time.sleep(2)
    else:
        parser.print_help()

if __name__ == '__main__':
    init_colors()
    main()
else:
    sys.tracebacklimit = 0
    raise ImportError("you can't import this as a module")
