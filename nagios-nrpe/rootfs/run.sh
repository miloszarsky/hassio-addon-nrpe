#!/usr/bin/env bashio
bashio::log.info "Starting nrpe server..."
mkdir -p /var/run/nagios /etc/nagios/certs /usr/lib/nagios/extra
[ -e "/var/run/nagios/nrpe.pid" ] && rm "/var/run/nagios/nrpe.pid"
ALLOWED_HOSTS=$(bashio::config 'allowed_hosts')
[ -z $(bashio::config 'allowed_hosts') ] && sed -i "s/allowed_hosts=0.0.0.0/allowed_hosts=$ALLOWED_HOSTS/g" /etc/nagios/nrpe.cfg
/usr/bin/nrpe -c /etc/nagios/nrpe.cfg -f -n