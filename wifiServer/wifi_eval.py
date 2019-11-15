#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn import svm

# 加载FR_inference.py 和 FR_train.py中定义的常量和函数
import wifi_inference
import wifi_train




def evaluate(test_data, MODEL_SAVE_PATH):
    TEST_SIZE=len(test_data)
    with tf.Graph().as_default() as g:
        # 定义输入输出的格式

        x = tf.placeholder(tf.float32, [
            TEST_SIZE,          # 第一维表示样例的个数
            wifi_inference.INPUT_NODE],          # 第四维表示图片的深度，对于RBG格式的图片，深度为5
                       name='x-input')

        validate_feed = {x: np.reshape(test_data, (TEST_SIZE, wifi_inference.INPUT_NODE))}
        # 直接通过调用封装好的函数来计算前向传播的结果。
        # 因为测试时不关注正则损失的值，所以这里用于计算正则化损失的函数被设置为None。
        y = wifi_inference.inference(x, False, None)

        # 使用前向传播的结果计算正确率。
        # 如果需要对未知的样例进行分类，那么使用tf.argmax(y, 1)就可以得到输入样例的预测类别了。


        # 通过变量重命名的方式来加载模型，这样在前向传播的过程中就不需要调用求滑动平均的函数来获取平局值了。
        # 这样就可以完全共用FR_inference.py中定义的前向传播过程
        variable_averages = tf.train.ExponentialMovingAverage(wifi_train.MOVING_AVERAGE_DECAY)
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
            #time.sleep(EVAL_INTERVAL_SECS)



def main(argv=None):
    test_data = np.load("test_data.npy")
    test_label = np.load("test_label.npy")

    predict_y = evaluate(test_data, wifi_train.MODEL_SAVE_PATH)
    print(np.shape(predict_y))
    ax = []
    average_dist = []
    for i in range(20):
        predict_y_sub = predict_y[:, i]
        test_label_sub = test_label[:, i]
        diff = predict_y_sub - test_label_sub # Subtract element-wise
        squaredDiff = diff ** 2  # squared for the subtract
        distance = squaredDiff ** 0.5
        average_dist.append(np.mean(distance))
        average_test_label = np.mean(test_label_sub)
        print("wifi_number:", i+1)
        print("max", np.max(distance))
        print("min", np.min(distance))
        print("average", average_dist[i])
        print("max", -np.max(distance) / average_test_label * 100, "%")
        print("min", -np.min(distance) / average_test_label * 100, "%")
        print("average", -average_dist[i] / average_test_label * 100, "%")
        print("\n")

        # train_data = np.load("train_data.npy")
        # train_label = np.load("train_label.npy")
        # train_label_1 = []
        # for i in range(len(train_label)):
        #     temp = []
        #     temp.append(train_label[i][0])
        #     train_label_1.append(temp)
        ax.append(plt.figure().add_subplot(111, projection='3d'))
        # ax[0].scatter(train_data[:, 0], train_data[:, 1], train_label_1, c='y')
        ax[i].scatter(test_data[:, 0], test_data[:, 1], test_label_sub, c='r')
        ax[i].scatter(test_data[:, 0], test_data[:, 1], predict_y_sub, c='g')
        ax[i].set_zlabel('Z')  # 坐标轴
        ax[i].set_ylabel('Y')
        ax[i].set_xlabel('X')
        # ax[0].legend(['TrainingData', 'TestingData','Predict'])
        ax[i].legend(['TestingData', 'Predict'])
    plt.show()

if __name__ == '__main__':
    tf.app.run()