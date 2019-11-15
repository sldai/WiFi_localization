#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tensorflow as tf

# 定义神经网络相关的参数
INPUT_NODE = 2
OUTPUT_NODE = 20

# 全连接层的节点个数
FC1_SIZE = 512
FC2_SIZE = 1024
FC3_SIZE = 2048
FC4_SIZE = 1024
FC5_SIZE = 512


def inference(input_tensor, train, regularizer):

    with tf.variable_scope('layer1-fc1'):
        fc1_weights = tf.get_variable("weight", [INPUT_NODE, FC1_SIZE],
                                      initializer = tf.truncated_normal_initializer(stddev = 0.1))
        # 只有全连接层的权重需要加入正则化
        if regularizer != None:
            tf.add_to_collection('losses', regularizer(fc1_weights))
        fc1_biases = tf.get_variable('bias', [FC1_SIZE], initializer = tf.constant_initializer(0.1))
        fc1 = tf.nn.relu(tf.matmul(input_tensor, fc1_weights)+fc1_biases)

    with tf.name_scope('layer2-fc2'):
        fc2_weights = tf.get_variable("weight", [FC1_SIZE, FC2_SIZE],
                                      initializer=tf.truncated_normal_initializer(stddev=0.1))
        # 只有全连接层的权重需要加入正则化
        if regularizer != None:
            tf.add_to_collection('losses', regularizer(fc2_weights))
        fc2_biases = tf.get_variable('bias', [FC2_SIZE], initializer=tf.constant_initializer(0.1))
        fc2 = tf.nn.relu(tf.matmul(fc1, fc2_weights) + fc2_biases)


    with tf.variable_scope('layer3-fc3'):
        fc3_weights = tf.get_variable("weight", [FC2_SIZE, FC3_SIZE],
                                      initializer=tf.truncated_normal_initializer(stddev=0.1))
        # 只有全连接层的权重需要加入正则化
        if regularizer != None:
            tf.add_to_collection('losses', regularizer(fc3_weights))
        fc3_biases = tf.get_variable('bias', [FC3_SIZE], initializer=tf.constant_initializer(0.1))
        fc3 = tf.nn.relu(tf.matmul(fc2, fc3_weights) + fc3_biases)

    with tf.variable_scope('layer4-fc4'):
        fc4_weights = tf.get_variable("weight", [FC3_SIZE, FC4_SIZE],
                                      initializer=tf.truncated_normal_initializer(stddev=0.1))
        # 只有全连接层的权重需要加入正则化
        if regularizer != None:
            tf.add_to_collection('losses', regularizer(fc4_weights))
        fc4_biases = tf.get_variable('bias', [FC4_SIZE], initializer=tf.constant_initializer(0.1))
        fc4 = tf.nn.relu(tf.matmul(fc3, fc4_weights) + fc4_biases)

    with tf.variable_scope('layer5-fc5'):
        fc5_weights = tf.get_variable("weight", [FC4_SIZE, FC5_SIZE],
                                      initializer=tf.truncated_normal_initializer(stddev=0.1))
        # 只有全连接层的权重需要加入正则化
        if regularizer != None:
            tf.add_to_collection('losses', regularizer(fc5_weights))
        fc5_biases = tf.get_variable('bias', [FC5_SIZE], initializer=tf.constant_initializer(0.1))
        fc5 = tf.nn.relu(tf.matmul(fc4, fc5_weights) + fc5_biases)

    with tf.variable_scope('layer6-fc6'):
        fc6_weights = tf.get_variable("weight", [FC5_SIZE, OUTPUT_NODE],
                                      initializer=tf.truncated_normal_initializer(stddev=0.1))
        # 只有全连接层的权重需要加入正则化
        if regularizer != None:
            tf.add_to_collection('losses', regularizer(fc6_weights))
        fc6_biases = tf.get_variable('bias', [OUTPUT_NODE], initializer=tf.constant_initializer(0.1))
        logit = tf.matmul(fc5, fc6_weights) + fc6_biases

    return logit