import warnings, logging

import tensorflow as tf
import numpy as np
import pickle, os

from settings import *

CHECK_POINT = os.path.normpath(os.path.abspath('./static_model.ckpt'))

# for using tensorflow as hyper parameter
INPUT_SIZE = 12288
OUTPUT_SIZE = 2
LEARNING_RATE = 1e-4
BATCH_SIZE = 256 # 몇 문제를 동시에 풀지
EPOCH = 40000 # 문제를 얼마나 풀지
DROPOUT_PROB = 0.7

def load_data():
    print('Data Loding starts')
    csv_data = np.loadtxt('train_data.csv', delimiter=',', dtype=np.str)

    x_data = csv_data[:, [0]]
    y_data = csv_data[:, [1]]

    ben_data_list = []
    mal_data_list = []

    for md5, detected in zip(x_data, y_data) :
        full_path = os.path.join(TRAIN_DATA_PATH, md5[0] + '.fh')

        with open(full_path, 'rb') as f :
            fh_vector = pickle.load(f)

        if detected == '1' :
            mal_data_list.append(fh_vector)
        else :
            ben_data_list.append(fh_vector)

    print('{CNT} Data reading finished'.format(CNT = len(ben_data_list) + len(mal_data_list)))

    return ben_data_list, mal_data_list

def get_batch(ben_data_list, mal_data_list):
    while True:
        np.random.shuffle(ben_data_list)
        np.random.shuffle(mal_data_list)

        half_batch_size = int(BATCH_SIZE / 2)
        batch_data_list, batch_label_list = [], []

        batch_data_list = ben_data_list[:half_batch_size] + mal_data_list[:half_batch_size]
        batch_label_list = [ [1, 0] for i in range(half_batch_size) ] + [ [0, 1] for i in range(half_batch_size) ]

        yield (batch_data_list, batch_label_list)

def run() :
    # 에러 메세지 제거
    warnings.filterwarnings('ignore')
    logger = logging.getLogger()
    logger.disabled = True

    tf.reset_default_graph()

    ben_data_list, mal_data_list = load_data()

    print('Load ANN network architecture')
    with tf.device('/gpu:0'):
        # ANN network architecture
        prob = tf.placeholder(tf.float32)

        x = tf.placeholder(tf.float32, shape=[None, INPUT_SIZE])
        y = tf.placeholder(tf.float32, shape=[None, OUTPUT_SIZE])

        dense_layer_1 = tf.layers.dense(inputs=x, units=4096, activation=tf.nn.relu)
        dense_drop_1 = tf.nn.dropout(dense_layer_1, prob)
        dense_layer_2 = tf.layers.dense(inputs=dense_drop_1, units=1024, activation=tf.nn.relu)
        dense_drop_2 = tf.nn.dropout(dense_layer_2, prob)
        dense_layer_3 = tf.layers.dense(inputs=dense_drop_2, units=256, activation=tf.nn.relu)
        dense_drop_3 = tf.nn.dropout(dense_layer_3, prob)
        dense_layer_4 = tf.layers.dense(inputs=dense_drop_3, units=64, activation=tf.nn.relu)
        dense_drop_4 = tf.nn.dropout(dense_layer_4, prob)
        dense_layer_5 = tf.layers.dense(inputs=dense_drop_4, units=16, activation=tf.nn.relu)
        dense_drop_5 = tf.nn.dropout(dense_layer_5, prob)

        y_ = tf.layers.dense(inputs=dense_drop_5, units=OUTPUT_SIZE)

        # loss function: softmax, cross-entropy
        cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=y_, labels=y))

        # optimizer: Adaptive momentum optimizer
        optimizer = tf.train.AdamOptimizer(LEARNING_RATE).minimize(cost)

    # predict
    prediction = tf.equal(tf.argmax(y_, 1), tf.argmax(y, 1))
    accuracy = tf.reduce_mean(tf.cast(prediction, tf.float32))

    print('Training session start')
    # training session start
    model_saver = tf.train.Saver()
    init = tf.global_variables_initializer()
    train_iter = get_batch(ben_data_list, mal_data_list)

    with tf.Session(config=tf.ConfigProto(allow_soft_placement=True, log_device_placement=True)) as sess:
        sess.run(init)
        if os.path.exists(CHECK_POINT) :
            model_saver.restore(sess, CHECK_POINT)
        print('learning start')
        for i in range(EPOCH):
            (training_data, training_label) = next(train_iter)
            sess.run(optimizer, feed_dict={x: training_data, y: training_label, prob: DROPOUT_PROB})
            if (i % 100 == 0):
                print(i, sess.run(accuracy, feed_dict={x: training_data, y: training_label, prob: DROPOUT_PROB}))
                if (i % 1000 == 0):
                    model_saver.save(sess, CHECK_POINT)
        print('------finish------')
        model_saver.save(sess, CHECK_POINT)
