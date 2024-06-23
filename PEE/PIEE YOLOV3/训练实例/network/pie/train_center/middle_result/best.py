class best:
    def __init__(self,list):
        self.list=list
        self.loss=999999
        self.x=0
        for i in self.list:
            if i !='loss':
                exec('self.'+i+'=0')
    def add(self,loss,dict):
        if self.loss > loss:
            self.loss = loss
            self.x = 1
        # print("dict", dict)
        # print('list',self.list)
        for i in dict:
            for j in i:
                # print("get", j, str(i.get(j)))
                if j!='loss' and self.x==1 and j.split('_')[0] in self.list and j.split('_')[1]=='all':
                    exec('self.' + j.split('_')[0] + '='+str(i.get(j)))
        self.x=0
    def __getitem__(self, item):
        return eval('self.' + item)
    def show(self):
        xx={}
        # a=[]
        for i in self.list:
            xx[i]=eval('self.' + i)
            # a.append(xx)
        return xx
# Best=best()