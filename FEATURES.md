## Features

- [x] Powerful protection against DDoS attacks, including advanced traffic filtering mechanisms.
- [x] Optimized multi-threaded processing for handling large volumes of traffic.
- [x] Intuitive interface for managing TCP tunnels and configuring ports.
- [x] Reliable NAT traversal system for convenient access to devices in a local network.
- [x] Automatic tunnel restart to ensure uninterrupted connection.
- [x] Integration with APIs for automating tunnel creation and management.
- [x] Support for working with dynamic IP addresses for flexible routing.
- [x] Dual-stack support for IPv4 and IPv6 protocols.
- [x] Secure console for managing active connections and monitoring their real-time status.
- [x] QoS (Quality of Service) support for prioritizing traffic of critical applications.
- [ ] Optimal adaptation to the system and its capabilities for effective multithreading.
- [ ] Built-in HTTP header logging feature for websites operating over HTTP.
- [ ] Supports SOCKS5 proxy with and without authentication for tunnels.

<details id="missing-code-coverage">
  <summary>more information.</summary>

- We added the X-Forwarded-For HTTP header, allowing us to identify the user's true IP address. This prevents the display of a local address, such as 127.0.0.1, and ensures accurate client identification.

- Support for multi-threading has been added to optimize traffic transmission, significantly speeding up data exchange and improving overall performance.

</details>
