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

$sysPackages = ['git', 'curl', 'supervisor', 'mongodb-server', 'redis-server', 'python-pip', 'python-dev', 'libpython-dev', 'npm', 'nodejs-legacy']
package { $sysPackages:
  ensure => "installed",
  require => Exec['apt-get update'],
}

package { 'bower':
  ensure => present,
  provider => 'npm',
}

#class { 'python' :
#    version    => 'system',
#    pip        => true,
#    dev        => true,
#    gunicorn   => true,
#  }

python::requirements { '/tmp/requirements.txt': }
