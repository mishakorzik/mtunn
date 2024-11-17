<img width="99.9%" src="https://raw.githubusercontent.com/mishakorzik/mtunn/refs/heads/main/Logo.jpg"/>

<p align="center">
<a href="https://github.com/mishakorzik/mtunn"><img title="Version" src="https://img.shields.io/badge/Build-beta-cornflowerblue?style=for-the-badge&logo="></a>
<a href="https://github.com/mishakorzik/mtunn/blob/main/LICENSE"><img title="License" src="https://img.shields.io/badge/Apache-License 2.0-blue?style=for-the-badge&logo=apache"></a>
<a href="https://github.com/mishakorzik"><img title="Made in Ukraine" src="https://img.shields.io/badge/Made in-Ukraine-steelblue?style=for-the-badge&logo="></a>
<a href="https://github.com/mishakorzik"><img title="Copyring" src="https://img.shields.io/badge/Copyring-2024-skyblue?style=for-the-badge&logo=github"></a>
<a href="https://github.com/mishakorzik"><img title="Author" src="https://img.shields.io/badge/Author-mishakorzik-lightblue?style=for-the-badge&logo=github"></a>
</p>

<p align="center">
• <a href="https://github.com/mishakorzik/mtunn/blob/main/LICENSE">License</a>
• <a href="https://github.com/mishakorzik/mtunn/blob/main/mtunn.py">Source code</a>
• <a href="https://www.buymeacoffee.com/misakorzik">Donate</a>
• <a href="https://github.com/mishakorzik/mtunn/issues">Issues</a> •
</p>

>  with «make tunnel» you can easily open http and tcp ports to the internet.

## Installation

Install the package from the `PyPi`:
```
pip install mtunn
```

Install manually from the `GitHub`:
```
pip install requests>=2.25.0
pip install PyYAML>=6.0.1
pip install ipaddress>=1.0.21
curl -o mtunn.py https://raw.githubusercontent.com/mishakorzik/mtunn/refs/heads/main/mtunn.py
```

## Config example's

In order to start the tunnel, you need to log in to your account and create a configuration file.

```yaml
proto: http              # protocol type                 (http/tcp)
target: 127.0.0.1:8080   # target host
tunnel: 10000            # the port that will be opened
domain: none             # domain to your tunnel
console: yes             # for tunnel control            (yes/no)
firewall:
  rate: 2                # anti ddos rate  0/1/2/3
  vpn: yes               # allow connection from vpn     (yes/no)
  tor: yes               # allow connectiom from tor     (yes/no)
network:
  compression: no        # use traffic compression       (yes/no)
  buffer_size: 1024      # socket buffer size            (1024-4096)
ping:
  method: icmp           # ping method                   (icmp/tcp)
```

```
firewall rates:
 0 - disable
 1 - light
 2 - moderate
 3 - strong
```

<details id="missing-code-coverage">
  <summary>frequently asked questions</summary>

**1) What to do if I don't have a domain?**
- No need to worry, you can run tunnel without a domain just by specifying “none” in the “domain” field.

**2) if I have a domain, how do i connect it?**
- Using a domain is quite simple, you just need to specify your domain in the "domain" field and specify the A and AAAA record in the ip address of the tunnel.

- Please note that if the tunnel does not have IPv6, you do not need to specify an AAAA record for the tunnel's IP address.

**3) What ping method is the best?**
- Both options are best, we added the tcp method so that you can know the delay point without the ping command. If you are not sure about choosing icmp or tcp, you can simply not specify, the tunnel will choose automatically.

</details>

If you have the correct configuration, you will be able to start the tunnel and everything will work.

## Tunnel commands

Instead of the name of the example.yml file, you can write your configuration name, but it must have the extension “.yml”.

```python
# show tunnel current version
python3 -m mtunn --version

# register or login to account
python3 -m mtunn --account

# use console to control tunnel
python3 -m mtunn --console

# open a port to internet
python3 -m mtunn --config example.yml
```

When you register you can run tunnels but only on ports in the range from 10000 to 11000. You can change it in your quota settings.

## Screenshots

Here are examples of how to run and how the tunnel will work.

<img width="48.9%" src="https://raw.githubusercontent.com/mishakorzik/mtunn/refs/heads/main/IMG_20241116_2.jpg"/> <img width="49.9%" src="https://raw.githubusercontent.com/mishakorzik/mtunn/refs/heads/main/IMG_20241116_3.jpg"/>
<img width="47.5%" src="https://raw.githubusercontent.com/mishakorzik/mtunn/refs/heads/main/IMG_20241116_1.jpg"/> <img width="51.4%" src="https://raw.githubusercontent.com/mishakorzik/mtunn/refs/heads/main/IMG_20241116_4.jpg"/>

In order to open ports through the tunnel you need to create a configuration file.

## Other

[![Github](https://img.shields.io/badge/TELEGRAM-MishaKorzhik-orange?style=for-the-badge&logo=telegram)](https://t.me/ubp2q)
[![Github](https://img.shields.io/badge/Discord-He1Zen-blue?style=for-the-badge&logo=discord)](https://discord.gg/xwpMuMYW57)

If you find a bug or have any questions about this project, write to us on discord.
