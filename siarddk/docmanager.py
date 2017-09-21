class DocumentManager(object):

    MAX = 10000

    def get_location(self):
        pass

    def increase_mID(self):
        pass


class LocalDocumentManager(DocumentManager):

    def __init__(self):
        self.dID = 1
        self.dCf = 1
        self.mID = 1

    def get_location(self):
        dID = self.dID
        dCf = self.dCf
        mID = self.mID

        if self.dID % self.MAX == 0:
            if self.dCf % self.MAX == 0:
                self.mID += 1
            self.dCf += 1

        self.dID += 1

        return mID, dCf, dID
