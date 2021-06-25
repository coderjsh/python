
#!/usr/bin/python3

from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException
from stdiomask import getpass
from sys import exit
from tabulate import tabulate
from os import getcwd
from time import sleep
def main():
    hosts_ssh = []
    ssh_branches = {       # Add all the branch IP's  Here. Eg below. Or else Login with Hostname if DNS is enabled on your machine
        #"bos-3560a": "10.203.108.11",
        #"dal-3560b": "10.209.108.12",
    }
    ping_list_branches = [  # Enter only IP's to be pinged. No hostname
        "10.217.107.1",
        "10.217.108.1",
    ]
    list_output_working_2 = []
    list_output_not_working = []
    list_hostname = []
    final_output_working = []
    final_output_not_working = []
    headers = ["From", "To", "Success Rate"]
    branch_list = str(input("Enter branch hostname or IP to log into (Use ',' for multiple branches): ")).split(",")
    for i in branch_list:
        if i == "":
            exit("Enter a Branch name and Try again!")
        i = i.lower().replace(" ", "")
        for k, v in ssh_branches.items():
            if i == k:
                hosts_ssh.append(v)
                break
        else:
            hosts_ssh.append(i)
    print("Branches Entered:", hosts_ssh)
    print("Enter creds to login to the device.")
    username = input("Enter Username: ")
    password = getpass(prompt='Enter Password: ')

    for i in hosts_ssh:
        cisco_881 = {
            'device_type': 'cisco_ios',
            'host':   i,
            'username': username,
            'password': password,
            'port' : 22,          # optional, defaults to 22
            'fast_cli': True
        }

        print(f"Connecting to device {i} and Fetching the output.")
        try:
            c = ConnectHandler(**cisco_881)
            hostname = c.send_command('sh run | i hostname').split()[1]
            list_output_working_1 = []
            for ping_output in ping_list_branches:
                output = c.send_command(f'ping {ping_output} repeat 2')
                list_output_working_1.append(output)
            list_hostname.append(hostname)
            list_output_working_2.append(list_output_working_1)

        except (NetmikoTimeoutException, NetmikoAuthenticationException) as Error:
            list_output_not_working.append([i])
            continue

    print("\nProcessing data and Dumping output in a text file.\n")
    list_output_working = zip(list_hostname, list_output_working_2)
    for host, op1 in list_output_working:
        ### For Output 1 ###
        for _ in op1:
            split_op1 = list(_.split())
            if "!" in split_op1[16]:
                final_output_working.append([host, split_op1[11].split(',')[0], split_op1[20] + "%"])

            else:
                final_output_not_working.append([host, split_op1[11].split(',')[0], "0%"])


    f = open(f"Ping.txt", "w")
    if final_output_working != []:
        f.writelines(tabulate(final_output_working, headers, tablefmt="pretty") + "\n" + "*"*60 + "\n")
    if final_output_not_working != []:
        f.writelines(tabulate(final_output_not_working, headers, tablefmt="pretty") + "\n" + "*" * 60 + "\n")
    if list_output_not_working != []:
        f.writelines(tabulate(list_output_not_working, headers=["Unable to connect to below devices"], tablefmt="pretty") + "\n" + "*"*60 + "\n")
    f.close()
    sleep(1)
    print("*"*40)
    print(f"Ping.csv file is ready!! File saved in {getcwd()}")
    print("*"*40)
    sleep(5)


if __name__ == "__main__":
    main()

