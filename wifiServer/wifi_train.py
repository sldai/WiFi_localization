#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import numpy as np
import tensorflow as tf
# 加载FR_inference.py中定义的常量和前向传播的函数
import wifi_inference

# 配置神经网络的参数
BATCH_SIZE = 50
LEARNING_RATE_BASE = 0.01
LEARNING_RATE_DECAY = 0.99
REGULARAZTION_RATE = 0.0001
TRAINING_STEPS = 5000
MOVING_AVERAGE_DECAY = 0.99
TRAIN_SIZE = 2349
# 模型保存的路径和文件名
MODEL_SAVE_PATH = "model_1/model1/"
MODEL_NAME = "model.ckpt"


def train(train_data, train_label):
    # 定义输入输出placeholder
    # 调整输入数据placeholder的格式，输入为一个四维矩阵
    x = tf.placeholder(tf.float32, [
        BATCH_SIZE,                             # 第一维表示一个batch中样例的个数
        wifi_inference.INPUT_NODE],          # 第四维表示图片的深度，对于RBG格式的图片，深度为3
                       name='x-input')
    y_ = tf.placeholder(tf.float32, [None, wifi_inference.OUTPUT_NODE], name='y-input')

    regularizer = tf.contrib.layers.l2_regularizer(REGULARAZTION_RATE)
    # 直接使用FR_inference.py中定义的前向传播过程
    y = wifi_inference.inference(x, True, regularizer)
    global_step = tf.Variable(0, trainable=False)

    #定义损失函数、学习率、滑动平均操作以及训练过程
    variable_averages = tf.train.ExponentialMovingAverage(MOVING_AVERAGE_DECAY, global_step)
    variable_averages_op = variable_averages.apply(tf.trainable_variables())
    # cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(logits=y, labels=tf.argmax(y_, 1))
    # cross_entropy_mean = tf.reduce_mean(cross_entropy)
    # loss = cross_entropy_mean + tf.add_n(tf.get_collection('losses'))
    diff = y - y_  # Subtract element-wise
    squaredDiff = diff ** 2  # squared for the subtract
    distance = squaredDiff ** 0.5
    average_dist = tf.reduce_mean(distance)
    loss = average_dist + tf.add_n(tf.get_collection('losses'))
    learning_rate = tf.train.exponential_decay(LEARNING_RATE_BASE, global_step, TRAIN_SIZE/BATCH_SIZE, LEARNING_RATE_DECAY)
    train_step = tf.train.AdamOptimizer(learning_rate).minimize(loss, global_step=global_step)
    # train_step = tf.train.GradientDescentOptimizer(learning_rate).minimize(loss, global_step=global_step)
    with tf.control_dependencies([train_step, variable_averages_op]):
        train_op = tf.no_op(name='train')

    # 初始化Tensorflow持久化类
    saver = tf.train.Saver()
    with tf.Session() as sess:
        tf.global_variables_initializer().run()
        # 验证和测试的过程将会有一个独立的程序来完成
        for i in range(TRAINING_STEPS):
            start = (i * BATCH_SIZE) % TRAIN_SIZE
            end = min(start + BATCH_SIZE, TRAIN_SIZE)
            xs = train_data[end - BATCH_SIZE:end]
            ys = train_label[end - BATCH_SIZE:end]
            if (end - start) != BATCH_SIZE:
                for j in range(end - start):
                    xs[j] = train_data[start + j]
                    ys[j] = train_label[start + j]
            for t in range(BATCH_SIZE - (end - start)):
                xs[end - start + t] = train_data[t]
                ys[end - start + t] = train_label[t]
            #类似地将输入的训练数据格式调整为一个四维矩阵，并将这个调整后的数据传入sess.run过程
            reshaped_xs = np.reshape(xs, (BATCH_SIZE, wifi_inference.INPUT_NODE))
            _, loss_value, step = sess.run([train_op, loss, global_step], feed_dict={x: reshaped_xs, y_: ys})
            print(i, ":", loss_value)
            #每100轮保存一次模型。
            if i%100 == 0:
                # 输出当前的训练情况。这里只输出了模型在当前训练batch上的损失函数大小。通过损失函数的大小可以大概了解训练的情况。
                # 在验证数据集上的正确率信息会有一个单独的程序来生成。
                print("After %d training step(s), loss on training batch is %f." % (step, loss_value))
                # 保存当前的模型。注意这里隔出了global_step参数，这样可以让每个被保存模型的文件名末尾加上训练的轮数，比如“model.ckpt-1000”表示训练1000轮后得到的模型
                saver.save(sess, os.path.join(MODEL_SAVE_PATH, MODEL_NAME), global_step=global_step)


def main(argv=None):
    train_data = np.load("train_data.npy")
    train_label = np.load("train_label.npy")
    train(train_data, train_label)


if __name__ == '__main__':
    tf.app.run()