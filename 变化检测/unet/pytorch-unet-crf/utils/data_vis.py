import matplotlib.pyplot as plt


def plot_img_and_mask(img, mask):
    fig = plt.figure()
    a = fig.add_subplot(1, 2, 1)  # ���Ǵ�ӡ�����ͼƬ
    a.set_title('Input image')
    plt.imshow(img)

    b = fig.add_subplot(1, 2, 2)  # Ȼ���ӡԤ��õ��Ľ��ͼƬ
    b.set_title('Output mask')
    plt.imshow(mask)
    plt.show()
