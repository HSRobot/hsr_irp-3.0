#!/usr/bin/env python
# -*- coding:UTF-8 -*-

"""
This script launches several training pipelines defined in a configuration file to train several models for several
objects
"""

import rospy

from object_recognition_core.db import ObjectDb, ObjectDbParameters, ObjectDbTypes, models
from object_recognition_core.db.tools import interpret_object_ids, init_object_databases
from object_recognition_core.pipelines.plasm import create_plasm
from object_recognition_core.utils.find_classes import find_class
from object_recognition_core.utils.training_detection_args import create_parser, read_arguments
import ecto
import sys

from ork_interface.srv import *

'''
if __name__ == '__main__':
    parser = create_parser(do_training=True)

    args = parser.parse_args()
    ork_params, _args = read_arguments(args)

    for _pipeline_id, pipeline_param in ork_params.iteritems():
        pipeline_class = find_class([ pipeline_param['module'] ], pipeline_param['type'] )
        if not pipeline_class:
            raise RuntimeError('Invalid pipeline name: %s\nMake sure that the pipeline type is defined by a '
                               'TrainingPipeline class, in the name class function.' % pipeline_param['type'])

        db_params_raw = pipeline_param['parameters'].get('json_db', {})
        db_params = db_params_raw
        object_ids = interpret_object_ids(db_params, pipeline_param.get('parameters', {}).get('json_object_ids', []))
        print('Training %d objects.' % len(object_ids))
        for object_id in object_ids:
            print('computing object_id: %s' % object_id)
            object_id = object_id.encode('ascii')

            ork_params_sub = {}
            ork_params_sub[_pipeline_id] = pipeline_param
            ork_params_sub[_pipeline_id]['parameters']['object_id'] = object_id
            plasm = create_plasm(ork_params_sub)
            plasm.execute()

        # Make sure the views exist
        object_db = ObjectDb(db_params)
        db_params = ObjectDbParameters(db_params)
        if db_params.type == ObjectDbTypes.COUCHDB:
            import couchdb
            import json
            dic = json.loads(db_params_raw)
            couch = couchdb.Server(dic['root'])
            init_object_databases(couch)
'''

# rosrun object_recognition_core training -c `rospack find object_recognition_linemod`/conf/training.ork

def handles_training(req):
    parser = create_parser(do_training=True)

    #args = parser.parse_args()
    args = parser.parse_args(['-c', req.cmd])
    args = parser.parse_args(['--config_file', req.path])
    ork_params, _args = read_arguments(args)

    for _pipeline_id, pipeline_param in ork_params.iteritems():
        pipeline_class = find_class([ pipeline_param['module'] ], pipeline_param['type'] )
        if not pipeline_class:
            raise RuntimeError('Invalid pipeline name: %s\nMake sure that the pipeline type is defined by a '
                               'TrainingPipeline class, in the name class function.' % pipeline_param['type'])

        db_params_raw = pipeline_param['parameters'].get('json_db', {})
        db_params = db_params_raw
        object_ids = interpret_object_ids(db_params, pipeline_param.get('parameters', {}).get('json_object_ids', []))
        print('Training %d objects.' % len(object_ids))
        for object_id in object_ids:
            print('computing object_id: %s' % object_id)
            object_id = object_id.encode('ascii')

            ork_params_sub = {}
            ork_params_sub[_pipeline_id] = pipeline_param
            ork_params_sub[_pipeline_id]['parameters']['object_id'] = object_id
            plasm = create_plasm(ork_params_sub)
            plasm.execute()

        # Make sure the views exist
        object_db = ObjectDb(db_params)
        db_params = ObjectDbParameters(db_params)
        if db_params.type == ObjectDbTypes.COUCHDB:
            import couchdb
            import json
            dic = json.loads(db_params_raw)
            couch = couchdb.Server(dic['root'])
            init_object_databases(couch)
	
    return training_srvResponse()

def training_server():
    # 初始化节点 用节点 发布服务数据
    rospy.init_node('training_server')
    # 声明了一个 'training'的服务， 数据类型为training_srv， 调用handles_training回调函数
    s = rospy.Service('training', training_srv, handles_training)
    print "Ready to train object."
    rospy.spin()
			
if __name__ == "__main__":
    training_server()
