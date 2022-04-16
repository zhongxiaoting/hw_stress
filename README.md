# 项目说明

## 启动开始项目

```
使用手册:
1. 打开文件所在的目录: cd /home/hw_stress 
2. 先执行重启和ltp压测操作: cd linux_reboot 
   2.1. 执行: chmod +x install.sh reboot.sh 
   2.2. 执行: ./install.sh 
   2.3. 执行: ./reboot.sh 
   2.4. 修改rc.local权限: chmod +x /etc/rc.d/rc.local
3. 等待执行重启和ltp压测5次之后, 执行文件权限: chmod + x start_test.sh 
4. 安装测试工具: cd shell
   4.1. 执行文件权限: chmod +x tool_install.sh 
   4.2. 运行文件安装压测工具: ./tool_install.sh
5. 如果想进行一键式自动化测试（所有流程自动化测试）,请按如下输入:
   5.1. 输入执行操作: ./start_test.sh 2 1 
   5.2. 输入服务器序列号（SN）: 如 123456 
   5.3. 输入执行操作的时间（以秒为计算）: 如 3600 （1小时）
6. 如果想对单个模块(第2个大测试模块的第3个子模块)进行验证请按如下输入: 
   6.1. CPU MCE 和内存ECC测试: ./start_test.sh 2 2 
   6.2. CPU压测: ./start_test.sh 2 3 
   6.3. 内存压测: ./start_test.sh 2 4 
   6.4. 硬盘压测: ./start_test.sh 2 5 
   6.5. 网卡压测: ./start_test.sh 2 6 
   6.6. 黑名单检查: ./start_test.sh 2 7 
   
7. 查看log日志 
   在hw_stress/log/123456（服务器序列号）/20221439（当前时间文件夹）
   7.1. 123456.log是所有压测的log,包括CPU、内存、硬盘、网卡
   7.2. mce_ecc.log是CPU MCE 和 内存ECC的log
   7.3. cpu_stress.log是CPU压测的log
   7.4. mem_stress.log是内存压测的log
   7.5. disk0.log（disk1.log）是硬盘压测的log
   7.6. lan_stress.log是网卡压测的log
   7.7. blacklistall.log是黑名单检查的log
   7.8. loss_disk.log是硬盘掉盘测试的log
   7.9. /hw_stress/log中的reboot.log日志是重启日志
```

## 文件说明
1. start_test.sh: 开始启动项目调用脚本
2. launch.py: 启动python开始的调用
3. cfg.json: 存放测试项目的配置文件
4. result.log: 存放测试结果的log文件

## 模块说明
1. config: 存放公用的常量文件
2. log_backup: 存放测试log的历史文件
3. main: 测试的主逻辑控制
4. result: 存放每个项目的测试结果的json文件
5. station_final: 存放后测的python模块文件
6. station_func: 存放功能测试python模块文件
7. station_stress: 存放压力测试的python模块文件
8. ui_desktop: 桌面交互开发
9. ui_web: 测试结果的web展示的开发
10. utils: 工具类的文件目录
