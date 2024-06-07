class Path(object):
    @staticmethod
    def db_root_dir(dataset):
        if dataset == 'pascal':
            return r'C:\Users\admin\Desktop\demo\VOCdevkit\VOC2007'  # folder that contains VOCdevkit/.
        elif dataset == 'sbd':
            return r'C:\Users\admin\Desktop\demo\VOCdevkit\SBD'  # folder that contains dataset/.
        elif dataset == 'cityscapes':
            return 'D:/baidudownload/cityscapes/'     # foler that contains leftImg8bit/
        elif dataset == 'coco':
            return r'C:\Users\Admin\Desktop\coco'
        else:
            print('Dataset {} not available.'.format(dataset))
            raise NotImplementedError
