# CCNA 200-301 Lab 11: OSPFv2 Single Area

A hands-on Cisco networking lab that configures **OSPFv2 in Area 0**
across five routers and verifies end-to-end connectivity between router
loopbacks and LAN PCs. The lab also practices OSPF clear-text
authentication, MD5 authentication, and Hello/Dead timer tuning.

## Lab Objectives

-   Configure IPv4 addresses on router interfaces and loopback
    interfaces.
-   Configure OSPFv2 in backbone Area 0 on five routers.
-   Advertise connected networks and learn routes dynamically.
-   Verify connectivity between all router loopbacks.
-   Verify connectivity between PCs on different LANs.
-   Configure clear-text OSPF authentication between R1 and R4.
-   Configure MD5 OSPF authentication between R4 and R5.
-   Change OSPF Hello and Dead intervals between R1 and R4.

## Topology Overview

The lab contains five routers (R1--R5), five LAN PCs, and a shared
transit network connecting R1, R2, and R3. R1 connects to R4, and R4
connects to R5.

``` text
 PC2                 PC3
  |                   |
 R2 -----------+----- R3
  \            |      /
   \         Switch-1
    \           |
             R1 -------- R4 -------- R5
                         |             |
                        PC4           PC5

PC2 LAN: 192.168.2.0/24
PC3 LAN: 192.168.3.0/24
PC4 LAN: 192.168.4.0/24
PC5 LAN: 192.168.5.0/24
```

*The diagram is a simplified logical view. Use the interface and
IP-address tables below as the source of truth for the lab addressing.*

## IP Addressing Plan

### Router interfaces

  Router   Interface   IPv4 address       Purpose
  -------- ----------- ------------------ --------------------
  R1       Fa0/0       `10.10.10.1/24`    Shared transit LAN
  R1       Fa1/1       `14.14.14.1/24`    Link to R4
  R1       Loopback0   `1.1.1.1/24`       Router loopback
  R2       Fa0/0       `10.10.10.2/24`    Shared transit LAN
  R2       Fa1/1       `192.168.2.2/24`   PC2 LAN gateway
  R2       Loopback0   `2.2.2.2/24`       Router loopback
  R3       Fa0/0       `10.10.10.3/24`    Shared transit LAN
  R3       Fa1/1       `192.168.3.3/24`   PC3 LAN gateway
  R3       Loopback0   `3.3.3.3/24`       Router loopback
  R4       Fa0/0       `14.14.14.4/24`    Link to R1
  R4       Fa1/0       `192.168.4.4/24`   PC4 LAN gateway
  R4       Fa1/1       `45.45.45.4/24`    Link to R5
  R4       Loopback0   `4.4.4.4/24`       Router loopback
  R5       Fa0/0       `45.45.45.5/24`    Link to R4
  R5       Fa0/1       `192.168.5.5/24`   PC5 LAN gateway
  R5       Loopback0   `5.5.5.5/24`       Router loopback

### PC addressing

  PC    IPv4 address     Subnet mask       Default gateway
  ----- ---------------- ----------------- -----------------
  PC2   `192.168.2.10`   `255.255.255.0`   `192.168.2.2`
  PC3   `192.168.3.10`   `255.255.255.0`   `192.168.3.3`
  PC4   `192.168.4.10`   `255.255.255.0`   `192.168.4.4`
  PC5   `192.168.5.10`   `255.255.255.0`   `192.168.5.5`

## Technologies and Concepts

-   Cisco IOS command-line configuration
-   IPv4 addressing and subnet masks
-   OSPFv2 dynamic routing
-   OSPF Area 0 and network statements
-   OSPF neighbor adjacencies and router IDs
-   OSPF routing table and link-state database
-   Simple password (clear-text) authentication
-   MD5 message-digest authentication
-   OSPF Hello and Dead intervals
-   ICMP ping and routing troubleshooting

## Configuration Highlights

### 1. Configure OSPF Area 0

Example for R1:

``` text
enable
configure terminal
router ospf 1
 network 14.14.14.1 0.0.0.0 area 0
 network 10.10.10.0 0.0.0.255 area 0
 network 1.1.1.1 0.0.0.0 area 0
end
```

The lab uses different local OSPF process IDs on different routers. OSPF
process IDs are locally significant; the important requirement is that
the participating interfaces belong to Area 0 and that the network
statements match the intended interfaces.

### 2. Clear-text authentication between R1 and R4

Configure the matching settings on both ends of the R1--R4 link.

**R1:**

``` text
configure terminal
interface FastEthernet1/1
 ip ospf authentication
 ip ospf authentication-key Cisco123
```

**R4:**

``` text
configure terminal
interface FastEthernet0/0
 ip ospf authentication
 ip ospf authentication-key Cisco123
```

### 3. MD5 authentication between R4 and R5

The authentication type, key ID, and key string must match on both ends.

**R4:**

``` text
configure terminal
interface FastEthernet1/1
 ip ospf authentication message-digest
 ip ospf message-digest-key 1 md5 Disco123
```

**R5:**

``` text
configure terminal
interface FastEthernet0/0
 ip ospf authentication message-digest
 ip ospf message-digest-key 1 md5 Disco123
```

### 4. Adjust Hello and Dead intervals between R1 and R4

Apply the same values on both ends of the link.

**R1:**

``` text
configure terminal
interface FastEthernet1/1
 ip ospf hello-interval 15
 ip ospf dead-interval 60
```

**R4:**

``` text
configure terminal
interface FastEthernet0/0
 ip ospf hello-interval 15
 ip ospf dead-interval 60
```

> **Lab security note:** The passwords shown here are for practice only.
> Do not reuse lab credentials in production networks. Clear-text OSPF
> authentication does not encrypt the password, and MD5 is a legacy
> mechanism.

## Verification and Testing

Run these commands on the routers to confirm interface status, OSPF
operation, learned routes, and neighbor adjacencies.

``` text
show ip interface brief
show ip protocols
show ip ospf interface brief
show ip ospf neighbor
show ip ospf database
show ip route ospf
show ip ospf interface FastEthernet1/1
```

Test loopback reachability between routers, for example:

``` text
R1# ping 2.2.2.2
R1# ping 3.3.3.3
R1# ping 4.4.4.4
R1# ping 5.5.5.5
```

Test PC-to-PC connectivity across LANs, for example:

``` text
PC2> ping 192.168.3.10
PC2> ping 192.168.4.10
PC2> ping 192.168.5.10
```

Expected results:

-   OSPF neighbors reach the `FULL` state on router-to-router OSPF
    links.
-   OSPF routes appear in `show ip route ospf`.
-   Router loopbacks are reachable from the other routers.
-   PCs can reach the other PCs when addressing, gateways, routing, and
    links are configured correctly.
-   Authentication settings match on each authenticated link.
-   R1 and R4 show Hello interval `15` and Dead interval `60` on their
    shared link.

The supplied lab document shows successful loopback pings and inter-PC
ping responses. Initial ping timeouts may occur while ARP resolution or
OSPF convergence is in progress.

## Troubleshooting Checklist

If a neighbor does not reach `FULL`, check:

1.  Both link interfaces are up and have correct IP addresses and masks.
2.  Both interfaces are assigned to Area 0.
3.  OSPF authentication type and credentials match on both ends.
4.  Hello and Dead intervals match on both ends.
5.  The intended networks are included in OSPF.
6.  The routing table contains the expected remote LAN and loopback
    routes.
7.  Each PC has the correct IP address, subnet mask, and default
    gateway.

Useful focused checks:

``` text
show ip ospf neighbor
show ip ospf interface
show ip route
show running-config
```

## Skills Demonstrated

-   Configuring and troubleshooting a multi-router routed network
-   Implementing single-area OSPFv2
-   Reading OSPF neighbor, interface, database, and route outputs
-   Applying routing-protocol authentication
-   Tuning routing-protocol timers
-   Verifying end-to-end IPv4 connectivity

## Lab Environment

This lab is designed for a Cisco IOS-compatible network simulator or lab
environment, such as Packet Tracer or GNS3, depending on feature
support. Some commands and authentication options may vary by platform
or IOS version.

## Source

Based on the practice document **"CCNA 200-301 - Lab-11 OSPFv2 Single
Area v1.0"** provided for this lab. This repository README summarizes
the exercise and highlights selected configurations; it is not a
replacement for the full lab instructions.

------------------------------------------------------------------------

If you are using this repository as a portfolio project, add your own
topology screenshot, configuration files, and verification screenshots
after reproducing the lab. Only claim tests you have personally run.
