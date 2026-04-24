import requests
import os
from dotenv import load_dotenv

load_dotenv()

ABUSE_API_KEY = os.getenv("ABUSE_API_KEY")
IPINFO_KEY = os.getenv("IPINFO_KEY")

def threat_level(score):
    if score < 20:
        return "Safe"
    elif score < 60:
        return "Suspicious"
    else:
        return "Malicious"

def check_ip(ip):

    abuse_url = "https://api.abuseipdb.com/api/v2/check"

    headers = {
        "Key": ABUSE_API_KEY,
        "Accept": "application/json"
    }

    params = {
        "ipAddress": ip,
        "maxAgeInDays": 90
    }

    abuse_response = requests.get(abuse_url, headers=headers, params=params).json()
    ipinfo_response = requests.get(f"https://ipinfo.io/{ip}/json?token={IPINFO_KEY}").json()

    loc = ipinfo_response.get("loc", "0,0").split(",")

    return {
        "ip": ip,
        "country": ipinfo_response.get("country", "N/A"),
        "org": ipinfo_response.get("org", "N/A"),
        "reports": abuse_response.get("data", {}).get("totalReports", 0),
        "confidence_score": abuse_response.get("data", {}).get("abuseConfidenceScore", 0),
        "threat_level": threat_level(
            abuse_response.get("data", {}).get("abuseConfidenceScore", 0)
        ),
        "lat": float(loc[0]),
        "lon": float(loc[1])
    }