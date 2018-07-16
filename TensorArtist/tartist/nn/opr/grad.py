# -*- coding:utf8 -*-
# File   : grad.py
# Author : Jiayuan Mao
# Email  : maojiayuan@gmail.com
# Date   : 4/13/17
#
# This file is part of TensorArtist.


from .helper import as_tftensor, wrap_varnode_func, wrap_named_op
from tensorflow.python.framework import function

import tensorflow as tf

__all__ = ['clip_gradient', 'preserve_gradient_unary']


@wrap_named_op
def clip_gradient(inpvar, clip_value_min, clip_value_max, name='clip_gradient'):
    def _clip_gradient_backward(unused_op, grad):
        return tf.clip_by_value(grad, clip_value_min, clip_value_max)

    @function.Defun(inpvar.dtype, python_grad_func=_clip_gradient_backward, func_name="ClipGradient")
    def _clip_gradient_forward(x):
        return x

    with tf.name_scope(name, values=[inpvar]):
        out = _clip_gradient_forward(inpvar)
        as_tftensor(out).set_shape(as_tftensor(inpvar).get_shape())
    return out


def preserve_gradient_unary(func):
    @wrap_varnode_func
    def new_func(inpvar, *args, **kwargs):
        def _backward(op, grad):
            return grad
        
        @function.Defun(inpvar.dtype, python_grad_func=_backward, func_name=func.__name__)
        def _forward(x):
            return func(x, *args, **kwargs)

        with tf.name_scope(func.__name__, values=[inpvar]):
            out = _forward(inpvar)
            as_tftensor(out).set_shape(as_tftensor(inpvar).get_shape())
        return out
    
    return new_func
