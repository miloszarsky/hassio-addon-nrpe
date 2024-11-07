#!/bin/sh
mkdir -p /var/run/nagios /etc/nagios/certs /usr/lib/nagios/extra
[ -e "/var/run/nagios/nrpe.pid" ] && rm "/var/run/nagios/nrpe.pid"
/usr/bin/nrpe -c /etc/nagios/nrpe.cfg -f -n