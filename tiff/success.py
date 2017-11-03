import os


class LocalSuccessStrategy(object):
    @staticmethod
    def post_convert(success, converter):
        if success:
            converter.docindex_handler.add_file(converter.next_file,
                                                converter.tiff_path)


class LocalInPlaceSuccessStrategy(object):
    @staticmethod
    def post_convert(success, converter):
        if success:
            LocalSuccessStrategy.post_convert(success, converter)
            os.remove(converter.next_file)
