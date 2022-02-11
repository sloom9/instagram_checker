from os import error
import requests
import random
import time
import threading

thread_num = int(input("Threads? (recommended 20) >>"))

check_url = 'https://www.instagram.com/accounts/web_create_ajax/attempt/'

errs = "username_is_taken username_held_by_others spam timeout"

file = open('./out_users.txt', 'a')

check_head = {
    'Host': 'www.instagram.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.7113.93 Safari/537.36',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'X-CSRFToken': 'alvJKdSarF6XQvCJFeELtd179wGXrWs9',
    'X-Instagram-AJAX': 'b7bf43601366',
    'X-IG-App-ID': '936619743392459',
    'X-ASBD-ID': '437806',
    'X-IG-WWW-Claim': '0',
    'Content-Type': 'application/x-www-form-urlencoded',
    'X-Requested-With': 'XMLHttpRequest',
    'Content-Length': '55',
    'Origin': 'https://www.instagram.com',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Referer': 'https://www.instagram.com/accounts/emailsignup/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'TE': 'trailers'
}


def check_user(username):
    try:
        res = requests.post(url=check_url, headers=check_head, data='email=&username=' + username +'&first_name=&opt_into_one_tap=false')
        if "spam" not in res.text and "fail" not in res.text:
            if 'username_is_taken' in res.text:
                print('[-] User is taken ' + username, end='\r')
            elif 'held_by_others' in res.text:
                print('14-day username >> '+ username)
                file.write('\n[+] 14 Day user >> '+username)
            elif errs not in res.text:
                print("\033[92m" + f'Available user >> {username}')
                file.write("\n[+] Available user >> "+username)
                return username
        else:
            print("\033[91m" + "[-] SPAM detected! try using proxies..", end='\r')
            time.sleep(2)
    except KeyboardInterrupt:
        file.write(f"[-] last username >>{username}")
        exit(0)


with open("./filtered.txt", 'r') as user_file:    
    users_arr = []

    for user in user_file:
        user = user.strip()
        users_arr.append(user)


def check():
    for i in range(len(users_arr)):
        check_user(users_arr[i])


def run_threads():
    Threads = []

    for i in range(int(thread_num)):
        t = threading.Thread(target=check)
        t.daemon = True
        Threads.append(t)
    for i in range(int(thread_num)):
        Threads[i].start()

    for i in range(int(thread_num)):
        Threads[i].join()

run_threads()
