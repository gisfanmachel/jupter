# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\geoparsing\_ger.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 19385 bytes
import os, re, yaml
from iobjectspy import Datasource, recordset_to_df
from iobjectspy.ml.toolkit import _toolkit
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

class GER(object):
    __doc__ = "地理实体识别类，包括地理实体识别所需要的模型训练、标签制作、模型预测等功能。\n    目前支持的后台模块框架为CRF++0.58\n    "

    def __init__(self, config_file=None):
        try:
            import CRFPP
            self.CRFPP = CRFPP
        except Exception as e:
            try:
                print("RuntimeError:", e)
            finally:
                e = None
                del e

        if config_file is None:
            print("Geograhpic Entity Recognization Model Object Created....")
            self.config_file = os.path.join(os.getcwd(), "config.yml")
        else:
            print("{0} is Set....".format(config_file))
            self.config_file = config_file
        try:
            self.load_config()
        except Exception as e:
            try:
                print("RuntimeError: ", e)
            finally:
                e = None
                del e

    class config_meta(object):
        __doc__ = "地理实体识别GER类的子类，负责管理GER中配置元信息\n        包括GER所用后台模块框架参数，标签系统定义等设定\n        "

        def __init__(self, config_file):
            if os.path.isfile(config_file):
                with open(config_file, "r") as stream:
                    try:
                        cc = yaml.load(stream)
                        self.framework = cc["framework"]
                        self.tags_classes = dict([x.split(":") for x in cc["tags"]["classes"]])
                        self.prefix = cc["tags"]["prefix"]
                        self.ommiting = cc["tags"]["ommiting"]
                        self.prob_threshold = cc["tags"]["prob_threshold"]
                    except yaml.YAMLError as exc:
                        try:
                            print(exc)
                        finally:
                            exc = None
                            del exc

            else:
                self.tags_classes = {'province':"1", 
                 'city':"2",  'district':"3"}
                self.prefix = ["B", "I", "E", "S"]
                self.ommiting = "O"
                self.prob_threshold = 0.1
                self.framework = "crfpp"

        def __str__(self):
            rep = "Meta Info of Geograhpic Entity Recognization Model :\n"
            rep += "framework: " + str(self.framework) + "\n"
            rep += "tags_classes:{0}\n".format(str(self.tags_classes))
            rep += "prefix: " + str(self.prefix) + "\n"
            rep += "ommiting: " + str(self.ommiting) + "\n"
            rep += "prob_threshold: " + str(self.prob_threshold) + "\n"
            return rep

        def __repr__(self):
            rep = "Meta Info of Geograhpic Entity Recognization Model :\n"
            rep += "framework: " + str(self.framework) + "\n"
            rep += "tags_classes:{0}\n".format(str(self.tags_classes))
            rep += "prefix: " + str(self.prefix) + "\n"
            rep += "ommiting: " + str(self.ommiting) + "\n"
            rep += "prob_threshold: " + str(self.prob_threshold) + "\n"
            return rep

        def write_training_data(self, outfile=None, method='a', tags_new=None, addr_input=None, encoding='utf-8'):
            """
            生成训练数据

            :param str outfile: 生成的训练数据文件路径
            :param str method: 打开训练数据文件的模式，默认为a，追加模式，为w时为覆盖模式
            :param list[str] tags_new: 对应地址文本的标签和起始终止位置，由make_tag生成
            :param str addr_input: 待解析的地址文本
            :param str endcoding: 训练数据文件的字符编码，默认为utf-8
            :return: 生成的训练数据文件路径位置
            :rtype: str
            """
            import codecs
            addr_input = _toolkit.merge_number(addr_input)
            with codecs.open(outfile, method, encoding) as outf:
                for i in range(0, len(tags_new)):
                    tag_cur = tags_new[i]
                    for ix in range(0, len(self.prefix)):
                        if tags_new[i].startswith(self.prefix[ix]):
                            tag_cur = tags_new[i][2[:None]]

                    outf.write("{0} {1} {2}\n".format(addr_input[i], tag_cur, tags_new[i]))

                outf.write("\n")
            return outfile

        def make_template(self, outf=None):
            """
            建立特征模板

            :param str outf: 建立特征模板文件的位置
            :return: 特征模板文件的路径
            :rtype: str
            """
            import tempfile, os
            if outf is None:
                outf = os.path.join(tempfile.mkdtemp(), "template")
            with open(outf, "w") as temp:
                temp.write("\n# Unigram\nU00:%x[-4,0]\nU01:%x[-3,0]\nU02:%x[-2,0]\nU03:%x[-1,0]\nU04:%x[0,0]\nU05:%x[1,0]\nU06:%x[2,0]\nU07:%x[3,0]\nU08:%x[4,0]\nU09:%x[-4,0]/%x[-3,0]/%x[-2,0]/%x[-1,0]/%x[0,0]/%x[1,0]/%x[2,0]/%x[3,0]\nU10:%x[-4,0]/%x[-3,0]/%x[-2,0]/%x[-1,0]/%x[0,0]/%x[1,0]/%x[2,0]\nU11:%x[-4,0]/%x[-3,0]/%x[-2,0]/%x[-1,0]/%x[0,0]/%x[1,0]\nU12:%x[-3,0]/%x[-2,0]/%x[-1,0]/%x[0,0]/%x[1,0]/%x[2,0]\nU13:%x[-3,0]/%x[-2,0]/%x[-1,0]/%x[0,0]/%x[1,0]\nU14:%x[-3,0]/%x[-2,0]/%x[-1,0]/%x[0,0]\nU15:%x[-2,0]/%x[-1,0]/%x[0,0]/%x[1,0]\nU16:%x[-2,0]/%x[-1,0]/%x[0,0]\nU17:%x[-2,0]/%x[-1,0]/%x[0,0]/%x[1,0]/%x[2,0]\nU18:%x[-1,0]/%x[0,0]/%x[1,0]\nU19:%x[0,0]/%x[1,0]/%x[2,0]\nU20:%x[-1,0]/%x[0,0]\nU21:%x[0,0]/%x[1,0]\n\n\n# Bigram\nB\n")
            print("Template created in the {0}".format(outf))
            return outf

        def make_tag(self, addr_word='北京市朝阳区', tags_input=None):
            """
            制作标签

            :param str addr_word: 被解析的地址文本
            :param tags_input: 地址文本对应的解析标注，格式为标注类型-起始序号-结束序号,并用英文-分割
            :type tags_input: str or NoneType
            :return: 解析后的标签list
            :rtype: list[str]
            """
            addr_input = _toolkit.merge_number(addr_word)
            print("请标注", addr_input)
            print("候选标注：", list(self.tags_classes.keys()))
            print("候选前缀：", self.prefix)
            for i in range(0, len(addr_input)):
                print("{0:2d}  {1:5s}".format(i, addr_input[i]))

            print("请输入:标注类型-起始序号-结束序号,并用英文-分割\n")
            print("例如：city-0-2-district-3-5\n")
            if tags_input is None:
                test = input(":")
            else:
                test = tags_input
            test = test.strip().split("-")
            print(test)
            tag = []
            begin = []
            end = []
            i = 0
            tags_new = [self.ommiting for x in range(0, len(addr_input))]
            while i < len(test):
                print(i)
                tag_cur = str(test[i])
                begin_cur = int(test[i + 1])
                end_cur = int(test[i + 2])
                tag.append(tag_cur)
                begin.append(begin_cur)
                end.append(end_cur)
                if begin_cur != end_cur:
                    tags_new[begin_cur] = self.prefix[0] + "_" + tag_cur
                    tags_new[end_cur] = self.prefix[2] + "_" + tag_cur
                    print(begin_cur, tags_new[begin_cur])
                    for ii in range(begin_cur + 1, end_cur):
                        tags_new[ii] = self.prefix[1] + "_" + tag_cur

                else:
                    tags_new[begin_cur] = self.prefix[3] + "_" + tag_cur
                i += 3

            print(tag, begin, end)
            return tags_new

    def train(self, template=None, data=None, model_path=None):
        """
        训练模型函数

        :param str template: 特征模板文件路径
        :param str data: 训练数据文件路径
        :param str model_path: 模型文件路径

        """
        if template is None or data is None or model_path is None:
            print("Pls provide all paramters!!")
        import subprocess
        subprocess.call(("crf_learn {0} {1} {2}".format(template, data, model_path)),
          shell=True)

    def gen_word_class(self, words, tags):
        """根据给定的字和标签，生成对应的实体类别.
        函数根据BIES等标签系统将独立的字进行合并，并将标签中的类别后缀信息提取出对应于该实体。

        :param words: 输入的字
        :param tags: 对应的标签
        :return: 返回地址实体和对应类别
        """
        prefix = self.config.prefix
        prefix_b = prefix[0]
        prefix_i = prefix[1]
        prefix_e = prefix[2]
        prefix_s = prefix[3]
        ommiting = self.config.ommiting
        ss = words
        tags_class = [re.compile("^._").sub("", tags[i]) for i in range(0, len(tags))]
        tags_uniclass = list(set(tags_class))
        tags_uniclass.sort(key=(tags_class.index))
        if _toolkit.find_element_in_list(ommiting, tags_uniclass):
            print("O-tags found")
            o_inx = [i for i in range(len(tags_class)) if tags_class[i] == ommiting]
            tags_class = [i for j, i in enumerate(tags_class) if j not in o_inx]
            ss = [i for j, i in enumerate(ss) if j not in o_inx]
            tags = [i for j, i in enumerate(tags) if j not in o_inx]
        if tags[0].startswith(prefix_i + "_") or tags[0].startswith(prefix_e + "_"):
            tags[0] = prefix_b + "_" + tags[0][1[:None]]
            print("incompleted tags merged")
        for i in range(1, len(tags)):
            if not (tags[i - 1].startswith(prefix_e + "_") or tags[i - 1].startswith(prefix_s + "_")):
                if tags[i - 1] == ommiting:
                    pass
                if tags[i].startswith(prefix_i + "_") or tags[i].startswith(prefix_e + "_"):
                    pass
                tags[i] = prefix_b + "_" + tags[i][1[:None]]
                print("incompleted tags merged")

        tags_b = [tags[i].startswith(prefix_b + "_") for i in range(0, len(tags))]
        tags_e = [tags[i].startswith(prefix_e + "_") for i in range(0, len(tags))]
        tags_s = [tags[i].startswith(prefix_s + "_") for i in range(0, len(tags))]
        addr_com = [""] * (sum([x for x in tags_b]) + sum([x for x in tags_s]))
        class_com = [""] * (sum([x for x in tags_b]) + sum([x for x in tags_s]))
        i = 0
        jj = 0
        while i < len(ss):
            class_cur = tags_class[i]
            j = i + 1
            while j < len(tags) and not tags_e[j] is True:
                if tags_s[j] is True:
                    break
                j += 1

            addr_com[jj] = "".join(ss[i[:j + 1]])
            class_com[jj] = class_cur
            i = j + 1
            jj += 1

        return (
         addr_com, class_com)

    def load_config(self):
        """读取配置信息，配置信息的路径由成员变量config_file提供"""
        self.config = self.config_meta(self.config_file)

    def parse_batch(self, in_data=None, addr_field=0, model_path='./model', out_name='result', out_data='/tmp/result.csv'):
        """
        批量解析函数

        :param in_data: 输入数据，默认第一列为多条待解析的地址文本
        :type in_data: str or DatasetVector
        :param addr_field: 待匹配的地址字段；参数为字符串类型时，表示字段名；参数为整数时，表示in_data中的第几列是待解析数据，默认为0，表示第一列
        :param str model_path: 模型文件路径
        :param str out_name: 输出数据集名称，默认为result，仅在输出到Datasource时起效
        :param out_data: 输出数据，可以是csv的路径，数据源的名称或路径
        :type out_data: str or Datasource
        """
        if not _toolkit.checkpath(model_path):
            print("Please provide a valid path of model file")
            return ()
        try:
            import iobjectspy._jsuperpy
        except Exception as e:
            try:
                print("Warning: ", e)
            finally:
                e = None
                del e

        import pandas as pd
        if _toolkit.checkpath(in_data, "csv"):
            df = pd.read_csv(in_data, low_memory=False)
            testaddr = df.ix[(None[:None], addr_field)]
        else:
            if _toolkit.check_module(modulename="iobjectspy._jsuperpy"):
                if isinstance(in_data, iobjectspy._jsuperpy.data.DatasetVector):
                    if isinstance(addr_field, int):
                        addr_field = in_data.get_field_info(addr_field).name
                    df = recordset_to_df(recordset=in_data.get_recordset(fields=addr_field), skip_null_value=False)
                    testaddr = df.ix[(None[:None], addr_field)]
        if testaddr is None:
            print("Please check input parameter of in_data ")
            return -1
        res = [self.parse((str(d)), model_path=model_path) for d in testaddr]
        res = pd.DataFrame.from_dict(res)
        if isinstance(out_data, str) and out_data.endswith("csv"):
            res.to_csv(out_data, index=False)
        else:
            if _toolkit.check_module(modulename="iobjectspy._jsuperpy"):
                if isinstance(out_data, (str, iobjectspy._jsuperpy.data.Datasource)):
                    from iobjectspy._jsuperpy.conversion import import_csv
                    from tempfile import gettempdir
                    tempoutf = os.path.join(gettempdir(), "temp.csv")
                    print(tempoutf)
                    res.to_csv(tempoutf, index=False)
                    import_csv(tempoutf, out_data, out_dataset_name=out_name)
            print("Done !")

    def parse(self, inputstr, model_path='./model', extra_option=' -v 3 -n2'):
        """
        地址文本解析函数（单条）

        :param str inputstr: 待解析的地址文本
        :param str model_path: 模型文件路径
        :param str extra_option: 模型解析附近选项，默认为-v 3 -n2，可参考CRF++手册
        :return: 解析出的各部分地理要素和各标签类别
        :rtype: dict
        """
        if not _toolkit.checkpath(model_path):
            print("Please provide a valid path of model file")
            return ()
        content_words = _toolkit.merge_number(inputstr.replace(" ", "").replace("\n", ""))
        tags = list()
        try:
            tagger = self.CRFPP.Tagger("-m " + model_path + extra_option)
            tagger.clear()
            for word in content_words:
                word = word.strip()
                if word:
                    tagger.add(word)

            tagger.parse()
            size = tagger.size()
            xsize = tagger.xsize()
            for i in range(0, size):
                for j in range(0, xsize):
                    tag = tagger.y2(i)
                    tags.append(tag)

        except Exception as e:
            try:
                print("RuntimeError: ", e)
            finally:
                e = None
                del e

        try:
            ss_gen = [
             "", ""]
            ss_gen = self.gen_word_class(content_words, tags)
        except Exception as e:
            try:
                print("RuntimeError: ", e)
                print(content_words, tags)
            finally:
                e = None
                del e

        dict_table = dict()
        keys = [tagger.yname(i).replace("B_", "").replace("I_", "").replace("E_", "").replace("S_", "") for i in range(0, tagger.ysize()) if tagger.yname(i) != "O"]
        keys = list(set(keys))
        keys.append("prob")
        keys.append("addr_raw")
        try:
            for i in range(len(keys)):
                if i == len(keys) - 1:
                    dict_table[keys[i]] = "".join(content_words).strip()
                elif i == len(keys) - 2:
                    dict_table[keys[i]] = tagger.prob()
                else:
                    dict_table[keys[i]] = re.sub("\\W+", "", _toolkit.getStr_InList_ByKey(keys[i], ss_gen[1], ss_gen[0]))

        except Exception as e:
            try:
                print("RuntimeError: ", e)
                print(ss_gen)
            finally:
                e = None
                del e

        dict_table = dict(((k, dict_table[k]) for k in keys))
        return dict_table
