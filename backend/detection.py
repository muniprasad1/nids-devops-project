NORMAL_THRESHOLD = 3
ATTACK_THRESHOLD = 15

# Track suspicious activity per IP
suspicious_count = {}

def detect_attack(rate, ip=None):
    global suspicious_count

    if ip is None:
        ip = "Unknown"

    # 🟢 NORMAL
    if rate < NORMAL_THRESHOLD:
        suspicious_count[ip] = 0   # reset behavior
        return "NORMAL"

    # 🟡 SUSPICIOUS
    elif NORMAL_THRESHOLD <= rate < ATTACK_THRESHOLD:
        suspicious_count[ip] = suspicious_count.get(ip, 0) + 1

        # 🔥 Escalate slower (more realistic)
        if suspicious_count[ip] >= 5:
            return "ATTACK"

        return "SUSPICIOUS"

    # 🔴 ATTACK
    else:
        return "ATTACK"