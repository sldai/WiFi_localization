#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import tensorflow as tf
import evaluate


class NN_predict:
    def __init__(self, MODEL_SAVE_PATH):

        self.graph=tf.Graph()
        with self.graph.as_default():
            self.sess=tf.Session(graph=self.graph)
            ckpt = tf.train.get_checkpoint_state(MODEL_SAVE_PATH)
            if ((ckpt and ckpt.model_checkpoint_path) == 0):
                print("No checkpoint file found")
            self.x = tf.placeholder(tf.float32, [None, evaluate.INPUT_NODE], name='x-input')
            self.y = evaluate.inference(self.x, False, None)
            variable_averages = tf.train.ExponentialMovingAverage(evaluate.MOVING_AVERAGE_DECAY)
            variable_to_restore = variable_averages.variables_to_restore()
            self.saver = tf.train.Saver(variable_to_restore)
            self.saver.restore(self.sess, ckpt.model_checkpoint_path)

    def predict(self, test_data):
        with self.graph.as_default():
            y_value = self.sess.run(self.y, feed_dict={self.x: np.reshape(test_data, (len(test_data), evaluate.INPUT_NODE))})
        return y_value


def main(argv=None):
    test_data = [[10, 4]]
    pp = []
    predict_y = []
    for i in range(20):
        pp.append(NN_predict("model_1/model"+str(i+1)+"/"))
        print('OK!',i)
    for i in range(20):
        predict_y.append(pp[i].predict(test_data).tolist())
    print(predict_y)
    print(np.shape(predict_y))


if __name__ == '__main__':
    tf.app.run()