# apeng-kicad
apeng's kicad library

### 组成
1. 在官网库 [kicad-library](https://github.com/KiCad/kicad-library/) 中挑选自己常用的footprint组成。
2. footprint对应的3D模型挑选自[kicad-3d-mcad-models](https://github.com/easyw/kicad-3d-mcad-models), 采用他的 [kicad StepUp](https://sourceforge.net/projects/kicadstepup/) 方法生成电路板的3D模型。

### 使用方法（win7）
1. 删除原来的环境变量 **KISYSMOD** **KISYS3DMOD**
2. 修改 `C:\Users\用户名\AppData\Roaming\kicad\kicad_common` 文件中环境变量为库所在地址。例如：
 - KISYS3DMOD=C:\\\PROJECTS\\\apeng-kicad\\\packages3d\\\
 - KISYSMOD=C:\\\PROJECTS\\\apeng-kicad\\\footprints\\\
3. 修改StepUp配置文件 `ksu-config.ini`：
 - prefix3d_1 = C:\PROJECTS\apeng-kicad\packages3d\ 
4. 拷贝fp-lib-table文件到目录 `C:\Users\用户名\AppData\Roaming\kicad\` 或者建议采用创建链接mklink方式。
 