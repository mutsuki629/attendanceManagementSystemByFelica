class queue:
    def __init__(self):
        self.queue=[]

    def append(self, func, arg):
        self.queue.append((func, arg))

    def execute(self):
        if self.queue==[]:
            return 1
        func, arg = self.queue.pop(0)
        func(*arg)

    def exist(self):
        if self.queue==[]:
            return 0
        else:
            return 1

if __name__=='__main__':
    a = [1, 2, 3]
    q = queue()
    q.append(print, (1,1,1))
    print(q.exist())
    q.execute()
    print(q.exist())