Discord Promo Checker

A fast and lightweight Discord promo checking utility designed to validate promotional codes and organize reward information efficiently. Supports multi-threading, proxy usage, webhook logging, and detailed promo status checking for large-scale promo verification workflows.

Features
Discord promo validation
Valid / invalid promo detection
Redeemed promo detection
Expired promo detection
Multi-threaded execution
Optional proxy support
Webhook logging support
Fast checking speeds
Organized output system
Config-based setup
Automatic retry handling
Real-time console statistics
Proxy rotation support
Duplicate removal system
Files
main.py            # Main checker program
config.yaml        # Configuration file
promos.txt         # Promo list to check
proxies.txt        # Proxy list (optional)

output/
├── Valid.txt
├── Invalid.txt
├── Redeemed.txt
└── Expired.txt
Requirements
Python 3.10+
pip
Windows / Linux supported
Installation

Clone the repository:

git clone <your-repo-url>
cd <your-folder>

Install dependencies:

pip install -r requirements.txt
Configuration
config.yaml

Controls threading, proxies, and webhook settings.

Example:

threads: 50
use_proxy: true
proxy_file: proxies.txt
webhook_url: ""
Key	Type	Description
threads	integer	Number of concurrent worker threads
use_proxy	boolean	Enable or disable proxies
proxy_file	string	Proxy list file
webhook_url	string	Webhook for valid promo logs
promos.txt

One promo per line.

Supported formats:

discord.gift/xxxxxxxx
https://discord.com/billing/promotions/xxxxxxxx
xxxxxxxx
proxies.txt

One proxy per line.

Supported formats:

ip:port
user:pass@ip:port
http://ip:port
http://user:pass@ip:port
Running
python main.py
Output Structure
output/
├── Valid.txt
├── Invalid.txt
├── Redeemed.txt
└── Expired.txt
Valid.txt

Contains all working promotional codes.

Notes
Duplicate promos are automatically removed before checking.
Invalid proxies are skipped automatically.
Rate-limited requests retry automatically.
Multi-threading improves checking speed significantly.
Stable proxies are recommended for large-scale checking.
Webhook logging can be enabled for valid promo notifications.
Disclaimer

This project is intended for educational and authorized usage only. Users are solely responsible for complying with Discord's Terms of Service and all applicable laws. The author assumes no liability for misuse.
