import tensorflow as tf
import numpy as np
import pickle, warnings, logging, sys

from settings import *

# for using tensorflow as hyper parameter
INPUT_SIZE = 12288
OUTPUT_SIZE = 7

LABEL = ['Virus', 'Worm', 'Trojan', 'Downloader', 'Rootkit', 'Ransomware', 'Backdoor' ]

def mc_run( feature_vector ) :
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
        print(DYNAMIC_MC_CHECK_POINT)
        model_saver.restore(sess, DYNAMIC_MC_CHECK_POINT)
        output = np.array(sess.run(y_test, feed_dict={x: [feature_vector]})).reshape([-1])
        group = {}
        for i in range(OUTPUT_SIZE) :
            group[i] = output[i]
        label=LABEL[int(output.argmax(-1))]
    return label, group

def load_data( file_path ) :
    with open(file_path, 'rb') as f :
        return pickle.load(f)
if __name__ == '__main__' :
    fh_path = sys.argv[1]
    feature_vector = load_data( fh_path )
    label, group = mc_run(feature_vector)
    print("{},{:.6f},{:.6f},{:.6f},{:.6f},{:.6f},{:.6f}".format(label, group[0], group[1], group[2], group[3], group[4], group[5], group[6]))