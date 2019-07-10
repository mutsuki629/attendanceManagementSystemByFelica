import time

class ignore:
    def __init__(self):
        self.ignore_list = []
        self.interval_time = 300 # sec

    def check(self, tag):
        for lst in self.ignore_list:
            t = lst[1] + self.interval_time
            if lst[0]==tag[0] and t>tag[1]:
                return 0
        return 1
        
    def update(self, tag):
        for lst in self.ignore_list:
            if lst[0]==tag[0]:
                self.ignore_list.remove(lst)
        self.ignore_list.append(tag)

    def show(self):
        print(self.ignore_list)

if __name__=='__main__':
    ig = ignore()

    t = time.time()
    idm = 'qwert'
    idm2 = 'qwe'

    lsts = ((idm, t), (idm, t+200), (idm2, t+300))
    for lst in lsts:
        if ig.check(lst):
            ig.update(lst)
            print(1)
        else:
            ig.update(lst)
            print(0)

    ig.show()