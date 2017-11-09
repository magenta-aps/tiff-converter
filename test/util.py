import os
import shutil
import tempfile


class StandardConversionTestSetup(object):
    """
    Create a temporary folder and then copy the conversion source to here.
    Create an empty folder to be used as the target.
    """

    def prepare(self, source):
        # Create the temp dir
        self.temp_dir = os.path.join(tempfile.gettempdir(), '_tmp_dir')
        if os.path.isdir(self.temp_dir):
            shutil.rmtree(self.temp_dir)
        os.mkdir(self.temp_dir)

        # Copy source from test/resources into the temp_dir
        temp_source = os.path.join(self.temp_dir, 'source')
        shutil.copytree(source, temp_source)

        # Create temporary target dir
        temp_target = os.path.join(self.temp_dir, 'target')
        os.mkdir(temp_target)

        return temp_source, temp_target

    def cleanup(self):
        if os.path.isdir(self.temp_dir):
            shutil.rmtree(self.temp_dir)
