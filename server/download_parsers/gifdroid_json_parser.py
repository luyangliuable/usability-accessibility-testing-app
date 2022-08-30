import mimetypes
from download_parsers.strategy import Strategy
import os
from typing import List

class gifdroidJsonParser(Strategy):

    gifdroid_result_file_json_format = {
        'name': '',
        'type': '',
        's3_bucket': '',
        's3_key': '',
    }

    @staticmethod
    def do_algorithm(uuid: str, file: List) -> List:
        # res =  self.gifdroid_result_file_json_format
        res = [{} for _ in range(len(file))]

        for i in range(len(file)):
            tmp = gifdroidJsonParser.gifdroid_result_file_json_format

            tmp['name'] = file[i]

            tmp['type'] = str( mimetypes.guess_type(file[i])[0] )
            tmp['s3_bucket'] = 'apk'

            # TODO when files are stored in algorithm folders change this to:
            # tmp['s3_key'] = os.path.join(uuid, apl_algorithm, file[i])
            tmp['s3_key'] = os.path.join(uuid, file[i])

            res[i] = tmp

        return res
