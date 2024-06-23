from pie.dataset.dataset import load_dataset

dataset_id='bc783faa-8975-4672-9e22-7b482f215dd6'
network_type=2
batch_size=1
invert_palette={(0, 0, 0): 0, (255, 0, 0): 1}
train_value_palette={0: 0, 1: 1}
class_name_list=['airplane']
image_size=[128,128]
# trans_pipelines=
a=load_dataset(dataset_id='bc783faa-8975-4672-9e22-7b482f215dd6',
             network_type=2,batch_size=1,
             invert_palette=invert_palette,
             class_name_list=class_name_list,
             # mosaic=mosaic,
             image_size=image_size)
anchors = a.save_pre_anchors('./' )
print(anchors)