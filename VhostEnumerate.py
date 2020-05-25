import os
import sys
import requests
import argparse
import threading
import tldextract
from colorama import *
from concurrent.futures import ThreadPoolExecutor

requests.packages.urllib3.disable_warnings()


class vhost():

    def __init__(self):

        init(autoreset=True)
        self.keywords = []
        self.target_list = []
        self.print_lock = threading.Lock()

        if not os.path.exists(args.wordlist):

            print(Fore.MAGENTA+"Wordlist Not Found:",args.list)

            sys.exit()

        else:

            file = open(args.wordlist, "r", encoding="utf-8").read().split("\n")
            filt = list(filter(None, file))

            if not len(filt) > 0:

                print(Fore.MAGENTA+"No keyword found in wordlist")

                sys.exit()

            self.keywords.extend(filt)

            del file
            del filt

        if args.url and not args.list and not args.stdin:

            self.target_list.append(args.url)

        elif args.list and not args.stdin and not args.url:

            if not os.path.exists(args.list):

                print(Fore.MAGENTA+f"List Not Found: {args.list}")

                sys.exit()

            file = open(args.list, "r", encoding="Utf-8").read().split("\n")

            filt = list(filter(None, file))

            if not len(filt) > 0:

                print(Fore.MAGENTA+"No url found in url list")

                sys.exit()

            self.target_list.extend(filt)

            del file
            del filt

        elif args.stdin and not args.list and not args.url:

            [self.target_list.append(x) for x in sys.stdin.read().split("\n") if x]

            if not len(self.target_list) > 0:

                print(Fore.MAGENTA+"No url found in stdin")

                sys.exit()

        else:

            print(Fore.MAGENTA+"You used the wrong Parameters")

            sys.exit()


        self.keywords = list(set(self.keywords))
        self.target_list = list(set(self.target_list))

        self.keywords.sort()
        self.target_list.sort()


        with ThreadPoolExecutor(max_workers=args.thread) as executor:

            for urls in self.target_list:

                if not urls.startswith("https://") and not urls.startswith("http://"):

                    urls = "https://" + urls

                for key in self.keywords:

                    package = [urls,key]

                    executor.submit(self.attack_start, package)

    def attack_start(self,target):

        header1 = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko"}

        header2 = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko", "Host": target[1]}

        try:

            response1 = requests.get(target[0], headers=header1, allow_redirects=True, verify=False, timeout=int(args.timeout))

            response2 = requests.get(target[0], headers=header2, allow_redirects=True, verify=False, timeout=int(args.timeout))

            if response2.status_code == 200 and len(response1.text) != len(response2.text):

                with self.print_lock:

                    print(Fore.RED+"[VHOST FOUND]",Fore.GREEN+target[0],Fore.CYAN+"==>",Fore.MAGENTA+f"Host: {target[1]}")

                if args.output:

                    self.print_now(target)

        except requests.exceptions.ConnectionError:

            fq = tldextract.extract(target[0]).fqdn

            if target[0].startswit("https://"):

                target[0] = "http://" + fq

            else:

                target[0] = "https://" + fq

            response1 = requests.get(target[0], headers=header1, allow_redirects=True, verify=False, timeout=int(args.timeout))
            response2 = requests.get(target[0], headers=header2, allow_redirects=True, verify=False,timeout=int(args.timeout))

            if response2.status_code == 200 and len(response1.text) != len(response2.text):

                with self.print_lock:

                    print(Fore.RED + "[VHOST FOUND]", Fore.GREEN + target[0], Fore.CYAN + "==>",Fore.MAGENTA + f"Host: {target[1]}")

                if args.output:
                    self.print_now(target)

        except Exception as e:
            print(Fore.RED+str(e))

    def print_now(self,target):

        print_value = """Target: {}\nHost: {}\n\n""".format(target[0], target[1])

        with open(args.output, "a+", encoding="utf-8") as f:

            f.write(print_value)

if __name__ == "__main__":

    ap = argparse.ArgumentParser()
    ap.add_argument("-u", "--url", metavar="", required=False, help="Single Target Url")
    ap.add_argument("-l", "--list", metavar="", required=False, help="Read Urls From List")
    ap.add_argument("-s", "--stdin", action="store_true", required=False, help="Read Urls From Stdin")
    ap.add_argument("-w", "--wordlist", metavar="", default="wordlist.txt", required=False, help="Keywords List")
    ap.add_argument("-o", "--output", metavar="", required=False, help="Save Output")
    ap.add_argument("-t", "--thread", metavar="", default=20, type=int, required=False, help="Thread Number (Default-20)")
    ap.add_argument("-tm", "--timeout", metavar="", default=30, type=int, required=False,help="Timeout (Default-30)")

    args = ap.parse_args()

    start_attack = vhost()
