#!/usr/bin/env python
# coding: utf-8

# In[25]:


import argparse
import re


# In[ ]:


import tensorflow as tf


# In[ ]:


parser = argparse.ArgumentParser()
parser.add_argument('tfrecord', metavar='<in.tfrecord>')
parser.add_argument('-o', '--output', metavar='<out.tfrecord>', default='subset.tfrecord')
parser.add_argument('-f', '--field-name')
parser.add_argument('-t', '--feature-type', default='string', help="One of ['string/bytes', 'int', 'float']")
parser.add_argument('-r', '--regex')
parser.add_argument('-v', '--inverse', action='store_true', default=False)
args = parser.parse_args()


# In[ ]:


if args.feature_type in ['string', 'bytes']:
    feature_description = {args.field_name: tf.io.FixedLenFeature([], tf.string, default_value='')}
elif args.feature_type == 'int':
    feature_description = {args.field_name: tf.io.FixedLenFeature([], tf.int64, default_value=-1)}
elif args.feature_type == 'float':
    feature_description = {args.field_name: tf.io.FixedLenFeature([], tf.float32, default_value=-1.0)}
else:
    raise ValueError("Feature type has to be one in ['string', 'bytes', 'int', 'float']")


# In[ ]:


def check_record(example_proto):
    # parse the input `tf.train.Example` proto using the dictionary above.
    parsed_example = tf.io.parse_single_example(example_proto, feature_description)
    
    if args.feature_type in ['string', 'bytes']: 
        target_string_field = parsed_example[args.field_name].numpy().decode('UTF-8')
    elif args.feature_type in ['int', 'float']:
        target_string_field = str(parsed_example[args.field_name].numpy())
    
    is_match = bool(re.search(args.regex, target_string_field))
    if args.inverse:
        is_match = not is_match

    return is_match


# In[ ]:


with tf.io.TFRecordWriter(args.output) as tfwriter:
    dataset = tf.data.TFRecordDataset(args.tfrecord)
    for raw_record in dataset:
        if check_record(raw_record):
            tfwriter.write(raw_record.numpy())

