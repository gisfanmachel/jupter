# SuperMap iObjects Python ( iObjectsPy ) 10.1.0 版本

## 1 简介

iObjectsPy 是 SuperMap iObjects Python 的简称。通过 iObjectsPy，用户可以直接使用 Python 语言操作 SuperMap 各种空间数据，

同时，iObjectsPy 也提供空间数据导入导出、投影转换、矢量拓扑分析、栅格分析等功能，帮助用户使用脚本进行空间数据快速处理和分析。

## 2 支持环境
[Python](https://www.python.org/) 3.5+

[SuperMap iObjects Java](http://support.supermap.com.cn/DownloadCenter/ProductPlatform.aspx) 10.1.0

## 3 支持特性
* 支持数据管理和组织，包括工作空间、数据源、数据集、记录集等
* 支持二维点、线、面、文本、三维点等几何对象和要素对象的创建和管理
* 支持投影转换和设置
* 支持常用数据格式导入和导出操作，包括 shp、mif、cad等矢量数据，tif、img、png等栅格和影像数据
* 支持缓冲区分析、叠加分析、融合、密度聚类、矢量数据重采样、矢量数据光滑、创建泰森多边形、统计点、矢量裁剪、拓扑检查等矢量数据处理和分析
* 支持栅格重采样、重分级、栅格数据聚合、重分级、插值分析、密度分析、矢栅转换、距离栅格、表面栅格、坡度坡向分析、代数运算等栅格数据处理和分析

## 4 使用说明

## 4.1 产品包结构

### 4.1.1 iobjectspy 目录

库文件所在目录

### 4.1.2 examples 目录

范例程序源码，供用户了解熟悉接口使用方式：

密度聚类范例：`example_aggregate_points.py`

栅格裁剪范例：`example_clip_raster.py`

密度分析范例：`example_density_analyst.py`

数据导出范例：`example_export_data.py`

数据导入范例：`example_import_data.py`

NumPy数据交互范例：`example_numpy_array.py`

叠加分析范例：`example_overlay_analyst.py`

数据查询范例：`example_query_data.py`

### 4.1.3 data 目录

范例数据，供范例程序使用：

`example_data.udb`：供范例程序共用的UDB数据源

`County_p.shp`：供数据导入使用的矢量数据文件

`multibands.img`：供数据导入使用的影像数据文件

`dem.npy`：供NumPy数据交互使用的NumPy文件

### 4.1.4 doc 目录

Python接口说明，供开发人员查阅.

## 4.2.环境设置

(1) 安装 [Python 3.5.0](https://www.python.org/download) 或以上版本

(2) 执行安装包内的 setup.py 脚本，命令为： python setup.py install

(3) 如需使用AI相关功能，还需要配置机器学习资源包（Machine Learning Resources），并通过 pip（pip版本不低于10.0.0）或 conda 在线安装相关依赖：

- 在官网下载 SuperMap iObjects Python Machine Learning Resources 10i 机器学习资源包，解压到iobjectspy根目录即可。资源包内包含示例模型、示例程序、示例文件、训练配置文件及训练所需的主干网络模型等。

- pip 环境配置：使用`python -m pip install -r requirement.txt`在线安装相关依赖。用`python -m pip freeze > requirement.txt`导出当前模块依赖。各requirement文件分别对应：

    -  `requirement.txt`:     如需使用CPU进行机器学习（默认）
    -  `requirement_gpu.txt`: 如需使用GPU进行机器学习（性能更优）

- conda 环境配置：使用`conda env create -f requirements-conda-cpu.yml`建立iobjectspy虚拟环境。
    
    - `requirements-conda-cpu.yml`: 如需使用CPU进行机器学习（默认）
    - `requirements-conda-gpu.yml`: 如需使用GPU进行机器学习（性能更优）

(4) 安装 Java 8 或以上版本

(5) 安装 SuperMap iObjects Java 组件，注意使用与产品包相对应的组件版本，依赖的最低版本为 10.1.0.18027.76100。

- Windows 用户，可以通过以下方式配置 SuperMap iObjects Python 使用的 SuperMap iObjects Java 组件:
  1. 将 SuperMap iObjects Java 组件的 Bin 目录设置到 Path 变量

  2. 在安装完 SuperMap iObjects Python 后，在 cmd 命令行中执行 "`iobjectspy set-iobjects-java E:\SuperMap\iObjects\Bin_x64`"，通过这种方式，必须确保 Python 的 Scripts 目录在 PATH 环境中，或者直接在 Scripts 目录下执行。

  3. 启动 python 窗口，执行以下代码:

    ```python
    import iobjectspy
    iobjectspy.set_iobjects_java_path(r'E:\SuperMap\iObjects\Bin_x64')
    ```

  需要注意的是，通过方式 2 和 3 配置 SuperMap iObjects Java 组件，会将指定的 SuperMap iObjects Java 组件目录配置到 iobjectspy 库目录下的 evn.json 文件中，这样，用户无需多次设置，但在升级 SuperMap iObjects Java 组件版本时，需要再次通过 2 或 3 执行。

- Linux 用户，可以通过以下方式配置 SuperMap iObjects Python 使用的 SuperMap iObjects Java 组件:

  1. 将 SuperMap iObjects Java 组件的 Bin 直接设置到 `/opt/SuperMap/iobjects/1010/Bin`

  2. 将 SuperMap iObjects Java 组件的 Bin 设置在环境变量中

    - export LD_LIBRARY_PATH=/home/user/iobjects-java/bin:$LD_LIBRARY_PATH

  3. 在安装完 SuperMap iObjects Python 后，在 cmd 命令行中执行 `iobjectspy set-iobjects-java /home/user/iobjects-java/bin`

  4. 启动 python 窗口，执行以下代码::

    ```python
    import iobjectspy
    iobjectspy.set_iobjects_java_path('/home/user/iobjects-java/bin')
    ```
  需要注意的是，通过方式 3 和 4 配置 SuperMap iObjects Java 组件，会将指定的 SuperMap iObjects Java 组件目录配置到 iobjectspy 库目录下的 evn.json 文件中，这样，用户无需多次设置，但在升级 SuperMap iObjects Java 组件版本时，需要再次通过 3 或 4 执行。所以需要确保当前操作对 iobjectspy 安装目录有写入权限（可以通过使用 root 用户权限执行命令）。

    
## 4.3 在线帮助

在线帮助文档，请参考[http://iobjectspy.supermap.io](http://iobjectspy.supermap.io)


## 5 版本历史

	9.1.0 - 2018-09
	9.1.1 - 2018-12
	9.1.2 - 2019-05
	10.0.0 - 2019-10
	10.0.1 - 2019-12