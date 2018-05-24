import tensorflow as tf
import numpy as np
import pickle

from settings import *

# for using tensorflow as hyper parameter
INPUT_SIZE = 12288
OUTPUT_SIZE = 7

def mc_run( feature_vector ) :
    tf.reset_default_graph()
    with tf.device('/gpu:0'):
        x = tf.placeholder(tf.float32, shape=[None, INPUT_SIZE])
        y = tf.placeholder(tf.float32, shape=[None, OUTPUT_SIZE])

        dense_layer_1 = tf.layers.dense(inputs=x, units=4096, activation=tf.nn.relu)
        dense_layer_2 = tf.layers.dense(inputs=dense_layer_1, units=1024, activation=tf.nn.relu)
        dense_layer_3 = tf.layers.dense(inputs=dense_layer_2, units=256, activation=tf.nn.relu)
        dense_layer_4 = tf.layers.dense(inputs=dense_layer_3, units=64, activation=tf.nn.relu)
        dense_layer_5 = tf.layers.dense(inputs=dense_layer_4, units=16, activation=tf.nn.relu)

        y_ = tf.layers.dense(inputs=dense_layer_5, units=OUTPUT_SIZE)
        y_test = tf.nn.softmax(y_)

    # testing session start
    model_saver = tf.train.Saver()
    init = tf.global_variables_initializer()

    tf_config = tf.ConfigProto(allow_soft_placement=True, log_device_placement=True)
    tf_config.gpu_options.allow_growth = True

    with tf.Session(config=tf.ConfigProto(allow_soft_placement=True, log_device_placement=True)) as sess:
        sess.run(init)
        print(DYNAMIC_MC_CHECK_POINT)
        model_saver.restore(sess, DYNAMIC_MC_CHECK_POINT)
        output = np.array(sess.run(y_test, feed_dict={x: [feature_vector]})).reshape([-1])
        group = []
        for i in range(OUTPUT_SIZE):
            group.append(int(output[i] * 100))
    return group

def load_data( file_path ) :
    with open(file_path, 'rb') as f :
        return pickle.load(f)

def run( file_path ) :
    feature_vector = load_data(file_path)
    return mc_run(feature_vector)