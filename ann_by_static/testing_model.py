import tensorflow as tf
import numpy as np
import pickle, os, json, warnings, logging
import datetime

from settings import *

# for using tensorflow as hyper parameter
INPUT_SIZE = 12288
OUTPUT_SIZE = 2

RESULT = [ False, True ]

def run( path ) :
    if not os.path.exists(TEST_RESULT_PATH) :
        os.makedirs(TEST_RESULT_PATH)
    warnings.filterwarnings('ignore')
    logger = logging.getLogger()
    logger.disabled = True

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
        model_saver.restore(sess, CHECK_POINT)
        with open(path, 'rb') as f :
            fh_vector = pickle.load(f)
        output = np.array(sess.run(y_test, feed_dict={x: [fh_vector]})).reshape([-1])
        malware_score = int(output[-1] * 100)
        detected=RESULT[int(output.argmax(-1))]
        md5 = os.path.splitext(os.path.basename(path))[0]
        result_dict = { 'md5' : md5, 'detected' : detected, 'label' : 'None', 'score' : malware_score, 'collected_date': datetime.datetime.now()}
        with open(os.path.join(TEST_RESULT_PATH, md5 + '.json'), 'w') as f :
            json.dump(result_dict, f)