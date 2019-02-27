

## 跑一个MSK-RCNN demo
参考 https://blog.csdn.net/ghw15221836342/article/details/80084984
> github地址`https://github.com/matterport/Mask_RCNN`
> 实例分割框架，通过训练，可以从图片中分割出人物。
> github上第一demo.ipynb就是一个人物分割的例子。
### 软件安装
> https://blog.csdn.net/u012513525/article/details/54947398

- 安装Anaconda（可选）
- 安装pycharm
- pycharm中配置Anacoda（可选）

### 克隆Mask_RCNN工程
`git clone https://github.com/matterport/Mask_RCNN.git`

sample目录下有demo.ipynb，ipynb需要用ipython notebook打开，我比较习惯用pycharm，所以用命令`jupyter nbconvert --to script demo.ipynb`将ipynb转为py
### 跑demo.ipynb
- pycharm中用conda创建一个工程
- 将之前转出来的demo.py粘到工程中。
- 安装远程依赖库
    - 会有许多报错，是因为demo需要依赖许多三方库。快捷键类似导包那样可以自动下载。
    - 下载失败可能是因为源的问题，在setting->project interpreter中把use conda package manager取消勾选，或者添加repositories
- 拷贝本地依赖
    - 根据报错信息，从Mask_RCNN工程中找到对应需要的py文件拷贝到工程中
- 下载MS COCO API
    - `https://github.com/waleedka/coco`
    - 根据本地依赖coco.py中的注释，下载MS COCO API。在python目录下执行make命令。将生成的pycocotools目录拷贝到工程中
- 拷贝Mask RCNN代码
    - 根据本地依赖coco.py的注释，把MaskRCNN的代码拷进来
- 删除demo.py的get_ipython那行（好像是notebook中用的，删了试了下没影响）
- 不断重试运行，修改各种demo.py中文件目录导致的错误以及依赖库所依赖的库的安装
- mrcnn/utils中有下载训练好数据的链接
- 修改一下图片读取路径
- demo最后一行代码使用matplotlib的api给图像上面绘制遮罩，可以通过测试控制只显示边框




## 智能弹幕

修改demo代码，在项目py目录的demoForData中，可以将一张图片解析出人的轮廓数据，把json数据放在安卓assets中
