class DocumentManager(object):

    MAX = 10000

    def get_location(self):
        pass

    def increase_mID(self):
        pass


class LocalDocumentManager(DocumentManager):

    def __init__(self, mID=1, dCf=1, dID=1):
        self.set_location(mID, dCf, dID)

    def get_location(self):
        dID = self.dID
        dCf = self.dCf
        mID = self.mID

        self._increment_values()

        return mID, dCf, dID

    def set_location(self, mID, dCf, dID):
        self.mID = mID
        self.dCf = dCf
        self.dID = dID

        if mID != 1 or dCf != 1 or dID != 1:
            self._increment_values()

    def _increment_values(self):
        if self.dID % self.MAX == 0:
            if self.dCf % self.MAX == 0:
                self.mID += 1
            self.dCf += 1

        self.dID += 1
