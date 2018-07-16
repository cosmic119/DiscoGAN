# -*- coding:utf8 -*-
# File   : tfutils.py
# Author : Jiayuan Mao
# Email  : maojiayuan@gmail.com
# Date   : 1/31/17
# 
# This file is part of TensorArtist.

import re
import tensorflow as tf


class TArtGraphKeys:
    PLACEHOLDERS = 'placeholders'
    TART_VARIABLES = 'tart_variables'
    INFERENCE_SUMMARIES = 'inference_summaries'
    SCALAR_VARIABLES = 'scalar_variables'
    OPTIMIZER_VARIABLES = 'optimizer_variables'

    # DEPRECATED: (2017-12-02)
    TART_OPERATORS = 'tart_operators'


def clean_name(tensor, suffix=':0'):
    name = tensor.name
    if name.endswith(suffix):
        name = name[:-len(suffix)]
    return name


def clean_summary_suffix(name):
    return re.sub('_\d+$', '', name)


def remove_tower_name(name):
    return re.sub('^tower/\d+/', '', name)


def format_summary_name(name):
    name = clean_summary_suffix(name)
    name = remove_tower_name(name)
    if 'train/' in name:
        name = name.replace('train/', '')
        name = 'train/' + name
    return name


def assign_variable(var, value, session=None, use_locking=False):
    from .graph.env import get_default_env
    session = session or get_default_env().session
    session.run(var.assign(value, use_locking=use_locking))


def fetch_variable(var, session=None):
    from .graph.env import get_default_env
    session = session or get_default_env().session
    try:
        return session.run(var)
    except tf.errors.FailedPreconditionError:
        session.run(var.initializer)
        return session.run(var)


def extend_collection_list(base, *others):
    if base is None:
        return others
    if type(base) is str:
        return (base, ) + others
    assert isinstance(base, (tuple, list))
    return tuple(base) + others
