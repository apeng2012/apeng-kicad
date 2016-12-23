# 将kicad输出的greber文件打包

预先安装7zip并将其7z加入本文所在目录加入PATH。
kicad 绘图输出中勾选“使用Protel文件扩展名”
在本文目录下新建"plotzip.bat"文件。其内容：
python 具体路径\plotzip\plotzip.py

使用时：打开工程目录下plot_files文件夹。先按住Shift键，然后鼠标右键，选择打开CMD命令窗口。输入plotzip
