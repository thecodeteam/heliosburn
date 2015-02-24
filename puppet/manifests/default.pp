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

$sysPackages = ['git', 'curl', 'postgresql-server-dev-9.3', 'ipython-notebook', 'mongodb-server', 'mongodb-clients']
package { $sysPackages:
  ensure => "installed",
  require => Exec['apt-get update'],
}

class { 'python' :
    version    => 'system',
    pip        => true,
    dev        => true,
    gunicorn   => true,
  }

python::requirements { '/tmp/requirements.txt': }

class { 'java':
  distribution => 'jre',
}

class { 'postgresql::server':
  ip_mask_allow_all_users    => '0.0.0.0/0',
  listen_addresses           => '*',
  postgres_password          => 'postgres',
}

postgresql::server::db { 'heliosburn':
  user     => 'heliosburn',
  password => postgresql_password('heliosburn', 'heliosburn'),
}


include redis
