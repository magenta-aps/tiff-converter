class DocumentManager(object):

    MAX = 10000

    def get_location(self):
        pass

    def increase_mID(self):
        pass


class LocalDocumentManager(DocumentManager):

    def __init__(self):
        self.dID = 0
        self.dCf = 1
        self.mID = 1

    def get_location(self):
        self.dID += 1
        if self.dID > self.MAX:
            self.dID = 1
            self.dCf += 1
        if self.dCf > self.MAX:
            self.dCf = 1
            self.mID += 1
        return self.mID, self.dCf, self.dID
