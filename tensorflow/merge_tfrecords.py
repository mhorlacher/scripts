#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import argparse


# In[ ]:


import tensorflow as tf


# In[ ]:


parser = argparse.ArgumentParser()
parser.add_argument('tfrecords', metavar='<in.tfrecord>', nargs='+')
parser.add_argument('-o', '--output', metavar='out.tfrecord', default='merged.tfrecord')
parser.add_argument('--shuffle', default=-1, type=int)
parser.add_argument('--interleave', action='store_true', default=False)
args = parser.parse_args()


# In[ ]:


@tf.function
def _load_tfrecord_dataset(filepath):
    return tf.data.TFRecordDataset(filepath)


# In[ ]:


with tf.io.TFRecordWriter(args.output) as tfwriter:
    if args.interleave:
        dataset = tf.data.Dataset.from_tensor_slices(args.tfrecords)
        dataset = dataset.interleave(_load_tfrecord_dataset, cycle_length=len(args.tfrecords))
    else:
        dataset = tf.data.TFRecordDataset(args.tfrecords)
    
    if args.shuffle:
        dataset = dataset.shuffle(args.shuffle)
    
    for raw_record in dataset:
        tfwriter.write(raw_record.numpy())


# In[ ]:




