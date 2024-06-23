import copy


class registry_i:

    def divfun(self, fun):
        if self.get_fun(str(fun).split(' ')[1])==None:
            exec(('self.' + str(fun).split(' ')[1] + '=fun'))
        else:
            print(str(fun).split(' ')[1],'该函数存在注册中心，请换一个名字！')

    def __getitem__(self, funname):
        return self.get_fun(funname)

    def get_fun(self,funname):
        try:
            fun=eval(('self.'+ str(funname)))
        except:
            fun=None
        return fun

Registry=registry_i()

# 初始化注册的方法
def registry_fun_init(registry_dict):
    '''
    :param registry_dict: {"type": registry_name,"params":{"num_classes":self.num_classes,"in_channal":self.input[2]}}
    :return:
    '''
    registry_name = registry_dict['type']
    registry_fun = Registry[registry_name]

    param_dict = None
    if registry_dict.get('params'):
        param_dict = registry_dict['params']
        fun = registry_fun(**param_dict)
    else:
        fun = registry_fun()
    return fun
