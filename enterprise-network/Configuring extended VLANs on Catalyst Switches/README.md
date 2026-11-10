#       Configuring Extended VLANs on Catalyst Switches

## 🎯 Lab Objective
The objective of this lab exercise is to learn and understand how to configure extended-range VLANs (1006–4096) on Cisco Catalyst IOS switches, and how to use Cisco IOS commands to validate your configuration.

## 📌 Metadata
* **Certification Target:** CCENT / CCNA
* **Lab Difficulty:** 5 / 10
* **Time Limit:** 10 minutes
* **Topics Covered:** VTP Transparent Mode, Extended Range VLANs, Access Port Assignment

---

## 💡 Lab Purpose
In modern network architectures, extended VLANs (IDs 1006 through 4096) are frequently used for larger deployments. Cisco IOS requires specific switch operating conditions (such as VTP Transparent mode) to enable extended VLAN creation.

---

## 🔑 Key Concept: VTP Modes & Extended VLANs
* **VTP Server Mode (Default):** Only supports standard VLAN IDs (1–1005). Attempting to create an extended VLAN in Server mode triggers an error:
  ```text
  Extended VLANs not allowed in VTP SERVER mode
  Failed to commit extended VLAN(s) changes.
  ```
* **VTP Transparent Mode:** Required to create extended-range VLANs (1006–4096) on standalone or Catalyst switches.

---

## 📝 Tasks

* **Task 1:** Configure a hostname on `Sw1`. Set VTP mode to **Transparent** and create the following extended VLANs:
  * VLAN 2010: `SALES`
  * VLAN 2020: `MANAGERS`
  * VLAN 2030: `ENGINEERS`
  * VLAN 2040: `SUPPORT`
* **Task 2:** Configure ports `FastEthernet0/5` – `FastEthernet0/8` as access ports and assign them to the specified extended VLANs.
* **Task 3:** Verify your VLAN configuration.

---

## 🛠️ Configuration & Verification

### Task 1: VTP Mode & Extended VLAN Creation
```text
Switch# configure terminal
Switch(config)# hostname Sw1
Sw1(config)# vtp mode transparent
Setting device to VTP TRANSPARENT mode.

Sw1(config)# vlan 2010
Sw1(config-vlan)# name SALES
Sw1(config-vlan)# exit

Sw1(config)# vlan 2020
Sw1(config-vlan)# name MANAGERS
Sw1(config-vlan)# exit

Sw1(config)# vlan 2030
Sw1(config-vlan)# name ENGINEERS
Sw1(config-vlan)# exit

Sw1(config)# vlan 2040
Sw1(config-vlan)# name SUPPORT
Sw1(config-vlan)# exit
```

### Task 2: Access Port Assignment
```text
Sw1(config)# interface FastEthernet0/5
Sw1(config-if)# switchport mode access
Sw1(config-if)# switchport access vlan 2010
Sw1(config-if)# exit

Sw1(config)# interface FastEthernet0/6
Sw1(config-if)# switchport mode access
Sw1(config-if)# switchport access vlan 2020
Sw1(config-if)# exit

Sw1(config)# interface FastEthernet0/7
Sw1(config-if)# switchport mode access
Sw1(config-if)# switchport access vlan 2030
Sw1(config-if)# exit

Sw1(config)# interface FastEthernet0/8
Sw1(config-if)# switchport mode access
Sw1(config-if)# switchport access vlan 2040
Sw1(config-if)# exit
```

### Task 3: Verification
Verify configuration using:
```text
Sw1# show vlan brief
```

---

## 🔍 Command Reference
| Command | Purpose |
| :--- | :--- |
| `vtp mode transparent` | Changes switch VTP mode to transparent to support extended VLANs |
| `show vlan brief` | Verifies active extended VLANs and port assignments |
| `show vtp status` | Confirms VTP mode is set to Transparent |
