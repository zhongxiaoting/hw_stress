
DC冷复位: ipmitool chassis power cycle



DC热复位: reboot

BMC Reset: ipmitool mc reset warm

CPU MCE检测: ras-mc-ctl --summary


LTP测试: ./runltp -p -l /tmp/resultlog.20211221 -d /tmp -o /tmp/ltpscreen.20211221 -t 5m

Stress --CPU:
一:
  stress -c $threadnum-1 -t 86400 (24h)
  threadnum = cat /proc/cpuinfo | grep -c processor

二:
  命令: stress -c $threadnum -t 300     -t 以秒为单位
  CPU 的总核数 corenum 获取方法: cat /proc/cpuinfo | grep -c processor
  每个内核在总 CPU 利用中占的比例: every_core= 100 / corenum
  获取当前 CPU 利用率:  currentcpuuse= us + sys
  当前空闲 cpu 的利用率: freecpu= 100 - currentcpuuse
  线程数量为空闲利用率除以每个和在总 CPU 利用中占的比例: threadnum= freecpu / every_core


MEM --内存
  空闲内存: fre = free -h
  命令: memtester [(fre - 10) * 98%] 5
  memtester是否正在运行: ps -ef | grep memtester | grep "[0-9]$"

Stress --HDD
  如果硬盘是接在raid卡上的，需要先组raid（注意：操作系统所在的盘，值读不写，其他盘做读和写）
  非系统盘命令: fio -filename=/dev/sd* -direct=1 -iodepth 1 -thread -rw=randrw -ioengine=psync -bs=16k -size=2G -numjobs=10 -runtime=60 -group_reporting -name=mytest0
  系统盘命令: fio -filename=/dev/nvme0n1 -direct=1 -iodepth 1 -thread -rw=randread -ioengine=psync -bs=16k -size=2G -numjobs=10 -runtime=60 -group_reporting -name=mytest1
  查询是否有Raid: lspci | grep "RAID"


fio -directory=/test -direct=1 -iodepth 1 -thread -rw=randread -ioengine=psync -bs=16k -size=2G -numjobs=10 -runtime=20 -group_reporting -name=mytest_os

  1、抓取到所有硬盘信息：
    区分系统盘和非系统盘
      sda               8:0    0 447.1G  0 disk
      ├─sda1            8:1    0   200M  0 part /boot/efi
      ├─sda2            8:2    0     1G  0 part /boot
      └─sda3            8:3    0   446G  0 part
        ├─centos-root 253:0    0    50G  0 lvm  /
        ├─centos-swap 253:1    0     4G  0 lvm  [SWAP]
        └─centos-home 253:2    0   392G  0 lvm  /home



NAME            MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT
sda               8:0    0 446.6G  0 disk
sdb               8:16   0 446.6G  0 disk
sdc               8:32   0  10.9T  0 disk
sdd               8:48   0  10.9T  0 disk
sde               8:64   0  10.9T  0 disk
sdf               8:80   0  10.9T  0 disk
sdg               8:96   0  10.9T  0 disk
sdh               8:112  0  10.9T  0 disk
sdi               8:128  0  10.9T  0 disk
sdj               8:144  0  10.9T  0 disk
sdk               8:160  0  10.9T  0 disk
sdl               8:176  0  10.9T  0 disk
nvme0n1         259:0    0   1.5T  0 disk
├─nvme0n1p1     259:1    0   200M  0 part /boot/efi
├─nvme0n1p2     259:2    0     1G  0 part /boot
└─nvme0n1p3     259:3    0   1.5T  0 part
  ├─centos-root 253:0    0    50G  0 lvm  /
  ├─centos-swap 253:1    0     4G  0 lvm  [SWAP]
  └─centos-home 253:2    0   1.4T  0 lvm  /home
nvme1n1         259:4    0   1.5T  0 disk


[command: lsblk]
['NAME', 'MAJ:MIN', 'RM', 'SIZE', 'RO', 'TYPE', 'MOUNTPOINT']
================
NAME
MAJ:MIN
RM
SIZE
RO
TYPE
MOUNTPOINT
----------------------
['sda', '8:0', '0', '446.6G', '0', 'disk']
================
sda
8:0
0
446.6G
0
disk


  2、对每一个非系统盘进行读写测试
      命令:

   find /sys/devices/ -name "sd*" | grep -E "sd[a-z]+$" |sort

   find /dev/ -name "sd*" | sort   # /dev/sda

   lsblk | grep "sd[a-z]"
   lsblk | grep "nvme[0-9]n1"


   find /sys/devices/ -name "nvme*" | grep -E "nvme[0-9]{1,}$" |sort

Stress --BMC
  BMC网口和板载的另一个网口对接起来，然后通过ipmitool命令设置BMC的IP地址和板载网口在同一个网段，测试的时候可以发送ping命令。



掉盘测试
  检查stress、memtester、fio是否在运行
    lsblk
        检查硬盘是否有丢失


# 网卡压力测试  --LAN
    # 1、筛选出要测试的网口
      ls /sys/class/net | grep -E "enp[a-z0-9]+f[0-1]$"
    # 2、是否网口有连接网线
          没有，终止程序
          有，继续往下进行程序
    # 3、正则出每一个网口的MAC地址
          mac=$(ifconfig $enp |grep -Eo '([[:xdigit:]]{1,2}:){5}[[:xdigit:]]{1,2}')
          放进数组中
    # 4、正则出每一个网口的speed速度，是否达到要求 1G、10G、25G
          speed=$(ethtool $i |grep "Speed: ")
    # 5、设置每一个网口pktgen的参数
          echo rem_device_all >/proc/net/pktgen/kpktgend_0
          echo add_device enp24s0f0 > /proc/net/pktgen/kpktgend_0
          echo count 10000 > /proc/net/pktgen/enp24s0f0
          echo clone_skb 1000 >/proc/net/pktgen/enp24s0f0
          echo pkt_size 1500 >/proc/net/pktgen/enp24s0f0
          echo dst 10.11.11.1 >/proc/net/pktgen/enp24s0f0
          echo dst_mac ${array_mac[$(($j+1))]} >/proc/net/pktgen/enp24s0f0
          echo dst_mac ${array_mac[$(($j-1))]} >/proc/net/pktgen/enp24s0f0
    # 6、检查Result结果是否达到标准传输速率
          查网速：ethtool enp134s0f0  如10G
          # 每隔一小时查一次
               查结果的平均传输速率：cat /proc/net/pktgen/enp134s0f0   如10G - 1G为正常








