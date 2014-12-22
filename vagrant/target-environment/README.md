Helios Burn target environment
===================================

This environment contains all needed dependencies to run Helios Burn.

The target environment is provided as a Vagrant box, which will be updated periodically to include any future requirements.

## Characteristics

- **Download Size**: ? GB
- **Storage**: ? GB
- **CPU**: 2 x vCPU
- **Base memory**: ? MB
- **OS**: Ubuntu Server 14.04.1 LTS (64 bits)
- **Username**: vagrant
- **Password**: vagrant
- **Box URL**: https://atlas.hashicorp.com/emccode/boxes/heliosburn-target
- **Latest box version**: 0.1

## Requirements:

1. Vagrant
2. VirtualBox

## Get the development environment

1. ```git clone https://github.com/emccode/HeliosBurn.git```
2. ```cd HeliosBurn/vagrant/target-environment```
4. ```vagrant up```

## PostgreSQL credentials

- **User**: postgres
- **Password**: postgres

## Tools and applications installed:

| Name | Version |
|------|---------|
| python | 2.7.6 |
|Git |1.7.9.5 |
|PostgreSQL server | 9.3 |
|pip | 1.5.4 |
|RabbitMQ |  |
| Django | 1.7.1 |
| twisted | 14.0.2 |
| djangorestframework | 3.0.1 |
| CherryPy | 3.6.0 |
| psycopg2 | 2.5.4 |
