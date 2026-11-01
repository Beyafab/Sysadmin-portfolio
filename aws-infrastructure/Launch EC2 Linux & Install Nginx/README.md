# Deploy a Linux Web Server on AWS EC2 Using Nginx

## Project Overview

This project demonstrates how to launch a Linux virtual server on Amazon Web Services (AWS), configure secure remote access, install the Nginx web server, and verify that the web server is accessible through a browser.

I documented the implementation process with step-by-step screenshots to demonstrate the configuration and deployment workflow.

The project helped me practise cloud infrastructure deployment, Linux system administration, network security, and basic web server management.

## Objectives

- Launch and configure a Linux EC2 instance.
- Configure inbound network access using AWS Security Groups.
- Connect to the server remotely using SSH.
- Install and start the Nginx web server.
- Verify web server availability through a browser.
- Document the implementation process with screenshots.

## Technologies Used

- **AWS EC2:** Virtual server hosting
- **Amazon VPC:** Cloud networking environment
- **AWS Security Groups:** Instance-level network traffic filtering
- **Linux:** Server operating system
- **SSH:** Secure remote administration
- **Nginx:** Web server
- **HTTP:** Web content delivery

## Architecture

```text
              User / Web Browser
                      |
                      | HTTP (Port 80)
                      |
              AWS Security Group
                      |
                      |
                EC2 Instance
                 Linux Server
                      |
                    Nginx
                      |
              Default Web Page
```

**Traffic flow:** A user accesses the EC2 instance's public IPv4 address through a browser. The Security Group permits HTTP traffic on port 80, allowing Nginx to serve the default web page.

SSH access on port 22 is used for remote administration and should be restricted to the administrator's IP address.

## Implementation Steps

### 1. Launch an EC2 Instance

I created an EC2 instance through the AWS Management Console and configured the required instance settings, including the operating system image, instance type, key pair, and network settings.

**Screenshot:** `screenshots/01-ec2-instance.png`

### 2. Configure the Security Group

I configured the instance's Security Group to allow the traffic needed for server administration and web access.

| Protocol | Port | Purpose | Recommended source |
|---|---:|---|---|
| SSH | 22 | Remote server administration | My IP |
| HTTP | 80 | Web server access | `0.0.0.0/0` for a public demo |

HTTPS on port 443 can be configured when TLS is set up.

**Screenshot:** `screenshots/02-security-group.png`

### 3. Connect to the Linux Server Using SSH

I used SSH to establish a secure remote connection to the EC2 instance.

Example command:

```bash
chmod 400 my-key.pem

ssh -i my-key.pem USERNAME@PUBLIC_IP
```

Replace `my-key.pem`, `USERNAME`, and `PUBLIC_IP` with the actual key file, operating-system username, and instance public IP address.

**Screenshot:** `screenshots/03-ssh-connection.png`

### 4. Install Nginx

After connecting to the server, I installed the Nginx web server using the package manager for the Linux distribution.

For Ubuntu:

```bash
sudo apt update
sudo apt install nginx -y
```

For Amazon Linux 2023:

```bash
sudo dnf install nginx -y
```

**Screenshot:** `screenshots/04-nginx-installation.png`

### 5. Start and Verify Nginx

I started the Nginx service and checked its status to confirm that the service was running.

For Ubuntu and Amazon Linux:

```bash
sudo systemctl enable --now nginx
sudo systemctl status nginx
```

**Screenshot:** `screenshots/05-nginx-service-status.png`

### 6. Test Web Server Accessibility

I opened a browser and accessed the EC2 instance using its public IPv4 address:

```text
http://PUBLIC_IP
```

The default Nginx welcome page confirmed that the web server was responding to HTTP requests.

**Screenshot:** `screenshots/06-nginx-web-page.png`

## Testing and Verification

The following checks were used to validate the deployment:

| Test | Expected result |
|---|---|
| EC2 instance status | Instance running |
| SSH connection | Successful remote login |
| Nginx service status | Active and running |
| HTTP access | Nginx page accessible through the browser |
| Security Group configuration | Required ports allowed according to the intended access policy |

These checks help identify common deployment issues, such as incorrect SSH key permissions, missing inbound rules, or an inactive web server.

## Security Considerations

- Restricted SSH access to my IP address rather than exposing port 22 to the entire internet.
- Used SSH key-based authentication for remote administration.
- Allowed only the inbound traffic required for the demonstration.
- Avoided storing private keys, passwords, or AWS credentials in the repository.
- Recognized that a public web server requires ongoing updates and appropriate security controls.

## Challenges and Troubleshooting

Common issues to investigate during deployment include:

- **SSH connection failure:** Check the key file permissions, username, public IP address, route configuration, and SSH Security Group rule.
- **Website not loading:** Verify that Nginx is running, port 80 is allowed, and the instance has the required network connectivity.
- **Nginx service failure:** Review service status and system logs to identify configuration or startup problems.

## Skills Demonstrated

- AWS EC2 instance provisioning
- Linux server administration
- SSH remote connectivity
- Security Group configuration
- Nginx installation and service management
- Basic network troubleshooting
- Technical documentation and screenshot-based reporting

## Future Improvements

- Host a custom HTML landing page instead of the default Nginx page.
- Configure HTTPS using a valid TLS certificate.
- Configure a custom domain name and DNS records.
- Explore automated deployment using Bash scripts.
- Add monitoring and logging for improved operational visibility.
- Explore infrastructure automation using Terraform.

## Conclusion

This project provided practical experience deploying and managing a Linux web server in AWS. It connected cloud computing concepts with Linux administration, networking, and basic security configuration.

It also serves as a foundation for more advanced projects involving cloud infrastructure, automation, monitoring, and secure application deployment.

---

**Author:** Beyene Bekele  
**Focus:** Cloud Infrastructure | Linux Administration | Networking

**Repository:** [Add your GitHub repository URL here]
