import requests
from colorama import Fore, Style, init
import time
import threading

init(autoreset=True)

def loading_animation(stop_event):
    animation = "|/-\\"
    idx = 0
    while not stop_event.is_set():
        print(f"\r{Fore.CYAN}IP checking... {animation[idx % len(animation)]}", end="")
        idx += 1
        time.sleep(0.2)

def get_ip():
    stop_event = threading.Event()
    thread = threading.Thread(target=loading_animation, args=(stop_event,))
    thread.start()

    try:
        response = requests.get("https://ipleak.net/json/")
        if response.status_code == 200:
            data = response.json()
        else:
            print(f"\n{Fore.YELLOW}WARNING: Received status code {response.status_code} from ipleak.net{Style.RESET_ALL}")
            data = response.json() if response.content else {}
        
        ip = data.get("ip", "Unknown")
        country = data.get("country_name", "Unknown")
        region = data.get("region_name", "Unknown")
        city = data.get("city_name", "Unknown")

        is_tor = check_tor(ip)
        tor_status = "Yes" if is_tor else "No"
        
        stop_event.set()
        thread.join()

        print(f"\n\n{Fore.GREEN}       IP INFORMATION\n{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f" ━{Fore.BLUE} Your IP:  {Fore.RED}{ip}")
        print(f" ━{Fore.BLUE} Tor:      {Fore.GREEN if is_tor else Fore.RED}{tor_status}")
        print(f" ━{Fore.BLUE} Country:  {Fore.YELLOW}{country}")
        print(f" ━{Fore.BLUE} Region:   {Fore.WHITE}{region}")
        print(f" ━{Fore.BLUE} City:     {Fore.WHITE}{city}")
        print(f"{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}\n")
    except requests.exceptions.RequestException as e:
        stop_event.set()
        thread.join()
        print(f"{Fore.RED}ERROR: An error occurred while trying to retrieve IP information: {e}{Style.RESET_ALL}")

def check_tor(ip):
    try:
        response = requests.get("https://check.torproject.org/torbulkexitlist", timeout=3)
        if response.status_code == 200:
            exit_nodes = response.text.splitlines()
            return ip in exit_nodes
        else:
            print(f"{Fore.RED}ERROR: Could not check Tor status{Style.RESET_ALL}")
            return False
    except requests.exceptions.Timeout:
        return False
    except Exception as e:
        print(f"{Fore.RED}ERROR: An exception occurred: {e}{Style.RESET_ALL}")
        return False

get_ip()
