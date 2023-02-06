#! /usr/bin/env python
import sys
import os
import configparser
import argparse
import logging
from ipaddress import IPv4Network, IPv4Address
import requests



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', required=True, help='Config file to be used')
    parser.add_argument('-l', '--log_level', choices=['INFO', 'DEBUG'], default='INFO', required=False, help='Parser log level DEBUG or INFO')
    parser.add_argument('-f', '--log', required=False, help='Log file path')
    args = parser.parse_args()

configFile = args.config

if args.log_level:
    logging_level = str(args.log_level)
else:
    logging_level = "CRITICAL" 

if args.log:
    log_file = args.log
else:
    log_file = "parser.log"

# Logger configuration
file_handler = logging.FileHandler(filename=log_file)
handlers = [file_handler]

logging.basicConfig(
    level=logging_level,
    format='%(levelname)s: %(message)s',
    handlers=handlers
)

new_logger = logging.getLogger('NEW_LOGGER')

# Reading config file
def ini_parser(config_file_path):
    
    config_params = {}
    if not os.path.exists(config_file_path):
        new_logger.critical("Config file " + config_file_path + " does not exist or not accessible")
        sys.exit(1)
    
    new_logger.debug(f'Loading Configuration from: {config_file_path}')        
    config = configparser.ConfigParser()
    config.read(config_file_path) 

    # Parsing configuration values     
    for key in config['config']:
        config_params[key] = config['config'][key]

    return config_params

# Get appropriate information from API
def get_api_json(api_url):
    
    headers = {'Accept': 'application/json'}
    
    try:                
        request_result = requests.get(api_url, headers=headers)
        result_json = request_result.json()
        return result_json
    except Exception as e:
        new_logger.error(f'Can\'t get information from API server error is {e}')

# Get servers subnet information
def get_network_info(servers_json, subnet, new_prefix):
    
    try:
        
        new_logger.debug(f'Loaded subnet: {subnet}')
        new_logger.debug(f'Generating new prefix size: {new_prefix}')
        
        # Generating network information using new prefix
        subnets_splitted = list(IPv4Network(subnet).subnets(new_prefix=new_prefix))        
        subnets_splitted_string = " ".join(subnets.exploded for subnets in subnets_splitted)
        
        new_logger.info(f'Generated subnets: [{subnets_splitted_string}]')
        
        # Servers total
        servers_count = len(servers_json)

        # Online servers
        online_servers = list(filter(lambda elem : elem['status'] == 'online', servers_json))        
        servers_list = list(map(lambda d: d['hostname'], online_servers))
        online_servers_count = len(servers_list)
    
        new_logger.debug(f'Loaded {servers_count} servers from API')
        new_logger.debug(f'Filtered {online_servers_count} online servers')
    
        # Check for servers belonging to the subnets provided
        for subnet in subnets_splitted:
        
            subnet_hostnames = []
            subnet_string = str(subnet)
            
            
            for server in online_servers:
            
                server_hostname = server['hostname']
            
                for ip_address in server['ips']:
                    
                    server_ip = ip_address['ip']['ip']
                    server_ip_object = IPv4Address(server_ip)
                                       
                    if server_ip_object in subnet:
                        subnet_hostnames.append(server_hostname)
                        hostname_matched = 'match'
                    else:
                        hostname_matched = 'miss'
                    
                    new_logger.debug(f'Host: {server_hostname} IP: {server_ip_object} Subnet: {subnet} Status: {hostname_matched}')

            servers_with_no_match = list(filter(lambda elem: elem not in subnet_hostnames, servers_list))
            servers_list = servers_with_no_match
                                    
            subnet_hostnames_string = ' '.join(subnet_hostnames)
            hostnames_matched = f'Subnet: {subnet_string} Hosts: [ {subnet_hostnames_string} ]'

            print(hostnames_matched)  
            new_logger.info(hostnames_matched)
        
        srever_list_string = ' '.join(servers_list)
        print(f'Hosts with no subnet match: [ {srever_list_string} ]')
            
    except Exception as e:
        new_logger.error(f'Error occured getting network information {e}')    

config_params = ini_parser(configFile)

api_url = config_params['api_url']
subnet = config_params['subnet']
new_prefix = int(config_params['new_prefix'])

servers_info = get_api_json(api_url)
network_info = get_network_info(servers_info, subnet, new_prefix)
