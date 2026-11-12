# ☕ Coffee Shop Network Topology (Cisco Packet Tracer)

A complete, segmented small-business network built in **Cisco Packet Tracer**. This project simulates a real-world coffee shop environment with separated traffic for point-of-sale (POS) systems, staff devices, and public guest Wi-Fi.

---

## 📋 Overview

Small businesses require network segmentation to protect sensitive financial transactions (like credit card terminals) from untrusted public guest traffic. This lab demonstrates how to build a secure, scalable local area network (LAN) from scratch in under 30 minutes.

### Key Technologies & Concepts
* **VLANs (Virtual Local Area Networks):** Logical segmentation of Staff, POS, and Guest networks.
* **Router-on-a-Stick (Inter-VLAN Routing):** Using router subinterfaces and 802.1Q trunking to route traffic between VLANs.
* **DHCP (Dynamic Host Configuration Protocol):** Automated IP address assignment configured directly on the Cisco router.
* **ACLs (Access Control Lists):** Security rules preventing guest users from accessing internal staff/POS networks while still allowing internet access.
* **Wireless LAN (WLAN):** Segmented wireless access for staff laptops and customer devices.

---

## 🏗️ Network Architecture

### VLAN & IP Addressing Plan

| VLAN ID | Department / Role | Subnet | Default Gateway | DHCP Range |
| :--- | :--- | :--- | :--- | :--- |
| **VLAN 10** | Staff / Management | `192.168.10.0/24` | `192.168.10.1` | `192.168.10.11 - .254` |
| **VLAN 20** | Point of Sale (POS) | `192.168.20.0/24` | `192.168.20.1` | `192.168.20.11 - .254` |
| **VLAN 30** | Public Guest Wi-Fi | `192.168.30.0/24` | `192.168.30.1` | `192.168.30.11 - .254` |

### Hardware Components
* **1x Router:** Cisco 2911 (Gateway, Inter-VLAN Routing, DHCP Server, Firewall/ACLs)
* **1x Switch:** Cisco 2960-24TT (Layer 2 Access & Trunking)
* **2x Wireless Access Points / Routers:** Dedicated SSIDs for Staff (`CoffeeShop_Staff`) and Guests (`CoffeeShop_Guest`)
* **End Devices:** POS Terminals, Manager PC, Guest Smartphones/Laptops

---

## 🚀 Setup & Configuration Steps

1. **Physical Cabling:**
   * Connect the Router (`GigabitEthernet0/0`) to the Switch (`GigabitEthernet0/1`).
   * Connect end devices and access points to their designated switch ports.
2. **Switch Configuration:**
   * Create VLANs `10`, `20`, and `30`.
   * Assign access ports to their respective VLANs (`switchport mode access`).
   * Configure the uplink port to the router as a trunk (`switchport mode trunk`).
3. **Router Configuration:**
   * Configure subinterfaces (`g0/0.10`, `g0/0.20`, `g0/0.30`) with `encapsulation dot1Q <vlan-id>`.
   * Set up DHCP pools for each subnet, excluding the `.1` to `.10` addresses for static assignments.
4. **Security (ACLs):**
   * Apply an Extended ACL on the Guest subinterface (`g0/0.30` inbound) to block traffic destined for `192.168.10.0/24` and `192.168.20.0/24`, while permitting all other traffic.

---

## ✅ Verification & Testing

To verify the lab is working properly, run the following checks inside Packet Tracer:
* **DHCP Check:** Confirm all PCs, POS terminals, and wireless devices automatically receive an IP address in their correct VLAN subnet.
* **Connectivity Check:** Ping from a Staff PC (`VLAN 10`) to the default gateway and external simulated internet server (`Success`).
* **Security Isolation Check:** Attempt to ping a POS terminal (`192.168.20.x`) from a Guest device (`192.168.30.x`). The request should be **blocked/unreachable** due to the ACL.

---

## 🛠️ Prerequisites
* [Cisco Packet Tracer](https://www.netacad.com/cisco-packet-tracer) (Version 8.0 or higher recommended)