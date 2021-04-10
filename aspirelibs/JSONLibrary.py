# -*- coding: utf-8 -*-

import os.path
import json
from jsonpath_rw import Index, Fields
from jsonpath_rw_ext import parse
from aspirelibs.logger import logger

class JSONObject(object):
    def load_json_from_file(self, file_name):
        """Load JSON from file.

        Return json as a dictionary object.

        Arguments:
            - file_name: absolute json file name

        Return json object (list or dictionary)

        Examples:
        | ${result}=  |  Load Json From File  | /path/to/file.json |
        """
        print("Check if file exists")
        if os.path.isfile(file_name) is False:
            print("JSON file: " + file_name + " not found")
            raise IOError
        with open(file_name) as json_file:
            data = json.load(json_file)
        return data

    def add_object_to_json(self, json_object, json_path, object_to_add):
        """Add an dictionary or list object to json object using json_path

            Arguments:
                - json_object: json as a dictionary object.
                - json_path: jsonpath expression
                - object_to_add: dictionary or list object to add to json_object which is matched by json_path

            Return new json object.

            Examples:
            | ${dict}=  | Create Dictionary    | latitude=13.1234 | longitude=130.1234 |
            | ${json}=  |  Add Object To Json  | ${json}          | $..address         |  ${dict} |
            """
        json_path_expr = parse(json_path)
        if str(json_path_expr) == "$.root":
            json_object.update(eval(object_to_add))
        else:
            for match in json_path_expr.find(json_object):
                if type(match.value) is dict:
                    match.value.update(eval(object_to_add))
                if type(match.value) is list:
                    match.value.append(object_to_add)
        return json_object

    def get_value_from_json(self, json_object, json_path):
        """Get Value From JSON using JSONPath

        Arguments:
            - json_object: json as a dictionary object.
            - json_path: jsonpath expression

        Return array of values

        Examples:
        | ${values}=  |  Get Value From Jsonpath  | ${json} |  $..phone_number |
        """
        json_path_expr = parse(json_path)
        #print(json_path_expr)
        return [match.value for match in json_path_expr.find(json_object)]

    def update_value_to_json(self, json_object, json_path, new_value):
        """Update value to JSON using JSONPath

        Arguments:
            - json_object: json as a dictionary object.
            - json_path: jsonpath expression
            - new_value: value to update

        Return new json_object

        Examples:
        | ${json_object}=  |  Update Value To Json | ${json} |  $..address.streetAddress  |  Ratchadapisek Road |
        """
        json_path_expr = parse(json_path)
        if new_value.lower().startswith('(int)'):
            new_value = int(new_value.lstrip('(int)'))
        elif new_value.lower().startswith('(bool)'):
            if new_value.lower().find('true'):
                new_value = True
            else:
                new_value = False
        else:
            pass
        if new_value==u"None":
            new_value = None        
        
        for match in json_path_expr.find(json_object):
            path = match.path
            if isinstance(path, Index):
                match.context.value[match.path.index] = new_value
            elif isinstance(path, Fields):
                match.context.value[match.path.fields[0]] = new_value
        return json_object

    def delete_object_from_json(self, json_object, json_path):
        """Delete Object From JSON using json_path

        Arguments:
            - json_object: json as a dictionary object.
            - json_path: jsonpath expression

        Return new json_object

        Examples:
        | ${json_object}=  |  Delete Object From Json | ${json} |  $..address.streetAddress  |
        """
        json_path_expr = parse(json_path)
        for match in json_path_expr.find(json_object):
            path = match.path
            if isinstance(path, Index):
                del(match.context.value[match.path.index])
            elif isinstance(path, Fields):
                del(match.context.value[match.path.fields[0]])
        return json_object

    def convert_json_to_string(self, json_object):
        """Convert JSON object to string

        Arguments:
            - json_object: json as a dictionary object.

        Return new json_string

        Examples:
        | ${json_str}=  |  Convert JSON To String | ${json_obj} |
        """
        return json.dumps(json_object)

    def upadate_values_to_json(self, json_obj, kvs):
        if (kvs is None) or (len(kvs) == 0):
            return json_obj
         
        for kv in kvs:
            field_info = kv.split("=")
            json_obj = JSONObject.update_value_to_json(self, json_obj, field_info[0], field_info[1])
             
        return json_obj
 
    def refactoring_json(self,req_obj,kvs):
        if(kvs is None) or (len(kvs)==0):
            return req_obj

        for kv in kvs:
            field_info = kv.split("=")
            if field_info[1] == "delete_Object":
                req_obj = JSONObject.delete_object_from_json(self,req_obj,field_info[0])
            elif field_info[1] == "add_Object":
                req_obj = JSONObject.add_object_to_json(self,req_obj,field_info[0],field_info[2])
            else:
                req_obj = JSONObject.update_value_to_json(self, req_obj,field_info[0],field_info[1])
        return req_obj
        

