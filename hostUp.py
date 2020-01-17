import subprocess
import sys
import socket
import argparse
def check_host_up(host):
    ret = False
    try:
        proc = subprocess.Popen("ping -t5 -c 5 {0} &> /dev/null ; echo $? ".format(host), shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        out, err = proc.communicate()
        out = out.strip()
        err = err.strip()
        if DEBUG:
            print("Out : {0}".format(out))
            print("Error : {0}".format(err))

        if int(out) == 0:
            ret = True
    except Exception as e:
        if DEBUG:
            print("Network Connectivity Exception : {0}".format(e))

    return ret

def check_port(host=None, port=None):
    ret = False
    try:
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.connect((host,int(port)))
        soc.shutdown(socket.SHUT_RDWR)
        ret = True
    except Exception as e:
        if DEBUG:
            print("Socket Connectivity Exception: {0}".format(e))
    finally:
        soc.close()
    return ret

if __name__ == '__main__':
    DEBUG=False
    host = '';
    port = 0;
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', action='store', dest='host',type=str, default=None, help='Host name or IP address of the server')
    parser.add_argument('-p','--port', action='store', dest='port', type=int, default=0, help='Port to be checked for connectivity')
    parser.add_argument('-d', '--debug', action='store_true', dest='debug', default=False, help='Enable Verbose Mode')
    i = parser.parse_args()
    if i.host == None:
        host = input("Hostname:").strip()
    else:
        host = i.host
    if i.port == 0:
        port = input("Port :").strip()
    else:
        port = i.port
    if i.debug:
        DEBUG = True

    if host == '':
        print("Host is required arg")
        sys.exit(1)
    ret = check_host_up(host)
    if ret == True:
        print("Host : {0} is UP".format(host))
    else:
        print("Host : {0} is NOT Reachable".format(host))
    if port != '' and port != 0:
        ret = check_port(host, port)

        if ret == True:
            print("Host : {0} has port : {1} as Available".format(host, port))
        else:
            print("Host : {0} has port : {1} as UN-Available".format(host, port))


