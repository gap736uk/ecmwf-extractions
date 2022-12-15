#!/bin/ksh
export PATH=/usr/local/bin:$PATH
. ~/.profile
. ~/.kshrc
env RSYNC_CONNECT_PROG=`/usr/bin/connect -H proxy.ecmwf.int:2222 %H 873`;
$@
