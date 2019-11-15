#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tensorflow as tf
import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# 定义神经网络相关的参数
INPUT_NODE = 2
OUTPUT_NODE = 1
# 全连接层的节点个数
FC1_SIZE = 512
FC2_SIZE = 1024
FC3_SIZE = 2048
FC4_SIZE = 1024
FC5_SIZE = 512

# 配置神经网络的参数
BATCH_SIZE = 50
LEARNING_RATE_BASE = 0.01
LEARNING_RATE_DECAY = 0.99
REGULARAZTION_RATE = 0.0001
TRAINING_STEPS = 1000
MOVING_AVERAGE_DECAY = 0.99
# 模型保存的路径和文件名

MODEL_NAME = "model.ckpt"
SUMMARY_DIR = "D:\log\\"


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


def train(train_data, train_label, graph):
    global TRAIN_SIZE
    global TEST_SIZE
    global MODEL_SAVE_PATH
    with graph.as_default():
        # 定义输入输出placeholder
        # 调整输入数据placeholder的格式，输入为一个四维矩阵
        x = tf.placeholder(tf.float32, [
            BATCH_SIZE,                             # 第一维表示一个batch中样例的个数
            INPUT_NODE],          # 第四维表示图片的深度，对于RBG格式的图片，深度为3
                           name='x-input')
        y_ = tf.placeholder(tf.float32, [None, OUTPUT_NODE], name='y-input')

        regularizer = tf.contrib.layers.l2_regularizer(REGULARAZTION_RATE)
        # 直接使用FR_inference.py中定义的前向传播过程
        y = inference(x, True, regularizer)
        global_step = tf.Variable(0, trainable=False)

        #定义损失函数、学习率、滑动平均操作以及训练过程
        variable_averages = tf.train.ExponentialMovingAverage(MOVING_AVERAGE_DECAY, global_step)
        variable_averages_op = variable_averages.apply(tf.trainable_variables())
        diff = y - y_  # Subtract element-wise
        squaredDiff = diff ** 2  # squared for the subtract
        distance = squaredDiff ** 0.5
        average_dist = tf.reduce_mean(distance)
        loss = average_dist + tf.add_n(tf.get_collection('losses'))
        learning_rate = tf.train.exponential_decay(LEARNING_RATE_BASE, global_step, TRAIN_SIZE/BATCH_SIZE, LEARNING_RATE_DECAY)
        train_step = tf.train.AdamOptimizer(learning_rate).minimize(loss, global_step=global_step)
        tf.summary.scalar(SUMMARY_DIR, loss)
        merged_summary_op = tf.summary.merge_all()
        with tf.control_dependencies([train_step, variable_averages_op]):
            train_op = tf.no_op(name='train')

        # 初始化Tensorflow持久化类
        saver = tf.train.Saver()
        with tf.Session(graph=graph) as sess:
            summary_writer = tf.summary.FileWriter(SUMMARY_DIR, graph=tf.get_default_graph())
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
                reshaped_xs = np.reshape(xs, (BATCH_SIZE, INPUT_NODE))
                _, loss_value, step, summary = sess.run([train_op, loss, global_step, merged_summary_op],
                                                        feed_dict={x: reshaped_xs, y_: ys})
                summary_writer.add_summary(summary, i * BATCH_SIZE)
                print(i, ":", loss_value)
                #每100轮保存一次模型。
                if i == 999:
                    # 输出当前的训练情况。这里只输出了模型在当前训练batch上的损失函数大小。通过损失函数的大小可以大概了解训练的情况。
                    # 在验证数据集上的正确率信息会有一个单独的程序来生成。
                    print("After %d training step(s), loss on training batch is %f." % (step, loss_value))
                    # 保存当前的模型。注意这里隔出了global_step参数，这样可以让每个被保存模型的文件名末尾加上训练的轮数，比如“model.ckpt-1000”表示训练1000轮后得到的模型
                    saver.save(sess, os.path.join(MODEL_SAVE_PATH, MODEL_NAME), global_step=global_step)


def evaluate(test_data, MODEL_SAVE_PATH):
    with tf.Graph().as_default() as g:
        # 定义输入输出的格式
        x = tf.placeholder(tf.float32, [
            TEST_SIZE,          # 第一维表示样例的个数
            INPUT_NODE],          # 第四维表示图片的深度，对于RBG格式的图片，深度为5
                       name='x-input')

        validate_feed = {x: np.reshape(test_data, (TEST_SIZE, INPUT_NODE))}
        # 直接通过调用封装好的函数来计算前向传播的结果。
        # 因为测试时不关注正则损失的值，所以这里用于计算正则化损失的函数被设置为None。
        y = inference(x, False, None)

        # 使用前向传播的结果计算正确率。
        # 如果需要对未知的样例进行分类，那么使用tf.argmax(y, 1)就可以得到输入样例的预测类别了。


        # 通过变量重命名的方式来加载模型，这样在前向传播的过程中就不需要调用求滑动平均的函数来获取平局值了。
        # 这样就可以完全共用FR_inference.py中定义的前向传播过程
        variable_averages = tf.train.ExponentialMovingAverage(MOVING_AVERAGE_DECAY)
        variable_to_restore = variable_averages.variables_to_restore()
        saver = tf.train.Saver(variable_to_restore)


        #每隔EVAL_INTERVAL_SECS秒调用一次计算正确率的过程以检测训练过程中正确率的变化
        while True:
            with tf.Session() as sess:
                # tf.train.get_checkpoint_state函数会通过checkpoint文件自动找到目录中最新模型的文件名
                ckpt = tf.train.get_checkpoint_state(MODEL_SAVE_PATH)
                if ckpt and ckpt.model_checkpoint_path:
                    # 加载模型
                    saver.restore(sess, ckpt.model_checkpoint_path)
                    # 通过文件名得到模型保存时迭代的轮数
                    global_step = ckpt.model_checkpoint_path.split('/')[-1].split('-')[-1]
                    y_value = sess.run(y, feed_dict = validate_feed)
                    print(global_step)
                    #print("After %s training step(s), validation accuracy = %f" % (global_step, accuracy_score))
                    return y_value
                else:
                    print("No checkpoint file found")
                    return


def main(argv=None):
    ax = []
    graph = []
    for i in range(20):
        graph.append(tf.Graph())
    for num in range(20):
        w_num = num+1
        train_data = np.load("train_data" + str(w_num) + ".npy")
        train_label = np.load("train_label" + str(w_num) + ".npy")
        global TRAIN_SIZE
        global TEST_SIZE
        global MODEL_SAVE_PATH
        TRAIN_SIZE = len(train_data)
        MODEL_SAVE_PATH = "model_1/model" + str(w_num) + "/"
        test_data = np.load("test_data" + str(w_num) + ".npy")
        test_label = np.load("test_label" + str(w_num) + ".npy")
        TEST_SIZE = len(test_data)
        # train(train_data, train_label, graph[num])

        predict_y = evaluate(test_data, MODEL_SAVE_PATH)
        average_dist = []
        predict_y_sub = predict_y[:, 0]
        test_label_sub = test_label[:, 0]
        diff = predict_y_sub - test_label_sub # Subtract element-wise
        squaredDiff = diff ** 2  # squared for the subtract
        distance = squaredDiff ** 0.5
        average_dist.append(np.mean(distance))
        average_test_label = np.mean(test_label_sub)
        print("wifi_number:", 0+1)
        print("max", np.max(distance))
        print("min", np.min(distance))
        print("average", average_dist[0])
        print("max", -np.max(distance) / average_test_label * 100, "%")
        print("min", -np.min(distance) / average_test_label * 100, "%")
        print("average", -average_dist[0] / average_test_label * 100, "%")
        print("\n")

        ax.append(plt.figure().add_subplot(111, projection='3d'))
        ax[num].scatter(test_data[:, 0], test_data[:, 1], test_label_sub, c='r')
        ax[num].scatter(test_data[:, 0], test_data[:, 1], predict_y_sub, c='g')
        ax[num].set_zlabel('Z')  # 坐标轴
        ax[num].set_ylabel('Y')
        ax[num].set_xlabel('X')
        ax[num].legend(['TestingData', 'Predict'])
    plt.show()


if __name__ == '__main__':
    tf.app.run()
