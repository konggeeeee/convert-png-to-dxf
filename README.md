这是我第一次使用github，如有问题或照顾不及的地方还请多多谅解。

这是一个 Python 脚本，用于将 PNG 图片通过灰度化和矢量化的方式转换为填充的 DXF 文件。它使用 Potrace 工具进行矢量化。
可用于将电子签名图片等处理为cad签名
## 功能

* 将 PNG 图片转换为 DXF 格式。
* 支持灰度图像处理。
* 使用 Potrace 进行矢量化，并填充轮廓。
* 自动处理拖拽到脚本上的一个或多个 PNG 文件。
* 转换后的 DXF 文件保存在与原始 PNG 文件相同的目录下，文件名为 `convert.dxf`，如果已存在则自动添加数字编号。

## 依赖项

要运行此脚本，你需要安装以下依赖项：

* **Python 3**
* **Pillow (PIL)**: 用于图像处理。你可以使用 pip 安装：
    ```bash
    pip install Pillow
    ```
* **Potrace**: 一个将位图追踪为矢量图形的工具。**你需要自行安装 Potrace 并确保其可执行文件 (`potrace` 或 `potrace.exe`) 在你的系统 PATH 环境变量中。**

    * **Windows:** 你可以从 [Potrace 官方网站](http://potrace.sourceforge.net/) 下载预编译的二进制文件，在脚本同目录下新建\potrace文件夹并将二进制文件解压放置进该文件夹当中。


## 使用方法

1.  确保你已经安装了 Python 3、Pillow 和 Potrace，并且 Potrace 命令可以在你的终端或命令提示符中运行。
2.  将一个或多个 PNG 文件拖拽到脚本文件 (`.py` 文件) 的图标上。
3.  脚本将自动处理这些文件，并在每个 PNG 文件所在的目录下生成相应的 DXF 文件 (`convert.dxf` 或 `convert1.dxf` 等)。
4.  你可以在脚本执行完毕后按 Enter 键退出。

## 注意事项

* 生成的 DXF 文件可能需要在 CAD 软件（如 AutoCAD）或其他兼容的软件中查看和进一步处理。
* 脚本假设 Potrace 命令在系统 PATH 中可用。如果不可用，你需要修改脚本中的 `potrace_path` 变量来指定 Potrace 可执行文件的完整路径。**当前脚本尝试在与脚本相同的目录下的 `potrace` 文件夹中查找 `potrace.exe`。**
* 转换效果取决于原始 PNG 图片的质量和复杂度。

## 本脚本适用MIT协议发布
