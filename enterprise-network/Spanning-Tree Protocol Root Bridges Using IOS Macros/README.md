# Spanning-Tree Protocol Root Bridges Using IOS Macros

## Overview

This lab demonstrates how to configure Cisco switches to become primary and secondary Spanning Tree Protocol (STP) Root Bridges for specific VLANs using Cisco IOS configuration macros.

The objective is to manually control Root Bridge placement across multiple VLANs to create a predictable and manageable Layer 2 switching topology.

The lab uses two switches:

- **Sw1:** Primary Root Bridge for VLANs 2010 and 2030.
- **Sw2:** Primary Root Bridge for VLANs 2020 and 2040.

Each switch is also configured as the backup Root Bridge for the VLANs primarily managed by the other switch.

## Objectives

- Configure switch hostnames.
- Configure VTP Transparent mode.
- Create and verify extended-range VLANs.
- Configure trunk links between switches.
- Configure STP Root Bridge priority using IOS macros.
- Establish primary and secondary Root Bridge roles for different VLANs.
- Verify STP operations using Cisco IOS show commands.

## Lab Environment

**Platform:** Cisco IOS / Cisco Packet Tracer or compatible Cisco switching lab environment

**Certification Level:** CCNA 200-301

**Difficulty:** 10/10 (as rated by the lab material)

### Network Topology

The lab uses two interconnected switches.

```text
             FastEthernet0/1
       +-------------------------+
       |                         |
   +-------+                 +-------+
   |  Sw1  |=================|  Sw2  |
   +-------+                 +-------+
   |       |                 |       |
   |       |                 |       |
   +-------+                 +-------+

       VLANs 2010, 2020, 2030, 2040
```

**Trunk connection:** FastEthernet0/1 between Sw1 and Sw2.

## VLAN and Root Bridge Design

| VLAN | Primary Root Bridge | Secondary Root Bridge |
|---|---|---|
| 2010 | Sw1 | Sw2 |
| 2020 | Sw2 | Sw1 |
| 2030 | Sw1 | Sw2 |
| 2040 | Sw2 | Sw1 |

This design distributes Root Bridge responsibilities across both switches.

## Task 1: Configure Hostnames and VTP Mode

Since VLANs 2010, 2020, 2030, and 2040 belong to the extended VLAN range, the lab requires configuring both switches in VTP Transparent mode.

### Switch 1

```cisco
enable
configure terminal

hostname Sw1
vtp mode transparent

end
```

### Switch 2

```cisco
enable
configure terminal

hostname Sw2
vtp mode transparent

end
```

## Task 2: Configure VLANs and Trunk Links

Create the required VLANs on both switches.

### VLAN Configuration on Sw1

```cisco
configure terminal

vlan 2010
vlan 2020
vlan 2030
vlan 2040

end
```

### VLAN Configuration on Sw2

```cisco
configure terminal

vlan 2010
vlan 2020
vlan 2030
vlan 2040

end
```

### Configure FastEthernet0/1 as a Trunk

Configure the inter-switch link as a trunk on both switches.

**Sw1:**

```cisco
configure terminal

interface fastEthernet 0/1
 switchport mode trunk
 no shutdown

end
```

**Sw2:**

```cisco
configure terminal

interface fastEthernet 0/1
 switchport mode trunk
 no shutdown

end
```

### Verify VLANs and Trunk Configuration

```cisco
show vlan brief
show interfaces trunk
```

These commands help verify that the VLANs exist and the inter-switch connection is operating as a trunk.

## Task 3: Configure STP Root Bridges Using IOS Macros

Cisco IOS provides two useful configuration macros:

**Root Primary**

```cisco
spanning-tree vlan <vlan-id> root primary
```

This automatically adjusts the switch's STP priority to make it the preferred Root Bridge for the specified VLAN.

**Root Secondary**

```cisco
spanning-tree vlan <vlan-id> root secondary
```

This configures the switch with a priority intended to make it the backup Root Bridge.

### Switch 1 Configuration

Sw1 must become the primary Root Bridge for VLANs 2010 and 2030 and the secondary Root Bridge for VLANs 2020 and 2040.

```cisco
configure terminal

spanning-tree vlan 2010 root primary
spanning-tree vlan 2030 root primary

spanning-tree vlan 2020 root secondary
spanning-tree vlan 2040 root secondary

end
```

### Switch 2 Configuration

Sw2 must become the primary Root Bridge for VLANs 2020 and 2040 and the secondary Root Bridge for VLANs 2010 and 2030.

```cisco
configure terminal

spanning-tree vlan 2020 root primary
spanning-tree vlan 2040 root primary

spanning-tree vlan 2010 root secondary
spanning-tree vlan 2030 root secondary

end
```

## Task 4: Configuration Verification

After configuring both switches, verify the spanning-tree operation.

### 1. Verify the Root Bridge for All VLANs

```cisco
show spanning-tree root
```

This command displays Root Bridge information for the VLANs in the spanning-tree domain.

### 2. Verify a Specific VLAN

On Sw1:

```cisco
show spanning-tree vlan 2010
show spanning-tree vlan 2030
```

On Sw2:

```cisco
show spanning-tree vlan 2020
show spanning-tree vlan 2040
```

### 3. Verify Root Bridge Status

Check the Root ID and bridge information in the output.

When a switch is the Root Bridge, the output should indicate:

```text
This bridge is the root
```

Also inspect:

- Root ID priority.
- Root Bridge MAC address.
- Local Bridge ID.
- Root port.
- Interface roles and states.

### 4. Additional Verification Commands

```cisco
show spanning-tree
show spanning-tree summary
show vlan brief
show interfaces trunk
```

## Understanding STP Priority Values

One important detail in this lab is that the displayed STP priority can look different from the configured base priority.

For example, the lab output for VLAN 2010 on Sw1 shows:

```text
Root ID
Priority 26586
Address 000d.bd06.4100

Bridge ID
Priority 26586 (priority 24576 sys-id-ext 2010)
Address 000d.bd06.4100
```

The displayed priority includes the VLAN System ID Extension.

In this example:

- Base priority: 24576
- VLAN ID: 2010
- Displayed priority: 26586

This is why the priority shown in the command output may not match the base priority configured by the IOS macro.

## Key Networking Concepts Learned

### 1. Spanning Tree Protocol (STP)

STP prevents Layer 2 switching loops by identifying redundant paths and placing selected ports into a blocking state.

### 2. Root Bridge Election

The Root Bridge acts as the reference point for STP path calculations within a VLAN.

The switch with the lowest Bridge ID wins the election. Bridge ID selection considers priority first and MAC address when priorities are equal.

### 3. Root Primary and Root Secondary

The IOS macros simplify STP priority configuration.

- `root primary` makes a switch the preferred Root Bridge.
- `root secondary` makes a switch the preferred backup Root Bridge.

These are intended roles, not absolute guarantees against every possible competing configuration.

### 4. Per-VLAN Spanning Tree

Different VLANs can have different Root Bridges.

This allows network administrators to distribute Layer 2 traffic paths across multiple switches.

### 5. VTP Transparent Mode

VTP Transparent mode allows switches to maintain locally configured VLAN information and is required by this lab's approach to configuring extended-range VLANs.

## Practical Importance

Root Bridge configuration is important in enterprise switching environments because it helps administrators:

- Control Layer 2 topology.
- Manage redundant network paths.
- Distribute traffic across multiple switches.
- Improve network predictability.
- Troubleshoot spanning-tree issues.

## Conclusion

This lab provided practical experience with configuring STP Root Bridges using Cisco IOS macros.

The most important takeaway is that Root Bridge placement should be planned according to the network design rather than left to default switch priorities.

Understanding STP, VLANs, trunk links, and Root Bridge election is an important foundation for managing reliable enterprise Layer 2 networks.

**Skills Practiced:**

- Cisco IOS Configuration
- VLAN Configuration
- VTP Transparent Mode
- Trunk Configuration
- Spanning Tree Protocol
- Root Bridge Election
- STP Priority Management
- Network Verification and Troubleshooting

---

**Lab:** 8 - Spanning-Tree Protocol Root Bridges Using the IOS Macro  
**Focus:** CCNA 200-301 Networking  
**Author:** Beyene Bekele
