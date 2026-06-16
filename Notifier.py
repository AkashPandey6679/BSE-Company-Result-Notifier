import requests
import time

BOT_TOKEN = "BOT TOKEN"
CHAT_ID = "CHAT ID"


BSE_URL = "https://api.bseindia.com/BseIndiaAPI/api/AnnSubCategoryGetData/w"

seen = set()

# ================= TELEGRAM =================

def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg[:4000]})

# ================= FILTER =================

def is_result(desc):
    d = desc.lower()
    return "result" in d or "financial" in d or "board meeting" in d

# ================= FETCH =================

def fetch_bse():
    params = {
        "strCat": "Result",
        "strSearch": "P",
        "strType": "C"
    }

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.bseindia.com/"
    }

    try:
        r = requests.get(BSE_URL, headers=headers, params=params, timeout=8)
        return r.json().get("Table", [])
    except:
        return []

# ================= INIT =================

print("Running... waiting for new results")

# 🔥 Step 1: ignore everything already present
for item in fetch_bse():
    key = str(item.get("SCRIP_CD")) + str(item.get("NEWS_DT"))
    seen.add(key)

# ================= LIVE =================

while True:
    data = fetch_bse()

    for item in data:
        desc = item.get("NEWSSUB", "")

        if not is_result(desc):
            continue

        key = str(item.get("SCRIP_CD")) + str(item.get("NEWS_DT"))

        if key in seen:
            continue

        seen.add(key)

        company = item.get("SLONGNAME")

        # 🔔 ONLY ALERT WHEN NEW RESULT COMES
        msg = f"{company}\n\nResults Announced"
        print("NEW:", company)
        send(msg)

    time.sleep(5)
