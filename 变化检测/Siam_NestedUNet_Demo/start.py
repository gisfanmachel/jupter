import datetime
import os
from loguru import logger
from crop import segmentation
from del_file import delete_files
from merge import merge_image
from utils.parser import get_parser_with_args
from visualization import visualization

parser, metadata = get_parser_with_args()
opt = parser.parse_args()
container_log_dir = opt.container_log_dir
if not os.path.exists(container_log_dir):
    os.mkdir(container_log_dir)

# 路径设置,推荐绝对路径
img_before_path = opt.before  # # 变化前影像
img_after_path = opt.after  # 变化后影像
tif_save_path = opt.tif  # 变化检测结果tif文件
shp_save_path = opt.shp  # 变化检测结果shp文件
# 定义日志
log_file_path = os.path.join(container_log_dir,
                             "excute_bnu_change_detect_of_{}.log".format(
                                 datetime.datetime.now().strftime(
                                     '%Y%m%d%H%M%S')))
logger.add(log_file_path, format="{time} | {level} | {message}", level="INFO", rotation="500MB")

# 对TIF进行裁剪256*256
segmentation(img_before_path, img_after_path, logger)
# 网络输出
visualization(logger)
# 合并
merge_image(img_before_path, tif_save_path, shp_save_path, logger)
# 删除过程文件 delete:True/False 过程文件会对下一次变化检测产生影响，默认删除过程文件
delete_files(logger, True)

# 调用示例
# python start.py -b D:\Code\changedata\1.tif -a D:\Code\changedata\2.tif -t D:\Code\changedata\change.tif -s D:\Code\changedata\change.shp
