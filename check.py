import os
import aiohttp
import asyncio
import tasksio
from colorama import Fore, Style, init
from dateutil import parser
import datetime

init(autoreset=True)

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def title(t):
    os.system(f'title "{t}"')

GREY  = '\x1b[90m'
RESET = Style.RESET_ALL
CYAN  = Fore.CYAN
WHITE = Fore.WHITE
BOLD  = Style.BRIGHT
DIM   = Style.DIM

def ts():
    n = datetime.datetime.now()
    return f"{n.hour:02d}:{n.minute:02d}:{n.second:02d}"

def log_cop(msg):
    print(f"{GREY}{ts()}{RESET}  {Fore.GREEN}{BOLD}COP{RESET}  {WHITE}{msg}{RESET}")

def log_inf(msg):
    print(f"{GREY}{ts()}{RESET}  {CYAN}{BOLD}INF{RESET}  {WHITE}{DIM}{msg}{RESET}")

def log_war(msg):
    print(f"{GREY}{ts()}{RESET}  {Fore.YELLOW}{BOLD}WAR{RESET}  {WHITE}{msg}{RESET}")

def log_dbg(msg):
    print(f"{GREY}{ts()}{RESET}  {Fore.RED}{BOLD}DBG{RESET}  {WHITE}{msg}{RESET}")

def ask(txt):
    print(f"\n{GREY}{ts()}{RESET}  {CYAN}{BOLD}INF{RESET}  {WHITE}{txt}{RESET}")

clear()
title("VAMPIRE | HORROR CYAN")

ask("Enter Delay Between Checks")
delay = float(input(">>> "))

auth  = {}

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

async def check(promocode):
    async with aiohttp.ClientSession(headers=auth) as cs:
        async with cs.get(
            f"https://ptb.discord.com/api/v10/entitlements/gift-codes/{promocode}"
        ) as rs:
            if rs.status in (200, 201, 204):
                data = await rs.json()
                if data["uses"] == data["max_uses"]:
                    log_war(f"Claimed  |  {promocode}")
                else:
                    try:
                        now    = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
                        exp_at = data["expires_at"].split(".")[0]
                        parsed = parser.parse(exp_at)
                        days   = abs((now - parsed).days)
                    except Exception:
                        exp_at = "Unknown"
                        days   = "?"
                    log_cop(f"VALID  |  {days} days  |  Expires: {exp_at}")
                    save_unique(
                        "valid.txt",
                        f"https://discord.com/billing/promotions/{promocode}",
                        valid_cache
                    )
            else:
                log_dbg(f"Invalid  |  {promocode}")

async def start():
    if not os.path.exists("promotions.txt"):
        log_dbg("promotions.txt missing")
        return

    codes = [c for c in open("promotions.txt").read().splitlines() if c.strip()]
    log_inf(f"Loaded {len(codes)} promo code(s)")

    async with tasksio.TaskPool(workers=300) as pool:
        for promo in codes:
            code = (
                promo
                .replace("https://discord.com/billing/promotions/", "")
                .replace("https://promos.discord.gg/", "")
                .replace("/", "")
            )
            log_inf(f"Checking  |  {code[:30]}...")
            await pool.put(check(code))
            await asyncio.sleep(delay)

    open("promotions.txt", "w").close()
    log_cop("All promos checked")

if __name__ == "__main__":
    asyncio.run(start())
