# Layer 3 Switch Inter-VLAN Routing with DHCP and NAT

This project demonstrates a fully functional enterprise network topology simulated in Cisco Packet Tracer / GNS3. It highlights **Inter-VLAN Routing** using a Layer 3 switch, centralized **DHCP Services**, and **Network Address Translation (NAT)** for internet access.

---

## 📐 Network Topology

```text
                           [ INTERNET / ISP ]
                                  |
                                  | (DHCP / 192.168.1.0/24)
                                  |
                             +----+----+
                             |   R1    | (Edge Router)
                             +----+----+
                                  |
                                  | 10.0.11.0/30 (Routed Port)
                                  |
                            +-----+-----+
                            |   Core1   | (Layer 3 Switch)
                            +--+-----+--+
                               |     |
              10.0.10.0/30     |     |  Trunk (802.1Q)
         +---------------------+     +-----------------------+
         |                                                   |
   +-----+-----+                                       +-----+-----+
   |   DHCP    | (Server Router)                       |  Access 1 | (Layer 2 Switch)
   +-----------+                                       +-----+-----+
                                                             |
                                            +----------------+----------------+
                                            |                |                |
                                        [VLAN 10]        [VLAN 20]        [VLAN 30]
                                         172.10.10.0/24   172.20.20.0/24   172.30.30.0/24
```

---

## 📊 Addressing Table

| Device | Interface | IP Address / Prefix | Default Gateway | Function |
| :--- | :--- | :--- | :--- | :--- |
| **ISP Router** | Gi0/0 | `192.168.1.1/24` | N/A | Simulated ISP & DHCP Server |
| **R1** | Gi0/0/0 | `10.0.11.1/30` | N/A | Internal Gateway |
| **R1** | Gi0/0/1 | `DHCP assigned` | `192.168.1.1` | WAN Interface (NAT Outside) |
| **Core1** | Gi0/0 | `10.0.11.2/30` | N/A | Connected to R1 (Routed Port) |
| **Core1** | Gi0/1 | `10.0.10.2/30` | N/A | Connected to DHCP (Routed Port) |
| **Core1** | Vlan10 | `172.10.10.254/24` | N/A | SVI Gateway for VLAN 10 |
| **Core1** | Vlan20 | `172.20.20.254/24` | N/A | SVI Gateway for VLAN 20 |
| **Core1** | Vlan30 | `172.30.30.254/24` | N/A | SVI Gateway for VLAN 30 |
| **DHCP Server** | Eth0/0 | `10.0.10.1/30` | `10.0.10.2` | Centralized DHCP Server |

---

## 🛠️ Key Features & Technologies

- **Inter-VLAN Routing**: SVI configuration on Core1 with `ip routing` enabled.
- **DHCP Relay**: `ip helper-address 10.0.10.1` used on Core1 SVIs to forward DHCP requests across routed interfaces.
- **Dynamic NAT with PAT**: Overload NAT configured on R1 for outbound internet reachability.
- **Trunking**: 802.1Q encapsulated trunks to Access layer switches with DTP disabled (`switchport nonegotiate`).

---

## ⚙️ Configuration Files

### 1. Core1 (Layer 3 Switch)
```text
enable
config terminal
hostname Core1

! Create VLANs
vlan 10
vlan 20
vlan 30
exit

! Enable IP Routing
ip routing

! Configure SVIs with DHCP Helper Address
interface Vlan10
 ip address 172.10.10.254 255.255.255.0
 ip helper-address 10.0.10.1
 no shutdown

interface Vlan20
 ip address 172.20.20.254 255.255.255.0
 ip helper-address 10.0.10.1
 no shutdown

interface Vlan30
 ip address 172.30.30.254 255.255.255.0
 ip helper-address 10.0.10.1
 no shutdown

! Configure Routed Ports
interface GigabitEthernet0/0
 no switchport
 ip address 10.0.11.2 255.255.255.252
 no shutdown

interface GigabitEthernet0/1
 no switchport
 ip address 10.0.10.2 255.255.255.252
 no shutdown

! Configure Trunk Ports to Access Switches
interface range GigabitEthernet0/2 - 3
 switchport trunk encapsulation dot1q
 switchport mode trunk
 switchport trunk allowed vlan 10,20,30
 switchport nonegotiate

! Default Route to Edge Router
ip route 0.0.0.0 0.0.0.0 10.0.11.1
end
```

### 2. DHCP Server Router
```text
enable
config terminal
hostname DHCP

interface Ethernet0/0
 ip address 10.0.10.1 255.255.255.252
 no shutdown

! Exclude Gateway IPs
ip dhcp excluded-address 172.10.10.254
ip dhcp excluded-address 172.20.20.254
ip dhcp excluded-address 172.30.30.254

! VLAN 10 Pool
ip dhcp pool VLAN10
 network 172.10.10.0 255.255.255.0
 default-router 172.10.10.254

! VLAN 20 Pool
ip dhcp pool VLAN20
 network 172.20.20.0 255.255.255.0
 default-router 172.20.20.254

! VLAN 30 Pool
ip dhcp pool VLAN30
 network 172.30.30.0 255.255.255.0
 default-router 172.30.30.254

! Default Route to Core Switch
ip route 0.0.0.0 0.0.0.0 10.0.10.2
end
```

### 3. Edge Router (R1)
```text
enable
config terminal
hostname R1

! LAN Interface
interface GigabitEthernet0/0/0
 ip address 10.0.11.1 255.255.255.252
 ip nat inside
 no shutdown

! WAN Interface (DHCP Client)
interface GigabitEthernet0/0/1
 ip address dhcp
 ip nat outside
 no shutdown

! Static Return Routes for Internal Subnets
ip route 172.10.10.0 255.255.255.0 10.0.11.2
ip route 172.20.20.0 255.255.255.0 10.0.11.2
ip route 172.30.30.0 255.255.255.0 10.0.11.2

! Configure NAT / PAT
access-list 1 permit 172.0.0.0 0.255.255.255
ip nat inside source list 1 interface GigabitEthernet0/0/1 overload
end
```

### 4. ISP Router (Simulated Internet Provider)
```text
enable
config terminal
hostname ISP

interface GigabitEthernet0/0
 ip address 192.168.1.1 255.255.255.0
 no shutdown

! Exclude ISP Gateway Address
ip dhcp excluded-address 192.168.1.1

! DHCP Pool for Edge Routers
ip dhcp pool ISP_POOL
 network 192.168.1.0 255.255.255.0
 default-router 192.168.1.1
end
```

---

## 🔍 Verification Commands

To verify operational status across devices:

- **Check Dynamic IP Assignment on R1:**
  ```text
  R1# show ip interface brief
  ```
- **Verify NAT Translations:**
  ```text
  R1# show ip nat translations
  ```
- **Verify Routing Tables:**
  ```text
  Core1# show ip route
  R1# show ip route
  ```
- **Verify Active DHCP Leases:**
  ```text
  DHCP# show ip dhcp binding
  ISP# show ip dhcp binding
  ```
- **Test End-to-End Connectivity:**
  From any VLAN client host:
  ```text
  ping 8.8.8.8
  ```

---

## 🤝 Contributing
Feel free to open an issue or submit a pull request if you find any misconfigurations or want to expand the topology!