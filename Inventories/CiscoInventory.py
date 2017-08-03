#!/usr/bin/python

#use mysql.connector 2.1.4 pip install mysql-connector==2.1.4
import mysql.connector as mariadb
import argparse
import json
import ConfigParser




def output_list_inventory(json_output):
    '''
    Output the --list data structure as JSON
    '''
    print json.dumps(json_output)




def find_host(search_host, inventory):
    '''
    Find the given variables for the given host and output them as JSON
    '''
    host_attribs = inventory.get(search_host, {})
    print json.dumps(host_attribs)



# for ip,username,password,enable in cursor:
#     cisco_inv['ciscoios']['hosts'].append(ip)
#print(cisco_inv)

def main():
    config = ConfigParser.ConfigParser()
    config.read("config.ini")
    hostname = config.get("CiscoInventory","hostname")
    username = config.get("CiscoInventory","username")
    password = ''
    db = config.get("CiscoInventory","db")
    sqlQuery = "SELECT ip,username,password,enable from dmvpn"
    mariadb_connection = mariadb.connect(host=hostname, user=username, password='', database=db)
    cursor = mariadb_connection.cursor()
    cursor.execute(sqlQuery)
    cisco_inv = {}
    cisco_inv['ciscoios'] = {}
    cisco_inv['ciscoios']['hosts'] = []
    cisco_inv['ciscoios']['vars'] = {}

    # Create the ciscoios group host json output
    for ip, username, password, enable in cursor:
        ip = ip.strip()
        cisco_inv['ciscoios']['hosts'].append(ip)

    # Create the ciscoios host variable json output

    host_vars = {}
    cursor.execute(sqlQuery)
    for ip, username, password, enable in cursor:
        ip = ip.strip()
        host_vars[ip] = {}
        host_vars[ip]['username'] = username.strip()
        host_vars[ip]['password'] = password.strip()
        host_vars[ip]['enable'] = enable.strip()




    # Argument parsing
    parser = argparse.ArgumentParser(description="Ansible dynamic inventory")
    parser.add_argument("--list", help="Ansible inventory of all of the groups",
                        action="store_true", dest="list_inventory")
    parser.add_argument("--host", help="Ansible inventory of a particular host", action="store",
                        dest="ansible_host", type=str)

    cli_args = parser.parse_args()
    list_inventory = cli_args.list_inventory
    ansible_host = cli_args.ansible_host

    if list_inventory:
        output_list_inventory(cisco_inv)

    if ansible_host:
        find_host(ansible_host, host_vars)


if __name__ == "__main__":
    main()


