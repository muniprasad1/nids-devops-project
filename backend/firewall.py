import os


def block_ip(ip):
    try:
        print(f"[FIREWALL] Blocking IP: {ip}")

        # Windows firewall command
        os.system(f'netsh advfirewall firewall add rule name="Block {ip}" dir=in action=block remoteip={ip}')

    except Exception as e:
        print("Firewall error:", e)