import tensorflow as tf
import numpy as np
import pickle, os
import ssdeep
from settings import *

# for using tensorflow as hyper parameter
INPUT_SIZE = 12288
OUTPUT_SIZE = 7
LEARNING_RATE = 1e-4
BATCH_SIZE = 128 # 몇 문제를 동시에 풀지
EPOCH = 40000 # 문제를 얼마나 풀지
DROPOUT_PROB = 0.7

LABEL_TO_INT = { 'Virus' : 0 , 'Worm' : 1, 'Trojan' : 2, 'not-a-virus:Downloader' : 3, 'Rootkit' : 4, 'Trojan-Ransom' : 5, 'Backdoor' : 6}

def load_data():
    print('Data Loding starts')
    csv_data = np.loadtxt(TRAIN_LABEL_PATH, delimiter=',', dtype=np.str)
    x_data = csv_data[:, [0]]
    y_data = csv_data[:, [2]]
    mal_data = [ [] for i in range(7) ]
    cnt = 0
    for md5, label in zip(x_data, y_data) :
        md5[0] = md5[0].replace('.vir','')
        full_path = os.path.join(TRAIN_STATIC_DATA_PATH, md5[0] + '.fhfops')
        try :
            with open(full_path, 'rb') as f :
                fh_vector = pickle.load(f)
            try :
                mal_data[LABEL_TO_INT[label[0]]].append(fh_vector)
                cnt += 1
            except :
                pass
        except :
            pass


    print('{CNT} Data reading finished'.format(CNT = cnt))

    return mal_data

def get_batch(mal_data_list):
    while True:
        batch_data_list = []
        batch_label_list = []
        for i in range(len(mal_data_list)) :
            np.random.shuffle(mal_data_list[i])
            group_list = [ 0 for i in range(7) ]
            group_list[i] = 1
            if len(mal_data_list[i]) >= BATCH_SIZE :
                batch_data_list += mal_data_list[i][:BATCH_SIZE]
                batch_label_list += [ group_list for i in range(BATCH_SIZE) ]
        yield (batch_data_list, batch_label_list)

def run() :
    print("Train Multi Classification")
    mal_data_list = load_data()

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
    train_iter = get_batch(mal_data_list)

    with tf.Session(config=tf.ConfigProto(allow_soft_placement=True, log_device_placement=True)) as sess:
        sess.run(init)
        try :
            model_saver.restore(sess, STATIC_MC_CHECK_POINT)
        except :
            pass
        print('learning start')
        for i in range(EPOCH):
            (training_data, training_label) = next(train_iter)
            sess.run(optimizer, feed_dict={x: training_data, y: training_label, prob: DROPOUT_PROB})
            if (i % 100 == 0):
                print(i, sess.run(accuracy, feed_dict={x: training_data, y: training_label, prob: DROPOUT_PROB}))
                if (i % 1000 == 0):
                    model_saver.save(sess, STATIC_MC_CHECK_POINT)
        print('------finish------')
        model_saver.save(sess, STATIC_MC_CHECK_POINT)

if __name__ == '__main__' :
    run()