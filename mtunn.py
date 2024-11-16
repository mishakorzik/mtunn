#!/usr/bin/python3
"""
                __              __                             .__
  _____ _____  |  | __ ____   _/  |_ __ __  ____   ____   ____ |  |
 /     \\__  \ |  |/ // __ \  \   __\  |  \/    \ /    \_/ __ \|  |
|  Y Y  \/ __ \|    <\  ___/   |  | |  |  /   |  \   |  \  ___/|  |__
|__|_|  (____  /__|_ \\___  >  |__| |____/|___|  /___|  /\___  >____/
      \/     \/     \/    \/                   \/     \/     \/

 Дякую за використання цього модуля для відкриття портів!
 Якщо знайдете хибу у коді будь ласка повідомте! Буду вдячний :D

 Переваги:
  1. Розширений і данійний захист від ddos атак.
  2. Відкриває порти до інтернету на IPv4 і IPv6 (подвійний стек).
  3. Багато корисних налаштувань і легке користування тунелями.
  4. Безпечна консоль для контролю над активними тунелями.
  5. Має буферизацію трафіку і працює на повільному інтернеті.

 he1zen networks.
 copyring © 2024. All rights reserved.
"""

import os, sys, time, json, threading, signal, argparse, curses, shutil, re
import socket, platform, json, ipaddress, zlib, yaml, requests, itertools
import subprocess as sp

version = '1.0.7'
build = 'beta'

global latest_conn
global ping_method
global nat_banned_ips
global support_ipv4
global support_ipv6
global buffer_size
global compression
global saved_network
global connections
global max_network
global used_network
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

st_t = False
latest_conn = ""
if shutil.which("ping"): ping_method = "icmp"
else: ping_method = "tcp"
tunnel_max_c = "0"
tunnel_total = "0"
buffer_size = 1024
saved_network = 0
compression = False
compressed_network = 0
quota_new = "-"
max_network = "-"
used_network = 0
connections = 0
tunnel_conn = 0
tunnel_traffic = 0
tunnels_hostname = []
tunnels_address = []
tunnels_domain = []

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
            tunnels_hostname.append(tunnel["hostname"]+", "+str(supported_types)+"  -  "+latency)
        return (tunnels_hostname, hostname)
    except Exception as e:
        print(e)
        print("tunnel config error")
        sys.exit(0)

def menu(stdscr, options, type):
    curses.curs_set(0)
    selected_index = 0
    while True:
        stdscr.clear()

        if type == 1:
            stdscr.addstr(1, 2, "Use the ↑ and ↓ keys to select which entry is highlighted.", curses.A_BOLD)
            stdscr.addstr(2, 2, "You in account control, select option to view details.", curses.A_BOLD)
        elif type == 2:
            stdscr.addstr(1, 2, "Use the ↑ and ↓ keys to select which entry is highlighted.", curses.A_BOLD)
            stdscr.addstr(2, 2, "You need to select tunnel server to use.", curses.A_BOLD)
        try:
            for i, option in enumerate(options):
                x = 4
                y = 4 + i
                mark = "*" if i == selected_index else " "
                stdscr.addstr(y, x, f"{mark} {option}")
        except curses.error:
            sys.exit(0)

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
    post = requests.post(f"http://{main_server}:5569/auth/regdate", headers=headers, timeout=10, json={"email": email}).json()
    if post["status"] == "success" and "rd:" in post["message"]:
        date = post["message"].replace("rd:", "")
    else:
        date = "unknown"
    post = requests.post(f"http://{main_server}:5569/auth/quota", headers=headers, timeout=10, json={"token": token}).json()
    if post["status"] == "success":
        payouts = str(post["payouts"])
    else:
        payouts = "?"
    post = requests.post(f"http://{main_server}:5569/auth/get_quota", headers=headers, timeout=10, json={"token": token}).json()
    if post["status"] == "success":
        connections, tunnels, network, ports = post["message"].split(" ")
    else:
        connections = "?"
        tunnels = "?"
        network = "?"
        ports = "?"
    spinner = ['⠋', '⠙', '⠹', '⠼', '⠴', '⠦', '⠧', '⠏']
    end_time = time.time() + 7
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
    stdscr.clear()

    stdscr.addstr(0, 0, "WARNING. Do you really want to delete all accounts without recovery?")
    stdscr.addstr(1, 0, "All your unused quota on this account will be deleted.")
    stdscr.addstr(3, 0, "To delete account type: “yes, delete my account.”")
    stdscr.addstr(4, 0, "Delete account?: ")
    stdscr.refresh()

    curses.echo()
    key = stdscr.getstr(4, 17).decode('utf-8')
    curses.noecho()
    if key.lower() == "yes, delete my account.":
        try:
            with open(path, "r") as file:
                data = file.read().split("\n")
                token = data[0]
                email = data[1]
                main_server = data[2]

            post = requests.post(f"http://{main_server}:5569/auth/delete_account", headers=headers, timeout=10, json={"token": token, "email": email}).json()
            if post["status"] == "success":
                stdscr.addstr(6, 0, post["message"], curses.color_pair(1))
            else:
                stdscr.addstr(6, 0, post["message"], curses.color_pair(2))
        except:
            stdscr.addstr(6, 0, "Failed to delete account.", curses.color_pair(2))
    else:
        stdscr.addstr(6, 0, "Account deletion cancelled.", curses.color_pair(1))

    stdscr.refresh()
    stdscr.getch()

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
    new_email = stdscr.getstr(2, 22).decode('utf-8')
    curses.noecho()

    try:
        post = requests.post(f"http://{main_server}:5569/auth/change_email", headers=headers, json={"new_email": new_email, "old_email": old_email, "token": token}, timeout=10).json()
        if post["status"] == "success":
            stdscr.addstr(3, 0, "Enter code from email: ")
            stdscr.refresh()

            curses.echo()
            code = stdscr.getstr(3, 23).decode('utf-8')
            curses.noecho()

            post = requests.post(f"http://{main_server}:5569/auth/verify", headers=headers, json={"email": new_email, "code": code}, timeout=10).json()
            if post["status"] == "success" and "token:" in post["message"]:
                with open(path, "w") as file:
                    file.write(post["message"].replace("token:", "") + "\n")
                    file.write(new_email+"\n")
                    file.write(main_server)
                stdscr.addstr(4, 0, f"Email changed to: {new_email}", curses.color_pair(1))
            elif post["status"] == "error" and "wrong code" in post["message"]:
                stdscr.addstr(4, 0, "Wrong code!", curses.color_pair(3))
            else:
                stdscr.addstr(4, 0, "Failed to change email!", curses.color_pair(3))
        else:
            stdscr.addstr(4, 0, "Failed to change email!", curses.color_pair(3))

    except requests.RequestException as e:
        stdscr.addstr(4, 0, f"Request failed: {str(e)}", curses.color_pair(3))

    stdscr.addstr(5, 0, "\nPress 'q' to exit.")
    stdscr.refresh()
    while True:
        key = stdscr.getch()
        if key == ord('q'):
            break

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
        if email in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
            continue
        else:
            break

    try:
        post = requests.post(f"http://{main_server}:5569/auth/check", headers=headers, json={"email": email}, timeout=10).json()
        if post["status"] == "success":
            if post["message"] == "x00x00x01":
                post = requests.post(f"http://{main_server}:5569/auth/register", headers=headers, json={"email": email}, timeout=10).json()
            elif post["message"] == "x00x01x03":
                post = requests.post(f"http://{main_server}:5569/auth/login", headers=headers, json={"email": email}, timeout=10).json()
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
                    if code in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
                        continue
                    else:
                        break
                stdscr.refresh()
                line = 7
                post = requests.post(f"http://{main_server}:5569/auth/verify", headers=headers, json={"email": email, "code": code}, timeout=10).json()
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

    stdscr.addstr(line-1, 0, "\nPress 'q' to exit.")
    stdscr.refresh()
    while True:
        key = stdscr.getch()
        if key == ord('q'):
            break
    sys.exit(1)

def cquota(stdscr, headers, path):
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
        post = requests.post(f"http://{main_server}:5569/auth/count_quota", headers=headers, timeout=10, json={"conn": conn, "tunn": tunn, "netw": netw, "prun": tta}).json()
    except requests.RequestException:
        stdscr.addstr(11, 0, "Failed to connect to server", curses.A_BOLD)
        stdscr.getch()
        return

    netw = netw * 1024 * 1024 * 1024
    if post.get("status") == "success":
        stdscr.clear()
        stdscr.addstr(0, 0, "WARNING: This will delete your current quota", curses.A_BOLD)
        stdscr.addstr(1, 0, f"Total price: {post['message']}")
        stdscr.addstr(3, 0, "Accept new quota? (y/n) ")
        stdscr.refresh()

        key = stdscr.getch()
        if key in [ord('y'), ord('Y')]:
            try:
                post = requests.post(f"http://{main_server}:5569/auth/change_quota", headers=headers, timeout=10, json={"token": token, "conn": conn, "tunn": tunn, "netw": netw, "prun": prun}).json()
                if post.get("status") == "success":
                    stdscr.addstr(5, 0, "Quota changed successfully.", curses.A_BOLD)
                    stdscr.addstr(6, 0, "Press 'q' to exit.")
                else:
                    stdscr.addstr(5, 0, "Failed to change quota.", curses.A_BOLD)
                    stdscr.addstr(6, 0, str(post["message"]).capitalize(), curses.A_BOLD)
                    stdscr.addstr(7, 0, "Press 'q' to exit.")
            except requests.RequestException:
                stdscr.addstr(5, 0, "Could not connect to server", curses.A_BOLD)
                stdscr.addstr(6, 0, "Press 'q' to exit.")
        else:
            stdscr.addstr(5, 0, "Operation canceled.", curses.A_BOLD)
            stdscr.addstr(6, 0, "Press 'q' to exit.")
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
headers = {"User-Agent": f"request/{requests.__version__} (mtunn; v{version} {build}) {str(platform.uname().machine)}"}
latency = '-'
status = '\033[01;31moffline\033[0m'
show_message = True

def update_msg(stdscr, protocol):
    global pk_loss
    global pk_colr
    global tunnel_conn
    global show_message
    global saved_network
    global explore_domain
    global tunnel_traffic
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
                    stdscr.addstr(line, 32+len(latency), f"medium", curses.color_pair(2))
                    stdscr.addstr(line, 38+len(latency), f")"+space)
                else:
                    stdscr.addstr(line, 0, f"Latency                       {latency} (")
                    stdscr.addstr(line, 32+len(latency), f"good", curses.color_pair(1))
                    stdscr.addstr(line, 36+len(latency), f")"+space)
            if status != "offline":
                if tunnel_traffic > 1024: # KBytes
                    if tunnel_traffic > 1048576: # MBytes
                        if tunnel_traffic > 1073741824: # GBytes
                            if tunnel_traffic > 1099511627776: # TBytes
                                tt = str(round(tunnel_traffic / 1024 / 1024 / 1024 / 1024, 3))+" TB/s"
                            else:
                                tt = str(round(tunnel_traffic / 1024 / 1024 / 1024, 3))+" GB/s"
                        else:
                            tt = str(round(tunnel_traffic / 1024 / 1024, 3))+" MB/s"
                    else:
                        tt = str(round(tunnel_traffic / 1024, 3))+" KB/s"
                else:
                    tt = str(tunnel_traffic)+" B/s"
                line += 1
                stdscr.addstr(line, 0, f"Network usage                 {tt}"+space)
            else:
                if max_network == "-":
                    tt = "-"
                else:
                    tt = "0 B/s"
                line += 1
                stdscr.addstr(line, 0, f"Network usage                 {tt}"+space)
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
            if compression == True:
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
                stdscr.addstr(line, 32+len(sn), f"zlib", curses.color_pair(5))
                stdscr.addstr(line, 36+len(sn), f")"+space)
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
                if used_network >= max_network:
                    st_t = True
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
            print(f"\033[01;36m" + str(time.strftime("%H:%M:%S")) + f"\033[0m [\033[01;31mERROR\033[0m] failed to display the terminal")
            break

def count_network():
    global tunnel_traffic
    global used_network
    while show_message:
        if tunnel_traffic != 0:
            time.sleep(1)
            tunnel_traffic = 0

def rupdate_msg(protocol):
    time.sleep(2)
    curses.wrapper(update_msg, protocol)

def check_domain(custom_domain):
    time.sleep(60)
    while show_message:
        global tunnel_address, tunnel_domain
        if tunnel_domain != custom_domain:
            if str(socket.gethostbyname(custom_domain)) != str(tunnel_address):
                run.stop()
                print(f"it was not possible to create a tunnel because the domain on the A record\ndoes not point to the ip “"+tunnel_address+"”")
                exit()
        time.sleep(60)

def update_pk():
    global pk_loss
    global show_message
    while show_message:
        if pk_loss == 0:
            pass
        else:
             if "online" in status:
                pk_loss = pk_loss - 1
        if "offline" in status:
            pk_loss = 100
        if pk_loss <= 0:
            pk_loss = 0
        time.sleep(0.20)

def ping_host():
    global pk_loss
    global latency
    global show_message
    global tunnel_max_c
    time.sleep(3)
    while show_message:
        if "offline" in status:
            latency = "-"
        else:
            success = False
            if support_ipv6 == True and isinstance(ipaddress.ip_address(tunnel_address), ipaddress.IPv4Address) == False:
                latency = ping.ipv6(tunnel_address)
                if latency != "-":
                    success = True
            else:
                latency = ping.ipv4(tunnel_address)
                if latency != "-":
                    success = True
            if success == True:
                pk_loss = pk_loss - 10
            if pk_loss <= 0:
                pk_loss = 0
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

def make_package(target, data):
    global compression, saved_network
    if isinstance(data, str):
        data = data.encode()
    comp = b'0'
    if compression == True and len(data) >= 54:
        compress = zlib.compress(data)
        if len(data)-1 > len(compress)+10:
            data = compress
            saved_network += len(data)- len(compress)
            comp = b'1'
    return str(target).encode() + b'L' + comp + b'F' + data

def parse_package(package=''):
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
    return t, data

def sock_read(sock):
    global buffer_size
    global pk_loss
    recv = b''
    if sock:
        try:
            recv = sock.recv(buffer_size)
        except:
            pass
    return recv

def sock_send(sock, data):
    global pk_loss
    if type(data) == type(''):
        data = data.encode()
    ret = False
    if sock:
        try:
            sock.sendall(data)
            ret = True
        except:
            pass
    return ret

_sock_recv = {}
_sock_io_map = {}

def read_package(sock):
    global pk_loss
    global buffer_size
    global tunnel_traffic
    if not sock:
        return
    sockid = int(id(sock))
    if sockid not in _sock_io_map:
        _sock_io_map[sockid] = SockIO(sock)
    try:
        package = _sock_io_map[sockid].recv()
        if package.startswith((b';')):
            tunnel_traffic += len(package)
        data = parse_package(package)
        if data:
            return data[0], data[1]
    except:
        pk_loss = pk_loss + 5
    return None

def send_package(sock, ix, data):
    global pk_loss
    global tunnel_traffic
    if not sock:
        return
    sockid = int(id(sock))
    if sockid not in _sock_io_map:
        _sock_io_map[sockid] = SockIO(sock)
    try:
        package = make_package(ix, data)
        if ix != 0:
            tunnel_traffic += len(package)
        return _sock_io_map[sockid].send(package)
    except:
        pk_loss = pk_loss + 5
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

class Lock(object):
    def __init__(self, name='default'):
        from threading import Lock
        self.name = name
        self.lock = Lock()

    def __enter__(self):
        self.lock.acquire()

    def __exit__(self, *unused):
        self.lock.release()

class PackageIt(object):
    head = b'DH'
    leng = b':'
    buffer = b''

    def feed(self, data):
        if isinstance(data, str):
            data = data.encode()
        self.buffer += data

    def recv(self):
        hix = self.buffer.find(self.head)
        if hix >= 0:
            lix = self.buffer.find(self.leng, hix + len(self.head))
            if lix > 0:
                lns = self.buffer[hix + len(self.head): lix]
                pend = lix + len(self.leng) + int(lns)
                if len(self.buffer) >= pend:
                    data = self.buffer[lix + len(self.leng):pend]
                    self.buffer = self.buffer[pend:]
                    return data
        return None

    def make(self, data):
        if isinstance(data, str):
            data = data.encode()
        pack = self.head + str(len(data)).encode() + self.leng + data
        return pack


class SockIO(object):
    global buffer_size
    _pi = PackageIt()
    _recv_lock = Lock()
    _send_lock = Lock()

    def __init__(self, sock):
        self.sock = sock
        assert sock

    def recv(self):
        with self._recv_lock:
            while True:
                data = self._pi.recv()
                if data == None:
                    r = self.sock.recv(buffer_size+128)
                    if not r:
                        break
                    self._pi.feed(r)
                else:
                    break
            return data

    def send(self, data):
        if isinstance(data, str):
            data = data.encode()
        pack = self._pi.make(data)
        ret = False
        with self._send_lock:
            try:
                self.sock.sendall(pack)
                ret = True
            except:
                pass
        return ret

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
        global status, latency, tunnel_conn, max_network
        self._dog_last = int_time()
        while self._dog_runing:
            now = int_time()
            if (now - self._dog_last) > 5:
                status = "offline"
                tunnel_conn = 0
                max_network = '-'
                latency = '-'
                time.sleep(2)
                self.stop()
                time.sleep(3)
            time.sleep(1)

    def stop_dog(self):
        self._dog_runing = False

    def start_dog(self):
        self._dog_runing = True
        start_thread(self._dog_run)

    def feed_dog(self):
        self._dog_last = int_time()

class ping:
    global ping_method
    def ipv4(host, timeout=2):
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

    def ipv6(host, port=5570, timeout=2):
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
    reconnect = "no"
    domain = ''
    proto = ''
    name = ''
    _client_map = {}

    def _run_con(self, ix, sock):
        while self._running:
            recv = sock_read(sock)
            if recv:
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
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.connect((self.target_host, self.target_port), )
            self._client_map[ix] = {
                'sock': sock,
                'th': start_thread(target=self._run_con, args=[ix, sock])
            }
            return self._client_map[ix]
        except:
            pass

    def _run_ping(self):
        global st_t
        while self._running:
            send_package(self._sock, 0, b'p;')
            time.sleep(1)
            if st_t == True:
                print(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] all data used.")
                self.stop(False)
                break

    def _run(self):
        if self.console == "yes":
            start_thread(target=self.remote)
            self.console = "no"
        global status, tunnel_two, compression
        global server_version, server_build, connections, tunnel_max_c, tunnel_total, saved_network
        global used_network, max_network, tunnel_traffic, tunnel_conn, latest_conn, quota_new
        tunnel_two = f"{self.target_host}:{self.target_port}"
        try:
            self.start_dog()
            if support_ipv6 == True and isinstance(ipaddress.ip_address(tunnel_address), ipaddress.IPv4Address) == False:
                if self.reconnect == "no":
                    print(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;34mINFO\033[0m ] \033[01;32mconnecting\033[0m with IPv6")
                    self.reconnect = "yes"
                else:
                    print(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;34mINFO\033[0m ] \033[01;33mreconnecting\033[0m with IPv6")
                sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
                self._sock = sock
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock.connect((tunnel_address, 5567))
            else:
                if self.reconnect == "no":
                    print(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;34mINFO\033[0m ] \033[01;32mconnecting\033[0m with IPv4")
                    self.reconnect = "yes"
                else:
                    print(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;34mINFO\033[0m ] \033[01;33mreconnecting\033[0m with IPv4")
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self._sock = sock
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock.connect((tunnel_address, 5567))
            if compression == True: c = 'yes'
            else: c = 'no'
            sd = {
                'version': version,
                'system': {'name': self.name[:20], 'arch': self.arch[:10].lower()},
                'tunnel': {'proto': self.proto, 'domain': self.domain, 'buffer': self.buffer, 'compression': c},
                'firewall': {'rate': self.rate, 'tor': self.allow_tor, 'vpn': self.allow_vpn},
                'token': self.token,
                'bind': self.proxy_bind,
                'port': self.proxy_port,
            }
            send_package(sock, 0, json.dumps(sd))
            self.feed_dog()
            _, data = read_package(sock)
            ret = json.loads(data)
            if ret["status"] == 1:
                server_version = str(ret['version'])
                server_build = str(ret['build'])
                tunnel_max_c = str(ret["max_tunnels"])
                used_network = int(ret["used_network"])
                max_network = int(ret["max_network"])
                status = "online"
                connections = int(ret["connections"])
                start_thread(rupdate_msg, [self.proto])
                start_thread(count_network)
                start_thread(update_pk)
                start_thread(ping_host)
            elif ret["status"] == 0:
                status = "offline"
            elif ret["status"] == 4:
                print(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] "+str(ret["message"]))
                self.stop()
                exit_system()
                time.sleep(2)
        except:
            status = "offline"
            self.stop()
        self.feed_dog()
        start_thread(target=self._run_ping)
        while self._running:
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
                    elif data.startswith(b"reply.nat:"):
                        latest_conn = data.decode().replace("reply.nat:", "")
                elif ix > 0:
                    if ix not in self._client_map:
                        d = self._add_con(ix)
                    else:
                        d = self._client_map[ix]
                    if d:
                        sock_send(d['sock'], data)
                    else:
                        send_package(self._sock, -1 * ix, b'')
                else:
                    nix = abs(ix)
                    if nix in self._client_map:
                        if not data or data == b'close':
                            d = self._client_map[nix]
                            sock_close(d['sock'])
                            del self._client_map[nix]

    def stop(self, s=True):
        if s == True:
            send_package(self._sock, 0, b'c;')
        del s
        self.stop_dog()
        for d in self._client_map.values():
            sock_close(d['sock'])
        self._client_map.clear()
        super(Client, self).stop()

    def remote(self):
        global latest_conn
        global used_network
        global max_network
        global quota_new

        nat_banned_ips = []
        nat_priory = []
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        for port in range(7010, 7041):
            try:
                s.bind(("127.0.0.1", int(port)))
            except:
                pass
        s.listen(5)
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
 network               : tunnel user and max network
 forward               : show tunnel forwarding information
 status                : show tunnel status online/offline
 quota                 : show tunnel day(s) to next quota
 conn                  : show tunnel latest or active connections

\033[01;33mFirewall:\033[0m
 list                  : list all banned ips
 ban <range/ip>        : ban ip-address or cidr on tunnel
 unban <range/ip>      : unban ip-address or cidr on tunnel
 rule <args1> <args2>  : update rule in firewall

\033[01;33mProtection:\033[0m
 iunban <range/ip>     : fully unban ip-address or cidr             (dangerous)
 priory <range/ip>     : add or remove priory to ip address         (dangerous)

\033[01;33mExamples:\033[0m
 ban 8.8.8.8/32        : specify ip or cidr to block
 unban 8.8.8.8/32      : specify ip or cidr to unblock
 iunban 8.8.8.8/32     : specify ip or cidr to unblock from firewall
 rule rate 1           : chane rate in firewall only numbers 0,1,2,3
 rule tor no           : block or unblock only vpn, tor and yes/no""")
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
                            banned = "banned ip ranges:"
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
                    elif r.startswith('conn'):
                        try:
                            wait = 0
                            send_package(self._sock, 0, b'e.nat:conn=latest')
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
                            if "/" not in str(ip):
                                ip = ip + "/32"
                            if str(ip) not in nat_banned_ips:
                                send_package(self._sock, 0, b'e.nat:ban='+str(ip).encode('utf-8'))
                                nat_banned_ips.append(str(ip))
                                sock.send(b'banned ip: '+ip.encode('utf-8'))
                            else:
                                sock.send(b'already banned')
                        except:
                            sock.send(b'\033[01;31mwrong arguments\033[0m')
                    elif r.startswith('priory'):
                        try:
                            _, ip = r.split(" ")
                            if "/" not in str(ip):
                                ip = ip + "/32"
                            send_package(self._sock, 0, b'e.nat:priory='+str(ip).encode('utf-8'))
                            if str(ip) in nat_priory:
                                nat_priory.remove(str(ip))
                                sock.send(b'removed ip: '+ip.encode('utf-8'))
                            else:
                                nat_priory.append(str(ip))
                                sock.send(b'added ip: '+ip.encode('utf-8'))
                        except:
                            sock.send(b'\033[01;31mwrong arguments\033[0m')
                    elif r.startswith('iunban'):
                        try:
                            _, ip = r.split(" ")
                            if "/" not in str(ip):
                                ip = ip + "/32"
                            send_package(self._sock, 0, b'e.nat:iunban='+str(ip).encode('utf-8'))
                            sock.send(b'\033[01;32msuccess\033[0m\nif the IP is not blocked, it will not be possible to unblock it')
                        except:
                             sock.send(b'\033[01;31mwrong arguments\033[0m')
                    elif r.startswith('unban'):
                        try:
                            _, ip = r.split(" ")
                            if str(ip) in nat_banned_ips:
                                send_package(self._sock, 0, b'e.nat:unban='+str(ip).encode('utf-8'))
                                nat_banned_ips.remove(str(ip))
                                sock.send(b'unbanned ip: '+ip.encode('utf-8'))
                            else:
                                sock.send(b'ip not banned')
                        except:
                             sock.send(b'\033[01;31mwrong arguments\033[0m')
                    elif r.startswith('rate'):
                        try:
                            _, rate = r.split(" ")
                            if rate == "0" or rate == "1" or rate == "2" or rate == "3":
                                send_package(self._sock, 0, b'e.nat:rate='+rate.encode('utf-8'))
                                sock.send(b'\033[01;32msuccess\033[0m')
                            else:
                                sock.send(b'wrong firewall rate')
                        except:
                            sock.send(b'\033[01;31mwrong arguments\033[0m')
                    elif r.startswith('rule'):
                        try:
                            _, var, bool = r.split(" ")
                            if var in ["tor", "vpn"]:
                                if bool == "yes" or bool == "no":
                                    send_package(self._sock, 0, b'e.rule:'+str(var).encode('utf-8')+b'='+str(bool).encode('utf-8'))
                                    sock.send(str(var).encode('utf-8')+b' = '+str(bool).encode('utf-8'))
                            elif var == "rate":
                                if bool == "0" or bool == "1" or bool == "2" or bool == "3":
                                    send_package(self._sock, 0, b'e.nat:rate='+bool.encode('utf-8'))
                                    sock.send(b'\033[01;32msuccess\033[0m')
                                else:
                                    sock.send(b'wrong firewall rate')
                            else:
                                sock.send(b'\033[01;31mwrong arguments\033[0m')
                        except:
                            sock.send(b'\033[01;31mwrong arguments\033[0m')
                elif data["version"] == "mtunn_cch1":
                    if data["command"] == "forwarding":
                        sock.send(str(explore_domain).encode('utf-8')+b':'+str(explore_port).encode('utf-8')+b' <-> '+str(tunnel_two).encode('utf-8'))
                else:
                    sock.send(b'x01x07')
                sock.close()

def main():
    global support_ipv4
    global support_ipv6
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('--version', help='show the tunnel current version %s' % version, action='store_true')
    parser.add_argument('--account', help='register or login to account', action='store_true')
    parser.add_argument('--console', help='open a console to control tunnel', action='store_true')
    parser.add_argument('--config', help='specify config file to run tunnel', type=str)
    args = parser.parse_args()
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
            s.send(json.dumps({"version": "mtunn_cv1.0", "command": command}).encode())
            fragments = []
            while True:
                chunk = s.recv(1024)
                fragments.append(chunk)
                if len(chunk) < 1024:
                    break
            s.close()
            return b''.join(fragments).decode()

        def console_check_connection(port):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(("127.0.0.1", port))
                s.settimeout(1)
                s.send(json.dumps({"version": "mtunn_cch1", "command": "forwarding"}).encode())
                r = s.recv(96).decode()
                s.close()
                return r
            except:
                return False

        for p in range(7010, 7039):
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
            while True:
                try:
                    command = str(input(f"\033[01;32mexecute:\033[0m$ "))
                    if command != "":
                        recv = console_make_package(command, port)
                        if recv == "x01x07":
                            print("\033[01;31mError.\033[0m Your console version is not supported")
                            break
                        else:
                            print(recv)
                except:
                    break
        else:
            print(f"tunnel is \033[01;31moffline\033[0m")
    elif args.account:
        try: requests.get("http://v4.ipv6-test.com/api/myip.php", timeout=10); support_ipv4 = True
        except: support_ipv4 = False
        try: requests.get("http://v6.ipv6-test.com/api/myip.php", timeout=10); support_ipv6 = True
        except: support_ipv6 = False
        if platform.system() == "Windows":
            if os.path.exists("C:\\") and os.path.isdir("C:\\"):
                path = "C:\\.auth.hz"
            elif os.path.exists("D:\\") and os.path.isdir("D:\\"):
                path = "D:\\.auth.hz"
        else:
            if os.path.exists("/data/data/com.termux/files/usr/etc") and os.path.isdir("/data/data/com.termux/files/usr/etc"):
                path = "/data/data/com.termux/files/usr/etc/.auth.hz"
            elif os.path.exists("/etc") and os.path.isdir("/etc"):
                path = "/etc/.auth.hz"
        token = ""
        main_server = ""
        try:
            with open(path, "r") as file:
                data = file.read().split("\n")
                try: data.remove("")
                except: pass
                token = data[0]
                main_server = data[2]
            post = requests.post(f"http://{main_server}:5569/status", headers=headers, timeout=10, json={"id": 0}).json()
            if post["*"] == "ok":
                if token == "" or main_server == "":
                    print(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] corrupted auth file, restart please")
                    os.system(f"rm {path}")
                    sys.exit(0)
                else:
                    post = requests.post(f"http://{main_server}:5569/auth/vtoken", headers=headers, timeout=10, json={"token": token}).json()
                    if post["message"] == "x00x00x01":
                         print(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] wrong auth file or token, restart please")
                         os.system(f"rm {path}")
                         sys.exit(0)
        except:
            tun = []
            hst = []
            r = _tunnels()
            for pr in r[0]:
                tun.append(pr)
            for pr in r[1]:
                hst.append(pr)
            index = curses.wrapper(menu, tun, 2)
            main_server = hst[index]
            try:
                post = requests.post(f"http://{main_server}:5569/status", headers=headers, timeout=10, json={"id": 0}).json()
            except:
                print(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] invalid server")
                sys.exit(9)
            if post["*"] == "ok":
                print(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;34mINFO\033[0m ] the server is checked and will be selected as primary")
            else:
                print(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] unknown response from server")
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
                print(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] invalid auth file")
                sys.exit(0)
            post = requests.post(f"http://{main_server}:5569/auth/ctoken", headers=headers, timeout=10, json={"token": _t}).json()
            if post["status"] == "success" and "token:" in post["message"]:
                with open(path, "w") as file:
                    file.write(post["message"].replace("token:", "")+"\n")
                    file.write(_e+"\n")
                    file.write(main_server)
                    print(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;34mINFO\033[0m ] token changed")
            else:
                print(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] "+post["message"])
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
            post = requests.post(f"http://{main_server}:5569/auth/quota_price", headers=headers, timeout=10, json={"token": token}).json()
            if post:
                print("quota price: "+str(round(post["total"], 2))+str(post["symbol"]))
            sure = str(input("Replenish the balance? (y/n): "))
            if sure == "y" or sure == "Y" or sure == "Yes" or sure == "yes":
                post = requests.post(f"http://{main_server}:5569/auth/rb", headers=headers, timeout=10, json={"*": ""}).json()
                if post["status"] == "success":
                    print("")
                    print(str(post["message"]))
                else:
                    print(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] failed to get payment")
            else:
                print(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;33mWARN\033[0m ] cancelled")
        elif index == 5:
            os.system(f"rm {path}")
            print(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;34mINFO\033[0m ] success")
        elif index == 6:
            curses.wrapper(delete_account, headers, path)
    elif args.config:
        print(": press CTRL+C to fully stop tunnel")
        try: requests.get("http://v4.ipv6-test.com/api/myip.php", timeout=10); support_ipv4 = True
        except: support_ipv4 = False
        try: requests.get("http://v6.ipv6-test.com/api/myip.php", timeout=10); support_ipv6 = True
        except: support_ipv6 = False
        run = None
        print(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;34mINFO\033[0m ] reading config's files")
        try:
            with open(str(args.config)) as file:
                cfg = yaml.load(file, Loader=yaml.FullLoader)
        except:
            print(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] no config file.")
            sys.exit(7)
        try: cfg["proto"]
        except:
            print(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] not enough arguments «proto»")
            sys.exit(7)
        if platform.system() == "Windows":
            if os.path.exists("C:\\") and os.path.isdir("C:\\"):
                path = "C:\\.auth.hz"
            elif os.path.exists("D:\\") and os.path.isdir("D:\\"):
                path = "D:\\.auth.hz"
        else:
            if os.path.exists("/data/data/com.termux/files/usr/etc") and os.path.isdir(
                    "/data/data/com.termux/files/usr/etc"):
                path = "/data/data/com.termux/files/usr/etc/.auth.hz"
            elif os.path.exists("/etc") and os.path.isdir("/etc"):
                path = "/etc/.auth.hz"
        if os.path.isfile(path):
            with open(path, "r") as file:
                data = file.read().split("\n")
                try: data.remove("")
                except: pass
                tt = data[0]
                main_server = data[2]
        else:
            print(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] failed to run tunnel. No auth file")
            sys.exit(7)
        print(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;34mINFO\033[0m ] checking account token")
        ccmp = False
        try:
            post = requests.post(f"http://{main_server}:5569/auth/vtoken", headers=headers, timeout=10, json={"token": tt}).json()
            if post["message"] == "x00x00x01":
                print(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] wrong auth file or token, please login again")
                os.system(f"rm {path}")
                sys.exit(0)
        except:
            print(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] failed to connect to the server")
            sys.exit(8)
        try: cfg["tunnel"]
        except:
            print(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] not enough arguments «tunnel»")
            sys.exit(7)
        try: cfg["target"]
        except:
            print(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] not enough arguments «target»")
            sys.exit(7)
        try: cfg["domain"]
        except:
            print(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] not enough arguments «domain»")
            sys.exit(7)
        try: cfg["console"]
        except:
            print(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] not enough arguments «console»")
            sys.exit(7)
        try: cfg["firewall"]["rate"]
        except:
            print(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] not enough arguments «rate» in «firewall»")
            sys.exit(7)
        try: cfg["firewall"]["vpn"]
        except:
            print(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] not enough arguments «vpn» in «firewall»")
            sys.exit(7)
        try: cfg["firewall"]["tor"]
        except:
            print(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] not enough arguments «tor» in «firewall»")
            sys.exit(7)
        try: cfg["network"]["compression"]
        except:
            print(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;33mWARN\033[0m ] not enough arguments «compression» in «network»")
            ccmp = True
        try: cfg["network"]["buffer_size"]
        except:
            print(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;31mERROR\033[0m] not enough arguments «buffer_size» in «network»")
            sys.exit(7)
        try:
            pm = cfg["ping"]["method"]
            if pm != "icmp" and pm != "tcp":
                if shutil.which("ping"):
                    print(f"\033[01;36m" + str(time.strftime("%H:%M:%S")) + f"\033[0m [\033[01;33mWARN\033[0m ] bad arguments «method» in «ping», using icmp method.")
                    pm = "tcp"
                else:
                    print(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;33mWARN\033[0m ] bad arguments «method» in «ping», using tcp method.")
                    pm = "tcp"
            if shutil.which("ping") is None and pm == "icmp":
                print(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;33mWARN\033[0m ] ping command not installed, using tcp method.")
                pm = "tcp"
        except:
            if shutil.which("ping"):
                pm = "icmp"
            else:
                pm = "tcp"
        target = cfg["target"]
        target_port = int(target[target.index(":")+1:])
        target_address = target[:target.index(":")]
        if cfg["firewall"]["tor"] == True: tor = "yes"
        else: tor = "no"
        if cfg["firewall"]["vpn"] == True: vpn = "yes"
        else: vpn = "no"
        is_android: bool = hasattr(sys, 'getandroidapilevel')
        if is_android == True:
            import getpass
            arch = str(platform.uname().machine)
            name = str(getpass.getuser())
        else:
            arch = str(platform.uname().machine)
            name = str(socket.gethostname())
        tunnel = cfg["tunnel"]
        if tunnel and target:
            global ping_method
            global buffer_size
            global compression
            global explore_port
            global explore_domain
            global tunnel_domain
            global tunnel_address
            ping_method = pm
            del pm
            try:
                tunnel_port = int(tunnel)
            except:
                print(f"\033[01;36m" + str(time.strftime("%H:%M:%S")) + f"\033[0m [\033[01;31mERROR\033[0m] bad tunnel port in config")
                sys.exit(9)
            tunnel_domain = main_server
            print(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;34mINFO\033[0m ] resolving tunnel domain")
            if support_ipv6 == True:
                try: tunnel_address = socket.getaddrinfo(tunnel_domain, None, socket.AF_INET6)[0][4][0]
                except: tunnel_address = socket.gethostbyname(tunnel_domain)
            else:
                tunnel_address = socket.gethostbyname(tunnel_domain)
            custom_domain = cfg["domain"]
            buffer_size = int(cfg["network"]["buffer_size"])
            if int(buffer_size) > 4096 or int(buffer_size) < 1024:
                print(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [ \033[01;31mERROR\033[0m] bad buffer size in config")
            if custom_domain == None or custom_domain == "none":
                custom_domain = str(tunnel_domain)
            else:
                print(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;34mINFO\033[0m ] resolving custom domain")
                if support_ipv6 == True:
                    try: record = socket.getaddrinfo(custom_domain, None, socket.AF_INET6)[0][4][0]
                    except: record = socket.gethostbyname(custom_domain)
                else:
                    try: record = socket.gethostbyname(custom_domain)
                    except: record = ""
                if record != tunnel_address:
                    print(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [ \033[01;31mERROR\033[0m] domain not connected")
                    print(f"it was not possible to create a tunnel because the domain on the A or AAAA record\ndoes not point to the ip “"+tunnel_address+"”")
                    sys.exit(7)
            start_thread(check_domain, [custom_domain])
            protocol = str(cfg["proto"])
            if protocol == "tcp" or protocol == "http":
                pass
            else:
                print(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [ \033[01;31mERROR\033[0m] unknown tunnel protocol")
                sys.exit(7)
            if cfg["console"] == True: console = "yes"
            else: console = "no"
            explore_domain = str(custom_domain)
            explore_port = str(tunnel_port)
            if ccmp == False:
                if cfg["network"]["compression"] == True: compression = True
                else: compression = False
            else:
                compression = False
            arguments = {
                'proxy_bind': "0.0.0.0",
                'proxy_port': tunnel_port,
                'target_host': target_address,
                'target_port': target_port,
                'allow_tor': tor,
                'allow_vpn': vpn,
                'compress': compression,
                'console': console,
                'server': tunnel_domain,
                'domain': custom_domain,
                'buffer': str(buffer_size),
                'token': tt,
                'proto': protocol,
                'rate': int(cfg["firewall"]["rate"]),
                'arch': arch,
                'name': name,
            }
            print(f"\033[01;36m"+str(time.strftime("%H:%M:%S"))+f"\033[0m [\033[01;34mINFO\033[0m ] executing tunnel threads")
            run = Client(**arguments)
        else:
            parser.print_help()
            exit_system(-1)

        def stop(a, b):
            run.stop()

        signal.signal(signal.SIGINT, exit_system)
        global pk_loss, show_message
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
    main()

