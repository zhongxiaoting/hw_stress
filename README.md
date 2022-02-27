# 项目说明

## 启动开始项目

```
'使用方法:'
'1.如果想进行完整测试请输入: ./start_test.sh '
'2.如果想单独进行第2个大项测试请输入: ./start_test.sh  2'
'3.如果想对单个模块(第2个大测试模块的第3个子模块)进行验证请按如下输入: '
'./start_test.sh 2 3'
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