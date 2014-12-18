Helios Burn development environment
===================================

There is an all-in-one development environment containing all necessary tools and applications to start working on Helios Burn coding.

The development environment is provided as a Vagrant box, which will be updated periodically to include any future requirements.

## Characteristics

- **Download Size**: 1.7GB
- **Storage**: 80GB
- **CPU**: 2 x vCPU
- **Base memory**: 1024 MB
- **OS**: Ubuntu Precise (64 bits)
- **Username**: vagrant
- **Password**: vagrant
- **Box URL**: https://atlas.hashicorp.com/emccode/boxes/heliosburn-dev
- **Latest box version**: 0.1

## Requirements:

1. Vagrant
2. VirtualBox

## Get the development environment

1. ```git clone https://github.com/emccode/HeliosBurn.git```
2. ```cd HeliosBurn```
3. ```cd dev-environment```
4. ```vagrant up```

Optionally, you can modify the amount of memory assigned to the VM by updating the Vagrantfile:

```
[...]
config.vm.provider "virtualbox" do |vb|
    vb.gui = true
    # You can customize the amount of memory for the VM
    vb.memory = "1024"
  end
[...]
```

## PostgreSQL credentials

- **User**: postgres
- **Password**: postgres

## Tools and applications installed:

| Name | Version |
|------|---------|
| python | 2.7.3 |
|Git |1.7.9.5 |
|PostgreSQL server | 9.3 |
|Pycharm Professional | 4.0.2 |
|pip | 1.0 |
|pgAdmin3 | 1.18.1 |
|Firefox | 34.0 |
|JDK | 1.7 |
|DbSchema | |
| Django | 1.7.1 |
| twisted | 14.0.2 |
| SQLAlchemy | 0.9.8 |
| django-bootstrap3 | 5.0.3 |
| djangorestframework | 3.0.1 |
| CherryPy | 3.6.0 |
