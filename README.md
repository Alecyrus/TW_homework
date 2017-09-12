# TW_homework

> Author: Junkai Huang

> Language: Python 3.5.2

> Platform: Ubuntu 16.04/vim

> Dependence: Redis

## Install
>$ sudo apt-get install redis-server python3-pip

>$ sudo pip3 install redis

## Usage
### Setting.ini
用于配置系统信息，如下
```ini
[basic]
redis_bind_host = 127.0.0.1
redis_bind_port = 6379
redis_bind_dp = 1


badminton_vneues=A,B,C,D
working_day_groups = GroupOne,GroupTwo
working_hours_start = 9
working_hours_end = 22

;分时间段表示价格，(3,30)
;3,表示从前一时间段结束点持续3小时
;30,表示这个时间段的价格
price = 3,30;6,50;2,80;2,60


[GroupOne]
working_days = 1,2,3,4,5

[GroupTwo]
working_days = 6,7
price = 3,40;6,50;4,60

```

### Start

### 附加命令
>`quit`: 退出系统

>`clear`: 清空数据库，重新初始化系统

#### 测试例一
```
Hello! Welcome to Badminton Vneues Management System(BVMS).
Initialize the database.....Done
Initialize the system.....Done
Input 'quit' to exit. 
(BVMS)> abcdefghijklmnopqrst1234567890
ERROR: the booking is invalid!
(BVMS)> U001 2016-06-02 22:00~22:00 A
Success: the booking is accepted!
(BVMS)> U002 2017-08-01 19:00~22:00 A
Success: the booking is accepted!
(BVMS)> U003 2017-08-02 13:00~17:00 B
Success: the booking is accepted!
(BVMS)> U004 2017-08-03 15:00~16:00 C
Success: the booking is accepted!
(BVMS)> U005 2017-08-05 09:00~11:00 D
Success: the booking is accepted!
(BVMS)> 
收⼊汇总:
---
场地:A
2016-06-02 22:00~22:00 0元
2017-08-01 19:00~22:00 180元
⼩计: 180.0元

场地:B
2017-08-02 13:00~17:00 200元
⼩计: 200.0元

场地:C
2017-08-03 15:00~16:00 50元
⼩计: 50.0元

场地:D
2017-08-05 09:00~11:00 60元
⼩计: 60.0元

---
总计: 490.0元
(BVMS)> clear
Are you sure? (Y/N)
Confirm:Y
Deleting....Done
(BVMS)> 
```

#### 测试例二
```
Hello! Welcome to Badminton Vneues Management System(BVMS).
Initialize the database.....Done
Initialize the system.....Done
Input 'quit' to exit. 
(BVMS)> U002 2017-08-01 19:00~22:00 A
Success: the booking is accepted!
(BVMS)> U003 2017-08-01 18:00~20:00 A
Error: the booking conflicts with existing bookings!
(BVMS)> U002 2017-08-01 19:00~22:00 A C
Success: the booking is accepted!
(BVMS)> U002 2017-08-01 19:00~22:00 A C
Error: the booking being cancelled does not exist!
(BVMS)> U003 2017-08-01 18:00~20:00 A
Success: the booking is accepted!
(BVMS)> U003 2017-08-02 13:00~17:00 B
Success: the booking is accepted!
(BVMS)> 
收⼊汇总:
---
场地:A
2017-08-01 18:00~20:00 120元
2017-08-01 19:00~22:00 违约⾦ 45.0元
⼩计: 165.0元

场地:B
2017-08-02 13:00~17:00 200元
⼩计: 200.0元

场地:C
⼩计: 0.0元

场地:D
⼩计: 0.0元

---
总计: 365.0元

```




