import matplotlib.pyplot as plt


def plot_img_and_mask(img, mask):
    fig = plt.figure()
    a = fig.add_subplot(1, 2, 1)  # 先是打印输入的图片
    a.set_title('Input image')
    plt.imshow(img)

    b = fig.add_subplot(1, 2, 2)  # 然后打印预测得到的结果图片
    b.set_title('Output mask')
    plt.imshow(mask)
    plt.show()
