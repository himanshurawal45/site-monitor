from threading import Thread
import requests
import time
import smtplib

import utils

import os

# email sending function


def email_sender(input_message, email_to, client):
    ''' function to send email '''
    to = email_to
    # email of sender account
    gmail_user = os.environ.get("MONITOR_GMAIL_USERNAME")
    # password of sender account
    gmail_pwd = os.environ.get("MONITOR_GMAIL_PASSWORD")
    smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login(gmail_user, gmail_pwd)
    header = f"To:{to} \nFrom: {gmail_user} \nSubject:site down! \n"
    input_message = input_message + client
    msg = header + input_message
    smtpserver.sendmail(gmail_user, to, msg)
    smtpserver.close()


# list of sites to track along with email address to send the alert
clients = {"http://localhost:8080": "some_dummy_email@gmail.com"}

# temporary dictionary used to do separate monitoring when a site is down
sites_down_now = {}

# site 'up' function


def site_up():
    ''' function to monitor up time '''
    while True:
        clients_copy = clients
        for client, email in clients_copy.items():
            try:
                r = requests.get(client)
                if r.status_code == 200:
                    print(client, 'Site ok')
                else:
                    print(
                        client, 'Site first registered as down - added to the "site down" monitoring')
                    sites_down_now[client] = email
            except requests.ConnectionError:
                print(
                    client, 'Site first registered as down - added to the "site down" monitoring')
                sites_down_now[client] = email

        
        time.sleep(5)  # sleep for 1 min

        for key in sites_down_now.keys():
            clients_copy = utils.delete_key_from_dict(clients, key)


# site 'down' function


def site_down():
    ''' function to monitor site down time '''
    while True:
        for client, email in sites_down_now.items():
            try:
                r = requests.get(client)
                if r.status_code == 200:
                    print(client, 'Site is back up!!')
                    email_sender('Site back up!! ', email, client)
                    clients[client] = email
                    del sites_down_now[client]
                else:
                    email_sender('Site down!! ', email, client)
                    print(client, 'Site Currently down - email sent')
            except requests.ConnectionError:
                email_sender('Site down!! ', email, client)
                print(client, 'Site Currently down - email sent')
        time.sleep(10)  # sleeps 15 mins


t1 = Thread(target=site_up)
t2 = Thread(target=site_down)
t1.start()
t2.start()
