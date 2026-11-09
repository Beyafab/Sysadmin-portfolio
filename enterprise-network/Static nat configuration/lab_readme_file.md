# Cisco Networking Lab: Static NAT and ACL Interactions

## 1. Network Topology & Overview

* **Internal Network (LAN):** `192.168.1.0/24`
  * **Gateway (R1 G0/0):** `192.168.1.1`
  * **PC1:** `192.168.1.11`
  * **PC2:** `192.168.1.12`
  * **PC3:** `192.168.1.13`
* **WAN / Simulated Internet Link:** `1.2.3.0/24`
  * **R1 Serial 0/3/0:** `1.2.3.1`
  * **R2 Serial 0/3/0:** `1.2.3.2`
* **Remote Network:** `1.1.1.0/24`
  * **SRV1:** `1.1.1.100`

---

## 2. Problem Analysis & Questions

### Question 1: Why can't PC1, PC2, and PC3 successfully ping SRV1 initially?

**Answer:** 
Without Static NAT configured, packets leave the LAN with their real source IP addresses (`192.168.1.x`). On R1's outbound WAN interface (`Serial0/3/0`), an Access Control List (`ip access-group 100 out`) is applied:

```text
access-list 100 deny ip any 10.0.0.0 0.255.255.255
access-list 100 deny ip any 172.16.0.0 0.15.255.255
access-list 100 deny ip any 192.168.0.0 0.0.255.255
access-list 100 permit ip any any
```

The rule `access-list 100 deny ip any 192.168.0.0 0.0.255.255` explicitly drops any packet destined for or originating from private IP space. Furthermore, unroutable private addresses should not traverse a public WAN link.

---

### Question 2: Static NAT Configuration on R1

To resolve private address exposure, static NAT is configured to map each internal private IP to a public IP on the `1.2.3.0/24` network:

```text
! Interfaces NAT Designation
interface GigabitEthernet0/0
 ip nat inside

interface Serial0/3/0
 ip nat outside

! Static NAT Mappings
ip nat inside source static 192.168.1.11 1.2.3.11 
ip nat inside source static 192.168.1.12 1.2.3.12 
ip nat inside source static 192.168.1.13 1.2.3.13 
```

---

### Question 3: Attempt to ping SRV1 from each PC again. Do the pings succeed?

**Answer:** 
**Yes**, after Static NAT is enabled, pings from PC1, PC2, and PC3 to SRV1 (`1.1.1.100`) will succeed. 

**Order of Operations (Outbound on R1):**
1. Packet arrives at `GigabitEthernet0/0` (NAT inside).
2. Routing decision routes packet out `Serial0/3/0` (NAT outside).
3. **NAT translation occurs FIRST:** Source IP is converted from `192.168.1.x` to `1.2.3.x`.
4. **Outbound ACL 100 is evaluated SECOND:** The packet source is now `1.2.3.x` (Public) and destination is `1.1.1.100` (Public). 
5. Because the packet no longer uses a private IP address (`192.168.0.0/16`), it bypasses the `deny` rules and hits `access-list 100 permit ip any any`.

---

## 3. Verification Commands

Run the following commands on **R1** to confirm operations:

```text
! View active NAT translations
R1# show ip nat translations

! Verify ACL matches and packet counts
R1# show access-lists 100

! Debug NAT in real time (optional)
R1# debug ip nat
```