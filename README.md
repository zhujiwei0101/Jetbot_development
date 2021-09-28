# Jetbot_development
## 远程连接

```bash
ssh -X {username}@{host}
```
访问 http://{host}:8888 使用jupyter notebook lab 开发
username:jetbot
password:jetbot
### 远程使用图形界面
https://blog.csdn.net/weixin_42232749/article/details/81624156?utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromMachineLearnPai2%7Edefault-1.control&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromMachineLearnPai2%7Edefault-1.control

之后每次调用
客户端
```bash
xhost + {host}
```
服务器端
```bash
export DISPLAY=localhost:10.0
```
性能监控
```bash
sudo jtop
```
## 舵机控制
```python3
import time 
import jetbot
robot =jetbot.robot.Robot()
#舵机1
for i in range(60,240,30):
    basevalue=4096*((i*11)+500)/20000
    print(basevalue/4096*100)
    Lable = 1
    robot.pwm.set_pwm(1,0,int(basevalue)) 
    time.sleep(1)
#舵机0
basevalue=4096*((90*11)+500)/20000
print(basevalue)
for i in range(162,188,4):
    basevalue = i
    print(basevalue)
    robot.pwm.set_pwm(0,0,int(basevalue))
    time.sleep(1)
```

行程大概60-210度,125度为中间位置 (目前角度的对应性还不知)
## 相机
### imx219相机 csi接口
```bash
#查看摄像头数量和规格，使用v4l2-utils工具
sudo apt install v4l-utils 
v4l2-ctl --list-devices
```
#### 相机使用
```python3
import cv2
from jetbot import Camera
from jetbot import bgr8_to_jpeg
import traitlets
import ipywidgets.widgets as widgets
from IPython.display import display

cam= Camera.instance()

face_image = widgets.Image(format='jpeg', width=640, height=480)
face_image1 = widgets.Image(format='jpeg', width=320, height=240)
display(face_image)
display(face_image1)

while True:
    frame = cam.value
    face_image.value = bgr8_to_jpeg(frame)
    face_image1.value = bgr8_to_jpeg(frame)

```
### realsense
https://github.com/jetsonhacks/installRealSenseSDK 下载
在installLibrealsense.sh 文件相应地方替换
```bash
sudo apt-key adv --keyserver keys.gnupg.net --recv-key F6E65AC044F831AC80A06380C8B3A55A6F3EFCDE || sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-key F6E65AC044F831AC80A06380C8B3A55A6F3EFCDE
sudo add-apt-repository "deb https://librealsense.intel.com/Debian/apt-repo bionic main" -u
```
在buildLibrealsense.sh文件中修改版本号以及
 将93行改为（指定生成python3的动态库）
 ```bash
/usr/bin/cmake ../ -DBUILD_EXAMPLES=true -DFORCE_LIBUVC=true -DBUILD_WITH_CUDA="$USE_CUDA" -DCMAKE_BUILD_TYPE=release -DBUILD_PYTHON_BINDINGS=bool:true -DPYTHON_EXECUTABLE=/usr/bin/python3
 ```
```bash
ls
cd installRealSenseSDK/
 ./installLibrealsense.sh 
 ./buildLibrealsense.sh 
```
安装完成后添加环境变量 
```bash
vim ~/.bashrc

export PYTHONPATH=$PYTHONPATH:/usr/local/lib:/usr/local/lib/python3.6/pyrealsense2

source ~/.bashrc
```
参考
[1]https://github.com/jetsonhacks/installRealSenseSDK
[2]https://dev.intelrealsense.com/docs/nvidia-jetson-tx2-installation 
[3]https://www.huaweicloud.com/articles/0ba49cd30493adbb37c82250408d8be4.html
[4] https://blog.csdn.net/weixin_41010198/article/details/113618002
[5]https://blog.csdn.net/weixin_41010198/article/details/113997798?utm_medium=distribute.pc_relevant.none-task-blog-2~default~baidujs_title~default-0.control&spm=1001.2101.3001.4242
[6]https://github.com/JetsonHacksNano/installLibrealsense
[7]https://www.jetsonhacks.com/2019/12/22/install-realsense-camera-in-5-minutes-jetson-nano/
[8]https://blog.csdn.net/weixin_43719386/article/details/102647424?utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromMachineLearnPai2%7Edefault-3.control&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromMachineLearnPai2%7Edefault-3.control
## 运动控制
```python3
import time 
import jetbot
robot =jetbot.robot.Robot()


robot.forward(speed =  0.3)#30%的速度
robot.backward(speed =  0.3)
robot.right(speed  =  0.3)
robot.left(speed  =  0.3)
robot.stop()


robot.left(0.3)
time.sleep(0.5)
robot.stop()


电机单独控制
robot.set_motors(0.3, 0.6)
time.sleep(1.0)
robot.stop()



robot.left_motor.value  =  0.3
robot.right_motor.value  =  0.6
time.sleep(1.0)
robot.left_motor.value  =  0.0
robot.right_motor.value  =  0.0
```

```bash
sudo apt-get install python3-pil python3-pil.imagetk
```
