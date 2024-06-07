# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/_jsuperpy\analyst\am.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 16534 bytes
"""
地址匹配
"""
import os
from iobjectspy._jsuperpy._gateway import get_jvm
from iobjectspy._jsuperpy.data import DatasetVector, Point2D, GeoPoint
from iobjectspy._jsuperpy.data._util import get_input_dataset
from iobjectspy._jsuperpy._utils import split_input_list_from_str, oj, parse_bool, java_array_to_list
from iobjectspy._jsuperpy.data._jvm import JVMBase
from iobjectspy._logger import log_warning
__all__ = [
 "build_address_indices", "AddressItem", "AddressSearch"]

def get_default_dictionary_file():
    curr_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return curr_dir + "/address.dct"


def build_address_indices(output_directory, datasets, index_fields, save_fields=None, top_group_field=None, secondary_group_field=None, lowest_group_field=None, is_build_reverse_matching_indices=False, bin_distance=0.0, dictionary_file=None, is_append=False):
    """
    构建地址匹配的索引文件

    :param str output_directory: 索引文件结果输出目录
    :param datasets: 保存地址信息，用来创建索引的数据集
    :type datasets: list[DatasetVector] or tuple[DatasetVector]
    :param index_fields: 需要建立索引的字段，比如详细地址字段或地址名称等，该字段集合应该在每一个数据集中都存在
    :type index_fields: str or list[str] or tuple[str]
    :param save_fields: 需要存储的额外信息的字段，这些信息不用于地址匹配，但会在地址匹配结果中返回出来。
    :type save_fields: str or list[str] or tuple[str]
    :param str top_group_field: 一级分组的字段名称，比如各个省名称。
    :param str secondary_group_field: 二级分组的名称，比如各个市名称。
    :param str lowest_group_field: 三级分组的名称，比如各个县名称。
    :param bool is_build_reverse_matching_indices: 是否为逆向地址匹配创建索引
    :param float bin_distance: 逆向地址匹配索引创建的间隔距离。距离单位和坐标系保持一致。
    :param str dictionary_file: 字典文件地址，如果为空，则使用默认的字典文件。
    :param bool is_append: 是否在原索引上追加，如果指定的输出索引文件目录上已经有索引文件，如果为 True，则在原索引文件上追加，但要求
                           追加新的数据时要求新的属性表结构与已加载数据的属性表结构相同。如果为 False，则创建新的索引文件。
    :return: 是否创建索引成功
    :rtype: bool
    """
    if output_directory is None:
        raise ValueError("output directory is None")
    if not os.path.exists(output_directory):
        os.mkdir(output_directory)
        is_append = False
    else:
        address_gp = os.path.join(output_directory, "address.gp")
        if os.listdir(output_directory):
            if not os.path.exists(address_gp):
                log_warning('output directory "' + output_directory + '" have files, may be overwritten.')
                is_append = False
            elif not is_append:
                log_warning('output directory "' + output_directory + '" have address indices, may be overwritten. You can use is_append=True for append data to this indices')
            else:
                is_append = False
        else:
            datasets = isinstance(datasets, (list, tuple)) or [
             datasets]
        input_datasets = []
        for dt in datasets:
            dt = get_input_dataset(dt)
            if dt is not None:
                input_datasets.append(dt)

        if not input_datasets:
            raise ValueError("have no valid dataset")
        else:
            index_fields = split_input_list_from_str(index_fields)
            if not index_fields:
                raise ValueError("have no valid index field")
            dictionary_file = dictionary_file if dictionary_file else get_default_dictionary_file()
            java_setting = get_jvm().com.supermap.analyst.addressmatching.AddressLoadSetting()
            java_setting.setLoadDirectory(str(output_directory))
            java_setting.setDictionaryFile(str(dictionary_file))
            for dt in input_datasets:
                java_setting.addDataset(oj(dt))

            for field in index_fields:
                java_setting.addIndexField(str(field))

            if save_fields:
                for field in split_input_list_from_str(save_fields):
                    java_setting.addSaveField(field)

            if bin_distance:
                java_setting.setBINDistance(float(bin_distance))
            if is_build_reverse_matching_indices:
                java_setting.setLoadPoint(True)
            else:
                java_setting.setLoadPoint(False)
        if top_group_field:
            java_setting.setTopGroupField(str(top_group_field))
        if secondary_group_field:
            java_setting.setSecondaryGroupField(str(secondary_group_field))
        if lowest_group_field:
            java_setting.setLowestGroupField(str(lowest_group_field))
        address_load = get_jvm().com.supermap.analyst.addressmatching.AddressLoad()
        address_load.setSetting(java_setting)
        return address_load.load(parse_bool(is_append))


class _AddressSearchParameter:

    def __init__(self, is_address_segmented=False, is_location_return=True, max_result_count=10, top_group_name=None, secondary_group_name=None, lowest_group_name=None):
        self._is_address_segmented = False
        self._is_location_return = True
        self._max_result_count = 10
        self._top_group_name = None
        self._secondary_group_name = None
        self._lowest_group_name = None
        self.set_address_segmented(is_address_segmented).set_location_return(is_location_return).set_max_result_count(max_result_count).set_top_group_name(top_group_name).set_secondary_group_name(secondary_group_name).set_lowest_group_name(lowest_group_name)

    def set_address_segmented(self, value):
        self._is_address_segmented = parse_bool(value)
        return self

    @property
    def is_address_segmented(self):
        return self._is_address_segmented

    def set_location_return(self, value):
        self._is_location_return = parse_bool(value)
        return self

    @property
    def is_location_return(self):
        return self._is_location_return

    def set_max_result_count(self, value):
        if value:
            self._max_result_count = int(value)
        return self

    @property
    def max_result_count(self):
        return self._max_result_count

    def set_top_group_name(self, value):
        if value:
            self._top_group_name = str(value)
        return self

    @property
    def top_group_name(self):
        return self._top_group_name

    def set_secondary_group_name(self, value):
        if value:
            self._secondary_group_name = str(value)
        return self

    @property
    def secondary_group_name(self):
        return self._secondary_group_name

    def set_lowest_group_name(self, value):
        if value:
            self._lowest_group_name = str(value)
        return self

    @property
    def lowest_group_name(self):
        return self._lowest_group_name

    @property
    def _jobject(self):
        java_object = get_jvm().com.supermap.analyst.addressmatching.AddressSearchSetting()
        if self.is_address_segmented:
            java_object.setAddressSegmented(True)
        else:
            java_object.setAddressSegmented(False)
        if self.is_location_return:
            java_object.setLocationReturn(True)
        else:
            java_object.setLocationReturn(False)
        if self.max_result_count:
            java_object.setMaxResultCount(int(self.max_result_count))
        if self.lowest_group_name:
            java_object.setLowestGroupName(str(self.lowest_group_name))
        if self.secondary_group_name:
            java_object.setSecondaryGroupName(str(self.secondary_group_name))
        if self.top_group_name:
            java_object.setTopGroupName(str(self.top_group_name))
        return java_object


class AddressItem:
    __doc__ = "\n    中文地址模糊匹配结果类。中文地址模糊匹配结果类存储了与输入的中文地址相匹配的查询结果的详细信息，包括查询出来的地址，该地址所在的\n    数据集，该地址在源数据集中的 SmID，查询结果的评分值以及地址的地理位置信息。\n\n    "

    def __init__(self, java_object):
        self._address = java_object.getAddress()
        address_list = java_array_to_list(java_object.getAddresses())
        self._address_as_tuple = tuple(address_list) if address_list else None
        self._dataset_index = java_object.getDatasetIndex()
        self._record_id = java_object.getID()
        self._location = Point2D._from_java_object(java_object.getLocation())
        self._score = java_object.getScore()

    def __str__(self):
        return "{}  {}  {}".format(self.address, self.location, self.score)

    __repr__ = __str__

    @property
    def address(self):
        """str: 匹配出来的地址"""
        return self._address

    @property
    def address_as_tuple(self):
        """tuple[str]: 匹配出来的地址的数组形式"""
        return self._address_as_tuple

    @property
    def dataset_index(self):
        """int: 查询出来的中文地址所在的数据集的索引"""
        return self._dataset_index

    @property
    def record_id(self):
        """int: 查询出来的地址在源数据集中所对应的 SMID"""
        return self._record_id

    @property
    def location(self):
        """Point2D: 查询出来的地址所在的地理位置"""
        return self._location

    @property
    def score(self):
        """float: 匹配的评分结果"""
        return self._score


class AddressSearch(JVMBase):
    __doc__ = "\n    中文地址模糊匹配类。\n\n    中文地址模糊匹配的实现流程和注意事项：\n\n    1. 指定中文地址库数据创建的地址索引的目录，创建一个中文地址匹配对象；\n    2. 调用match对象，指定要搜索的地址所在城市，必须是中文地址数据库中市级字段中的值，再指定要搜索的中文地址和返回个数；\n    3. 系统对待匹配的关键字进行分词，然后去匹配指定数据集中指定字段中的内容，通过一定的运算，返回匹配的结果。\n    "

    def __init__(self, search_directory):
        """
        初始化对象

        :param str search_directory: 地址索引所在的目录
        """
        JVMBase.__init__(self)
        self._search_directory = None
        if search_directory:
            self.set_search_directory(search_directory)

    def set_search_directory(self, search_directory):
        """
        设置地址索引所在的目录。地址索引使用 :py:meth:`build_address_indices` 方法创建。

        :param str search_directory: 地址索引所在的目录
        :return: self
        :rtype: AddressSearch
        """
        if not search_directory:
            raise ValueError("search directory is None")
        if not os.path.exists(search_directory):
            raise ValueError("index directory is not existed")
        self._search_directory = search_directory
        java_setting = get_jvm().com.supermap.analyst.addressmatching.AddressSearchSetting()
        java_setting.setSearchDirectory(self.search_directory)
        self._jobject.setSetting(java_setting)
        return self

    def _make_java_object(self):
        return get_jvm().com.supermap.analyst.addressmatching.AddressSearch()

    @property
    def search_directory(self):
        """str: 地址索引所在的目录"""
        return self._search_directory

    def is_valid_lowest_group_name(self, value):
        """
        判断指定的名称作为三级分组名称是否合法。

        :param str value: 要判断的字段名称
        :return: 合法返回 True，否则返回 False
        :rtype: bool
        """
        if value:
            return self._jobject.isValidLowestGroupName(str(value))
        return False

    def is_valid_secondary_group_name(self, value):
        """
        判断指定的名称作为二级分组名称是否合法。

        :param str value: 要判断的字段名称
        :return: 合法返回 True，否则返回 False
        :rtype: bool
        """
        if value:
            return self._jobject.isValidSecondaryGroupName(str(value))
        return False

    def is_valid_top_group_name(self, value):
        """
        判断指定的名称作为一级分组名称是否合法。

        :param str value: 要判断的字段名称
        :return: 合法返回 True，否则返回 False
        :rtype: bool
        """
        if value:
            return self._jobject.isValidTopGroupName(str(value))
        return False

    def match(self, address, is_address_segmented=False, is_location_return=True, max_result_count=10, top_group_name=None, secondary_group_name=None, lowest_group_name=None):
        """
        地址匹配。该方法支持多线程。

        :param str address: 要检索的地名地址
        :param bool is_address_segmented: 传入的中文地址是否已经被分割，即用“*”分隔符进行了分词。
        :param bool is_location_return: 中文地址模糊匹配结果对象是否包含位置信息。
        :param int max_result_count: 中文地址模糊匹配的搜索的匹配结果的最大数目
        :param str top_group_name: 一级分组名称，前提是创建数据索引的时候设置了一级分组字段名称
        :param str secondary_group_name: 二级分组名称，前提是创建数据索引的时候设置了二级分组字段名称
        :param str lowest_group_name: 三级分组名称，前提是创建数据索引的时候设置了三级分组字段名称
        :return: 中文地址模糊匹配结果集合
        :rtype: list[AddressItem]
        """
        if not address:
            raise ValueError("invalid address")
        parameter = _AddressSearchParameter(is_address_segmented, is_location_return, max_result_count, top_group_name, secondary_group_name, lowest_group_name)
        address_result = self._jobject.match(str(address), oj(parameter))
        if address_result:
            address_items = AddressSearch._make_java_address_result(address_result)
            address_result.dispose()
            return address_items

    def reverse_match(self, geometry, distance, max_result_count=10):
        """
        逆向地址匹配。该方法支持多线程。

        :param geometry: 指定的点对象
        :type geometry: GeoPoint or Point2D
        :param float distance: 指定的搜索范围。
        :param int max_result_count: 搜索的匹配结果的最大数目
        :return: 中文地址匹配结果集合
        :rtype: list[AddressItem]
        """
        if not geometry:
            raise ValueError("invalid geometry")
        geometry = GeoPoint(geometry)
        if not geometry:
            raise ValueError("invalid geometry")
        if not distance or float(distance) < 0:
            raise ValueError("invalid distance")
        parameter = _AddressSearchParameter(max_result_count=max_result_count)
        address_result = self._jobject.match(oj(geometry), float(distance), oj(parameter))
        if address_result:
            address_items = AddressSearch._make_java_address_result(address_result)
            address_result.dispose()
            return address_items

    @staticmethod
    def _make_java_address_result(java_object):
        address_items = []
        if java_object:
            count = java_object.getCount()
            if count > 0:
                java_match_results = java_object.get(count, 0)
                result_count = java_match_results.getCount()
                for i in range(result_count):
                    java_match_result_item = java_match_results.get(i)
                    address_items.append(AddressItem(java_match_result_item))

                java_match_results.dispose()
        return address_items
