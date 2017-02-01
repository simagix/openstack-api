#! /usr/bin/env python
import sys
from novaclient import client as nova_client
from cinderclient import client as cinder_client
from time import sleep

def create_vm(name, image, flavor, network=None, key_name=None, v4_fixed_ip=None, volume=None, floating_ip=None, files=None, userdata=None):
    nics = [{'net-id': network.id}]
    if v4_fixed_ip != None:
        nics = [{'net-id': network.id, 'v4-fixed-ip': v4_fixed_ip}]
        
    server = nova.servers.create(name = name,
        image = image.id,
        flavor = flavor.id,
        key_name = key_name,
        nics = nics,
        files = files,
        userdata=userdata)
#        userdata="#!/bin/bash \n sh +x /tmp/post_install.sh > /tmp/post_install.log")
    if volume != None:
        while server.status != 'ACTIVE':
            sleep(2)
            server = nova.servers.get(server)
        
        nova.volumes.create_server_volume(server.id, volume.id)
    if floating_ip != None:
        server.add_floating_ip(floating_ip)

def get_volume(name):
    try: 
        volume = cinder.volumes.find(name=name)
    except:
        print 'creating volume'
        volume = cinder.volumes.create(name=name, size=10, description='management yum repo')
    return volume

OS_USERNAME='simagix'
OS_PASSWORD='simagix'
OS_TENANT_NAME='simagix'
OS_AUTH_URL='http://10.116.2.22:5000/v2.0'
OS_COMPUTE_API_VERSION=2
nova = nova_client.Client(OS_COMPUTE_API_VERSION, OS_USERNAME, OS_PASSWORD, OS_TENANT_NAME, OS_AUTH_URL)
cinder = cinder_client.Client(OS_COMPUTE_API_VERSION, OS_USERNAME, OS_PASSWORD, OS_TENANT_NAME, OS_AUTH_URL)

# print nova.floating_ips.list()

key_name = 'simagix'
network_name = 'simagix-prinet'
network = nova.networks.find(label = network_name)

image_name = 'CentOS 7'
image = nova.images.find(name = image_name)
flavor = nova.flavors.find(name = 'm1.small')
volume = get_volume('mgmt')
user_data = open('cloud-config.yaml', 'r').read()
post_install = open('post_install.sh', 'r').read()
create_vm('mgmt', image, flavor, network=network, key_name=key_name, volume=volume,
            files={"/tmp/post_install.sh": post_install},
            userdata=user_data,
            v4_fixed_ip='192.168.111.18', floating_ip='10.116.32.111')

# flavor = nova.flavors.find(name = 'm1.tiny')
# create_vm('amqp-1', image, flavor, network=network, key_name=key_name, volume=None, v4_fixed_ip='192.168.111.20')

