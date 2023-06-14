import requests


def get_public_ip():
    try:
        response = requests.get("https://api.ipify.org?format=json")
        if response.status_code == 200:
            data = response.json()
            ip_address = data["ip"]
            return ip_address
        else:
            return None
    except requests.exceptions.RequestException:
        return None


def details():
    try:
        ip = get_public_ip()
        response = requests.get("https://ipinfo.io/" + str(ip))
        return response.json()
    except:
        return {}
