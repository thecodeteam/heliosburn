## Development environment

You can get an all-in-one development environment containing all necessary dependencies to start working on Helios Burn coding. Below is the description of the environment and a guide on how to get started as a developer. You can also watch the [YouTube video](https://www.youtube.com/watch?v=PSXemMqiqIU) which explains the same information.

The development environment is provided as a Vagrant box.

### Characteristics

- **Storage**: 40GB
- **CPU**: 2 x vCPU
- **Base memory**: 1024 MB
- **OS**: Ubuntu Trusty (64 bits)
- **Username**: vagrant
- **Password**: vagrant

### Requirements:

1. Vagrant
2. VirtualBox

### Get the development environment

First, make a clone the repository into your local filesystem. Don't forget the `--recursive` parameter to download the Puppet modules.

```git clone --recursive https://github.com/emccode/HeliosBurn.git```

By default, the host port 8100 forwards to guest port 8000, and host port 9100 forwards to 9000.

If those ports are already in use by another virtual machine or application, you can edit the `Vagrantfile` and modify the host ports.

```
[...]
# Django app
config.vm.network "forwarded_port", guest: 8000, host: 8100

# Twisted server
config.vm.network "forwarded_port", guest: 9000, host: 9100
[...]
```

Next, you can run `vagrant up` to get the Vagrant box and provision it. Note that this will take a while since it will need to download the VM image from the repository and install all the dependencies.

### Update dependencies

Whenever we modify the dependencies you can just run `vagrant reload` to stop and start the box again and load any new modifications. When the box is up and running again, you can run `vagrant provision` to incorporate the new packages.


### PostgreSQL credentials

- **Root user**: postgres
- **Root password**: postgres
- **Database**: heliosburn
- **User**: heliosburn
- **Password**: heliosburn


### Configure PyCharm to work on the Vagrant VM

Even though you can use the editor you feel more comfortable with, PyCharm is the preferred IDE to work with the project. Next we provide a tutorial about how to configure your local PyCharm to work on the Vagrant VM we have just created.

In PyCharm, make sure that Vagrant plugin is enabled: on the main toolbar, click Preferences, and in the Settings dialog box, open the page Plugins.

![developers-pycharm-vagrant_1](https://github.com/emccode/HeliosBurn/blob/master/docs/figures/developers-pycharm-vagrant_1.png)

Now click on the Project Interpreter section. You would normally have the system Python interpreter. Click on the settings wheel and select Add Remote to configure a remote Python interpreter.

![developers-pycharm-vagrant_2](https://github.com/emccode/HeliosBurn/blob/master/docs/figures/developers-pycharm-vagrant_2.png)

Select the Vagrant option and configure your project root directory in the Vagrant Instance Folder field. It will probably ask you to start the Vagrant box if it not already running. After the VM is running, PyCharm will fill the rest of fields automatically.

![developers-pycharm-vagrant_3](https://github.com/emccode/HeliosBurn/blob/master/docs/figures/developers-pycharm-vagrant_3.png)
