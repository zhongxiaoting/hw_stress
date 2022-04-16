#!/bin/bash
if [ -e /var/tmp/times.log ] && [ -w /var/tmp/times.log ];then
	times=`awk '{print $1}' /var/tmp/times.log|cut -d"=" -f2`
	if [ $times -gt 1 ];then
		let times=times-1
		echo "times=$times" >/var/tmp/times.log
		echo "times=$times `date +"%T_%F"` Reboot sucess" >>/home/hw_stress/log/reboot.log
		# cd /opt/ltp/
#		# ./runltp -t 300s | tee /home/linux_reboot/$times.log
		/sbin/reboot
	fi
fi
