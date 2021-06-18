#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import argparse


# In[1]:


import tensorflow as tf


# In[ ]:


parser = argparse.ArgumentParser()
parser.add_argument('tfrecord', metavar='<in.tfrecord>')
parser.add_argument('-n', '--number', type=int, default=10)
parser.add_argument('-o', '--output', metavar='out.tfrecord', default='head.tfrecord')
args = parser.parse_args()


# In[ ]:


@tf.function
def _load_tfrecord_dataset(filepath):
    return tf.data.TFRecordDataset(filepath)


# In[ ]:


with tf.io.TFRecordWriter(args.output) as tfwriter:
    dataset = tf.data.TFRecordDataset([args.tfrecord])
    
    for i, raw_record in enumerate(dataset, start=1):
        tfwriter.write(raw_record.numpy())
        
        if i % args.number:
            break

