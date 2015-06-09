Exec { path => [ "/bin/", "/sbin/" , "/usr/bin/", "/usr/sbin/" ] }

exec { 'apt-get update':
  command => 'apt-get update',
  timeout => 60,
  tries   => 3
}

class { 'apt':
  always_apt_update => true,
}

package { ['python-software-properties']:
  ensure  => 'installed',
  require => Exec['apt-get update'],
}

$sysPackages = ['git', 'curl', 'supervisor', 'mongodb-server', 'redis-server', 'python-pip', 'python-dev', 'libpython-dev']
package { $sysPackages:
  ensure => "installed",
  require => Exec['apt-get update'],
}

class { 'nodejs':
  version => 'stable',
  make_install => false,
}

package { 'bower':
  provider => 'npm',
  require  => Class['nodejs']
}

#class { 'python' :
#    version    => 'system',
#    pip        => true,
#    dev        => true,
#    gunicorn   => true,
#  }

python::requirements { '/tmp/requirements.txt': }
