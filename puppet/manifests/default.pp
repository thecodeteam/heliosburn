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

$sysPackages = [ 'build-essential', 'git', 'curl']
package { $sysPackages:
  ensure => "installed",
  require => Exec['apt-get update'],
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
