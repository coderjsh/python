
#!/usr/bin/python3
from time import sleep
import json
from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException
import logging
logging.basicConfig(filename='test.log', level=logging.DEBUG)
logger = logging.getLogger("netmiko")


def main():
    hosts_ssh = (                  #Put all the IP's from the branches. Below Eg:
                 '10.111.11.11',
                 )
    f = open(f"Ping.csv", "w")
    for i in hosts_ssh:
        cisco_881 = {
            'device_type': 'cisco_ios',
            'host':   i,
            'username': 'Your_Username',  # Put your username
            'password': 'Your_Password',  # Your Password
            'port' : 22,          # optional, defaults to 22
            'fast_cli': True
            #'session_log' : "test.txt"
        }
        #print(cisco_881)

        print(f"Connecting to device {i}.")
        try:
            c = ConnectHandler(**cisco_881)
            print(f"Connection complete to {i}, Fetching the output.")
            hostname = c.send_command('sh run | i hostname').split()[1]
            output1 = c.send_command('ping 10.217.108.1 re 2') # Voice server IP 
            output2 = c.send_command('ping 10.217.101.1 re 2')
            print(f"Writing file to Ping.csv")
            f = open(f"Ping.csv", "a")
            f.writelines(f"***Output for {hostname}***\n")
            f.writelines(output1 + "\n" + output2 + "\n" + "*" * 40 + "\n")
        except (NetmikoTimeoutException, NetmikoAuthenticationException) as Error:
            output3 = str(Error)
            print(f"Writing file to Ping.csv")
            f = open(f"Ping.csv", "a")
            f.writelines(f"***Output for {i}***\n")
            f.writelines(output3 + "\n" + "*" * 40 + "\n")
            continue
    f.close()
    print(f"\nPing.csv file is ready!!")
    print("*"*40)


if __name__ == "__main__":
    main()

