# -*- coding:utf8 -*-
# File   : demo.py
# Author : Jiayuan Mao
# Email  : maojiayuan@gmail.com
# Date   : 3/16/17
# 
# This file is part of TensorArtist.

from tartist.core import get_env, get_logger, set_env
from tartist.core.utils.cli import load_desc, parse_devices, parse_args
from tartist.nn import Env

import sys
import argparse
import os.path as osp
import tensorflow as tf

logger = get_logger(__file__)

parser = argparse.ArgumentParser()
parser.add_argument(dest='desc', help='The description file module')
parser.add_argument('-w', '--weights', dest='weights_path', help='The pickle containing weights')
parser.add_argument('-e', '--epoch', dest='epoch_num', help='Epoch number')
parser.add_argument('-d', '--dev', dest='devices', default=[], nargs='+',
                    help='The devices trainer will use, default value can be set in env')
args = parse_args(parser)


def get_weights_path():
    if args.weights_path is not None:
        return args.weights_path
    
    if args.epoch_num == 'last':
        filename = 'last_epoch.snapshot.pkl'
    else:
        epoch = int(args.epoch_num)
        filename = 'epoch_{}.snapshot.pkl'.format(epoch)

    return osp.join(get_env('dir.root'), 'snapshots', filename)


def main():
    from tartist.plugins.trainer_enhancer import snapshot

    desc = load_desc(args.desc)
    devices = parse_devices(args.devices)
    assert len(devices) > 0

    assert args.weights_path is not None or args.epoch_num is not None

    env = Env(Env.Phase.TEST, devices[0])
    env.flags.update(**get_env('demo.env_flags', {}))

    with env.as_default():
        desc.make_network(env)

        func = env.make_func()
        func.compile(env.network.outputs)

        env.initialize_all_variables()
        snapshot.load_weights_file(env, get_weights_path())

    if not hasattr(desc, 'main_demo'):
        logger.warn('Function main_demo not found in desc {}; fallback to old-style demo.'.format(desc))
        set_env('demo.customized', False)

    if get_env('demo.customized', True):
        desc.main_demo(env, func)
    else:
        logger.warn('Non-customized demo has been deprecated. Use main_demo instead')
        assert hasattr(desc, 'make_dataflow_demo') and hasattr(desc, 'demo')

        it = iter(desc.make_dataflow_demo(env))
        for data in it:
            if type(data) is tuple:
                feed_dict, extra_info = data
            else:
                feed_dict, extra_info = data, None
            res = func(**feed_dict)
            desc.demo(feed_dict, res, extra_info)


if __name__ == '__main__':
    main()
