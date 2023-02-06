## General info
Ansible configuration for setting up Wireguard server on Debian host. Docker Composer is used in order to have Wireguard and all related services up and running.

## Usage
1. First of all you need to change inventory file configuration to match your Linux server infromation

Configuration Example:
```yaml
all:
  hosts:
    194.XXX.XXX.XXX:
  vars:
    ansible_port: 22
    ansible_python_interpreter: "/usr/bin/python3"
    ansible_user: "devops"
    ansible_ssh_private_key_file: "~/.ssh/id_ansible"
    operator_accounts:
      - username: devops
        comment: Jevgenij
        pubkey: "ssh-rsa AAAABXXXXXX ..."
        state: present
```
2. Run Ansible

```bash
ansible-playbook -i ./inventories/wire_nodes/wire_nodes.yml ./bootstrap_server.yml
```

3. After Ansible setup completed run this command to get Wireguard client configuration from the server


```bash
ansible -i ./inventories/wire_nodes/wire_nodes.yml -m shell -a "cat ~/wireguard_setup/config/peer1/peer1.conf" all
```
