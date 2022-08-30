import mimetypes
from download_parsers.strategy import Strategy
import os
from typing import List

class gifdroidJsonParser(Strategy):

    gifdroid_result_file_json_format = {
        'name': '',
        'link': '',
        'type': '',
        's3_bucket': '',
        's3_key': '',
    }

    @staticmethod
    def do_algorithm(uuid: str, file: List, name: List) -> List:
        # res =  self.gifdroid_result_file_json_format

        if type( file ) != list: raise ValueError("file must be a list")

        res = [{} for _ in range(len(file))]
        print(name)

        for i in range(len(file)):
            tmp = gifdroidJsonParser.gifdroid_result_file_json_format

            tmp['link'] = file[i]
            tmp['name'] = name[i]

            tmp['type'] = str( mimetypes.guess_type(name[i])[0] )
            tmp['s3_bucket'] = 'apk'

            # TODO when files are stored in algorithm folders change this to:
            # tmp['s3_key'] = os.path.join(uuid, apl_algorithm, file[i])
            tmp['s3_key'] = os.path.join(uuid, name[i])

            res[i] = tmp

        return res
