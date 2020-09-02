# 钓鱼星球脚本

[English version](documents/English_readme.md)

该项目是一个基于python3的钓鱼星球脚本，意在跳过繁琐的升级过程，尽快升到高级别以解锁渔具，从而获得更好的游戏体验。
仅推荐有python程序基础的玩家使用该项目。

## 依赖的包:
```
PIL
pywin32
opencv-python
numpy
pysimplegui
```

## 程序功能
程序目前仅提供在Alberta秒提狗鱼/大西洋鲑鱼的功能。

程序正在Michigan渔场进行测试。


## 如何运行：
进入游戏，将游戏分辨率设置为```1280×720```，关闭全屏幕模式，将指示器调至三列版本，到达指定位置，如有可能请将特效调节至最低。

使用git clone将程序clone到任意位置，进入游戏后调整自身所在位置，并将鱼竿调整至抛投模式后，使用已经安装好包的python环境调用```main.py```即可。

使用时请务必保证游戏界面在屏幕范围内，请关闭所有可能的弹窗软件，脚本使用期间不能锁屏，且焦点必须一直在游戏中。

## 程序测试

程序在Alberta指定位置测试连续钓鱼4小时无异常。测试时使用的渔具如下：

![Equipment in Alberta](image/readme/equipment_in_alberta.png "Equipment")

测试时使用的位置如下：

![Position in Alberta](image/readme/position_in_alberta.png "Position")

程序正在Michigan进行测试。测试使用的渔具为：

![Equipment in Alberta](image/readme/equipment_in_michigan.png "Equipment")

测试使用的位置如下：

![Position in Alberta](image/readme/position_in_michigan.png "Position")

## 程序日志

程序日志保留在```log```文件夹中，若项目中无此文件夹，请手动创建。