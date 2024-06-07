# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\spacetime\_models\dcrnn\base\base_data_loader.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 1970 bytes
import numpy as np
from torch.utils.data import DataLoader
from torch.utils.data.dataloader import default_collate
from torch.utils.data.sampler import SubsetRandomSampler

class BaseDataLoader(DataLoader):
    __doc__ = "\n    Base class for all data loaders\n    "

    def __init__(self, dataset, batch_size, shuffle, validation_split, num_workers, collate_fn=default_collate):
        self.validation_split = validation_split
        self.shuffle = shuffle
        self.batch_idx = 0
        self.n_samples = len(dataset)
        self.sampler, self.valid_sampler = self._split_sampler(self.validation_split)
        self.init_kwargs = {'dataset':dataset, 
         'batch_size':batch_size, 
         'shuffle':self.shuffle, 
         'collate_fn':collate_fn, 
         'num_workers':num_workers}
        (super().__init__)(sampler=self.sampler, **self.init_kwargs)

    def _split_sampler(self, split):
        if split == 0.0:
            return (None, None)
        else:
            idx_full = np.arange(self.n_samples)
            np.random.seed(0)
            np.random.shuffle(idx_full)
            if isinstance(split, int):
                assert split > 0
                assert split < self.n_samples, "validation set size is configured to be larger than entire dataset."
                len_valid = split
            else:
                len_valid = int(self.n_samples * split)
        valid_idx = idx_full[0[:len_valid]]
        train_idx = np.delete(idx_full, np.arange(0, len_valid))
        train_sampler = SubsetRandomSampler(train_idx)
        valid_sampler = SubsetRandomSampler(valid_idx)
        self.shuffle = False
        self.n_samples = len(train_idx)
        return (
         train_sampler, valid_sampler)

    def split_validation(self):
        if self.valid_sampler is None:
            return
        return DataLoader(sampler=self.valid_sampler, **self.init_kwargs)
