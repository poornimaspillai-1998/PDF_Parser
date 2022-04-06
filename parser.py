import traceback
import camelot
import json
import logging
import datetime
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.secrets'))


class Pdfparser():
    def __init__(self):
        self.file = ''
        self.column_headings = []
        self.records = []
        self.sub_type = ''
        self.file = os.environ.get('path')+os.environ.get('filename')

    def parse_pdf(self):
        try:
            
            self.tables = camelot.read_pdf(self.file)
            tab=self.tables[0].df
            json_data = tab.to_json(orient = 'split')
            json_rec = json.loads(json_data)
            len_json = len(json_rec['data'])
            column_headings1 = json_rec['data'][0]
            column_headings2 = json_rec['data'][1]
            self.column_headings.append(column_headings1[0])
            for i in column_headings2:
                if i=='':
                    continue
                self.column_headings.append(i)
            self.column_headings.append(column_headings1[-1])
            for dat in range(2,len_json):
                data1 = json_rec['data'][dat] 
                each_dict = {}
                if '\n' in data1[0]:
                    sub_type_list = data1[0].split('\n')
                    self.sub_type = sub_type_list[0]
                    key = sub_type_list[1]
                    each_dict["sub_type"] = self.sub_type
                    each_dict["key"] = key
                else:
                    key = data1[0]
                    each_dict["sub_type"] = self.sub_type
                    each_dict["key"] = key

                heading_values = dict(zip(self.column_headings[1:],data1[1:]))

                for hv in heading_values:
                    new_dict = {}
                    new_dict['sub_type'] = each_dict['sub_type']
                    new_dict['key'] = each_dict['key']
                    new_dict['column_heading'] = hv
                    new_dict['value'] = heading_values[hv]
                    
                    if not new_dict['value'] == '':
                        self.records.append(new_dict)
            return self.records
        except Exception:
            logging.error(traceback.format_exc())

if __name__ == "__main__":
    filename = 'logs/log_'+str(datetime.datetime.now())+'.log'
    logging.basicConfig(filename=filename,filemode='w')
    parse_to_json = Pdfparser()
    print(parse_to_json.parse_pdf())
