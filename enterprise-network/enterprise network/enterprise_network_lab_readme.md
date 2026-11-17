# 🏢 Build an Enterprise Network from Scratch (Cisco Packet Tracer)

A complete, high-availability enterprise campus network built from scratch in **Cisco Packet Tracer** (based on the *ITTechStudies* CCNA enterprise lab). This project demonstrates multi-layer switching, gateway redundancy, dynamic routing, and WAN connectivity.

* **Video Reference:** [Build an Enterprise Network from Scratch (Packet Tracer)](https://youtu.be/RvPR2BeqwLw) by **ITTechStudies**
* **Certification Focus:** Cisco CCNA (200-301)

---

## 📋 Overview

Enterprise networks require both **segmentation** (to isolate departmental traffic) and **redundancy** (to eliminate single points of failure). In this lab, you design and configure a multi-tier topology featuring redundant distribution switches, Layer 3 Switched Virtual Interfaces (SVIs), First-Hop Redundancy via HSRP, dynamic routing with OSPF, and WAN connectivity.

### Key Technologies & Protocols

* **Enterprise Campus Design:** Hierarchical Access, Distribution/Core, and WAN Edge layers.
* **VLANs & 802.1Q Trunking:** Departmental traffic isolation across access and distribution switches.
* **Inter-VLAN Routing (SVIs):** Layer 3 switching using Switched Virtual Interfaces (`interface vlan <id>`).
* **HSRP (Hot Standby Router Protocol):** Active/Standby default gateway redundancy across dual distribution switches so hosts never lose gateway reachability if one switch fails.
* **OSPF (Open Shortest Path First):** Dynamic interior gateway routing between the distribution/core layer and the WAN edge routers.
* **WAN Connectivity:** Point-to-point routing connecting the enterprise campus to remote/external networks.

---

## 🏗️ Network Architecture

### Logical Topology Flow

```text
   [ End Devices / Departmental PCs ]
                   │  (Access Ports)
          [ Access Switches ]
               ╱       ╲  (802.1Q Trunks)
   [ Dist-SW1 (Active) ] ═══ [ Dist-SW2 (Standby) ]   <-- HSRP Virtual Gateway + SVIs
               ╲       ╱  (Layer 3 / OSPF Area 0)
            [ WAN Edge Routers ]
                   │  (WAN Link)
           [ External / Remote Site ]
```

### Core Configuration Components

| Layer / Role | Devices | Key Configurations |
| :--- | :--- | :--- |
| **Access Layer** | Layer 2 Switches (`2960`) | VLAN creation, `switchport mode access`, `switchport mode trunk` uplinks |
| **Distribution / Core** | Multilayer Switches (`3560` / `3650`) | `ip routing`, SVIs (`interface vlan`), HSRP (`standby <group> ip <vip>`), OSPF |
| **WAN Edge** | Cisco Routers (`2911` / `4321`) | Point-to-point interfaces, OSPF Area 0 neighbor adjacencies |
| **End Hosts** | PCs / Servers | IPv4 addresses pointed to the **HSRP Virtual IP** as their default gateway |

---

## 🚀 Step-by-Step Build & Configuration Workflow

1. **Physical Topology & Cabling**
   * Place Access switches, dual Distribution Layer 3 switches, WAN routers, and end devices.
   * Wire redundant uplinks from Access switches to both Distribution switches, cross-connect the Distribution switches, and link them to the WAN routers.

2. **Layer 2 Switching (VLANs & Trunks)**
   * Create departmental VLANs consistently across all switches.
   * Assign host-facing ports to their respective VLANs (`switchport mode access`).
   * Configure inter-switch uplinks as `switchport mode trunk` with 802.1Q encapsulation.

3. **Inter-VLAN Routing (SVIs)**
   * Enable Layer 3 routing (`ip routing`) on both Distribution switches.
   * Create Switched Virtual Interfaces (`interface vlan <id>`) with unique physical IP addresses on each Distribution switch.

4. **Gateway Redundancy (HSRP)**
   * Configure HSRP on each SVI across both Distribution switches using a shared Virtual IP (VIP).
   * Adjust HSRP priority (`standby <group> priority 110`) and enable `preempt` on the primary Distribution switch so it deterministically holds the **Active** role.

5. **Dynamic Routing (OSPF) & WAN Links**
   * Configure IP addressing on the Layer 3 links connecting the Distribution switches and WAN routers.
   * Enable OSPF (`router ospf 1`) and advertise internal VLAN subnets and transit links into Area 0.

---

## ✅ Verification & Testing

Run the following commands and failover tests in Cisco Packet Tracer to validate the build:

* **Verify VLANs & Trunks:**
  ```ios
  show vlan brief
  show interfaces trunk
  ```
* **Verify HSRP Active/Standby Roles:**
  ```ios
  show standby brief
  ```
  *(Confirm one Distribution switch shows `Active` and the other shows `Standby` for each VLAN group.)*
* **Verify OSPF Neighbors & Routing Table:**
  ```ios
  show ip ospf neighbor
  show ip route ospf
  ```
* **End-to-End & Failover Testing:**
  1. Ping between PCs in different VLANs and across the WAN link (`Success`).
  2. Shut down the uplink or SVI on the **Active** HSRP Distribution switch and run a continuous ping (`ping -t`) from a PC to verify automatic failover to the **Standby** switch.

---

## 🛠️ Prerequisites

* [Cisco Packet Tracer](https://www.netacad.com/cisco-packet-tracer) (Version 8.0 or higher recommended)