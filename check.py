import os
import aiohttp
import asyncio
import tasksio
from colorama import Fore, Style, init
from dateutil import parser
import datetime
import requests
import sys

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

init(autoreset=True)

# ---------------- SYSTEM ----------------
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def title(t):
    os.system(f"title {t}")

def ts():
    now = datetime.datetime.now()
    return f"{now.hour:02d}:{now.minute:02d}:{now.second:02d}"

def log(message, log_type="info"):
    tags = {
        "success": (f"{Fore.GREEN}{Style.BRIGHT}COP{Style.RESET_ALL}", Fore.GREEN),
        "info":    (f"{Fore.CYAN}{Style.BRIGHT}INF{Style.RESET_ALL}", Fore.CYAN),
        "warning": (f"{Fore.YELLOW}{Style.BRIGHT}WAR{Style.RESET_ALL}", Fore.YELLOW),
        "error":   (f"{Fore.RED}{Style.BRIGHT}DBG{Style.RESET_ALL}", Fore.RED),
    }
    tag, color = tags.get(log_type, tags["info"])
    print(f"{Style.DIM}{ts()}{Style.RESET_ALL}  {tag}  {Fore.WHITE}{message}{Style.RESET_ALL}")

# ---------------- START ----------------
clear()
title("VAMPIRE | HORROR CYAN")
clear()

print()
log("Enter Delay Between Checks", "info")
delay = float(input(">>> "))

log("Verifying token...", "info")

# ---------------- TOKEN ----------------
token = "MTUwNTUwNDczNjg2MDcwMDc2NQ.GqhUlT.RTKpQMiJJekqYJFcJr-qyUqAkG2ovK9h65IiPU"
auth = {"Authorization": f"Bot {token}"}

r = requests.get("https://ptb.discord.com/api/v10/users/@me", headers=auth)
if r.status_code not in (200, 201, 204):
    log("Invalid token", "error")
    sys.exit()

log("Token verified", "success")

# ---------------- FILE HELPERS ----------------
def load_existing(file):
    if not os.path.exists(file):
        return set()
    return set(open(file, "r", encoding="utf-8").read().splitlines())

valid_cache = load_existing("valid.txt")

def save_unique(file, data, cache):
    if data not in cache:
        cache.add(data)
        with open(file, "a", encoding="utf-8") as f:
            f.write(data + "\n")

# ---------------- CHECKER ----------------
async def check(promocode):
    async with aiohttp.ClientSession(headers=auth) as cs:
        async with cs.get(
            f"https://ptb.discord.com/api/v10/entitlements/gift-codes/{promocode}"
        ) as rs:

            if rs.status in (200, 201, 204):
                data = await rs.json()
                if data["uses"] == data["max_uses"]:
                    log(f"Claimed | {promocode}", "warning")
                else:
                    try:
                        now = datetime.datetime.utcnow()
                        exp_at = data["expires_at"].split(".")[0]
                        parsed = parser.parse(exp_at)
                        days = abs((now - parsed).days)
                    except:
                        exp_at = "Unknown"
                        days = "?"

                    log(f"VALID | {days} days | Expires: {exp_at}", "success")
                    save_unique(
                        "valid.txt",
                        f"https://discord.com/billing/promotions/{promocode}",
                        valid_cache
                    )
            else:
                log(f"Invalid | {promocode}", "error")

# ---------------- MAIN ----------------
async def start():
    if not os.path.exists("promotions.txt"):
        log("promotions.txt missing", "error")
        return

    codes = [c for c in open("promotions.txt").read().splitlines() if c.strip()]
    log(f"Loaded {len(codes)} promo code(s)", "info")

    async with tasksio.TaskPool(workers=300) as pool:
        for promo in codes:
            code = promo.replace("https://discord.com/billing/promotions/", "") \
                        .replace("https://promos.discord.gg/", "") \
                        .replace("/", "")
            await pool.put(check(code))
            await asyncio.sleep(delay)

    open("promotions.txt", "w").close()
    log("All promos checked", "success")

# ---------------- RUN ----------------
if __name__ == "__main__":
    asyncio.run(start())
