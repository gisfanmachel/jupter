'''
This file is used to save the output image
'''

import torch.utils.data
from utils.parser import get_parser_with_args
from utils.helpers import get_test_loaders, initialize_metrics
import os
from tqdm import tqdm
import cv2


def visualization(logger):
    output_img_path='./output_img'
    if not os.path.exists(output_img_path):
        os.mkdir(output_img_path)

    parser, metadata = get_parser_with_args()
    opt = parser.parse_args()

    dev = torch.device(opt.gpu_device if torch.cuda.is_available() else 'cpu')

    test_loader = get_test_loaders(opt, batch_size=1)

    path = opt.checkpoint_path  #  mothe path of thedel
    model = torch.load(path)

    model.eval()
    index_img = 0
    test_metrics = initialize_metrics()
    with torch.no_grad():
        tbar = tqdm(test_loader)
        for batch_img1, batch_img2, name in tbar:
            batch_img1 = batch_img1.float().to(dev)
            batch_img2 = batch_img2.float().to(dev)

            cd_preds = model(batch_img1, batch_img2)

            cd_preds = cd_preds[-1]
            _, cd_preds = torch.max(cd_preds, 1)
            cd_preds = cd_preds.data.cpu().numpy()
            cd_preds = cd_preds.squeeze() * 255

            file_path = output_img_path+"/" + name[0]
            cv2.imwrite(file_path, cd_preds)

            index_img += 1

    logger.info('网络输出完成')
