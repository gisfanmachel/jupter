import os


# -------------------------删除过程文件------------------------

# 删除文件
def del_file(path):
    ls = os.listdir(path)
    for i in ls:
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):
            del_file(c_path)
        else:
            os.remove(c_path)


def delete_files(logger, delete):
    # 变化前分割影像路径
    seg_a_path = './Data/test/A'
    # 变化后分割影像路径
    seg_b_path = './Data/test/B'
    # 网络输出
    out_path = './output_img'

    if delete:
        del_file(seg_a_path)
        del_file(seg_b_path)
        del_file(out_path)
        logger.info("过程文件已删除")
