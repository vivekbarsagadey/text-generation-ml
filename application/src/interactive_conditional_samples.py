#!/usr/bin/env python3

import fire
import json
import os
import numpy as np
import tensorflow as tf
from application.src import model, sample, encoder

BASE_DIR = os.path.abspath(os.path.dirname(__name__))
out_text = []
def interact_model(input_data=""):
    """
    Interactively run the model
    :model_name=117M : String, which model to use
    :seed=None : Integer seed for random number generators, fix seed to reproduce
     results
    :nsamples=1 : Number of samples to return total
    :batch_size=1 : Number of batches (only affects speed/memory).  Must divide nsamples.
    :length=None : Number of tokens in generated text, if None (default), is
     determined by model hyperparameters
    :temperature=1 : Float value controlling randomness in boltzmann
     distribution. Lower temperature results in less random completions. As the
     temperature approaches zero, the model will become deterministic and
     repetitive. Higher temperature results in more random completions.
    :top_k=0 : Integer value controlling diversity. 1 means only 1 word is
     considered for each step (token), resulting in deterministic completions,
     while 40 means 40 words are considered at each step. 0 (default) is a
     special setting meaning no restrictions. 40 generally is a good value.
    :top_p=0.0 : Float value controlling diversity. Implements nucleus sampling,
     overriding top_k if set to a value > 0. A good setting is 0.9.
    """

    seed = None
    nsamples = 1
    batch_size = 1
    length = 0
    temperature = 1
    top_k = 40
    top_p = 0.0

    enc = encoder.get_encoder('117M')
    hparams = model.default_hparams()
    with open(os.path.join(BASE_DIR,'application\models', '117M', 'hparams.json')) as f:
        hparams.override_from_dict(json.load(f))

    len_hparams = hparams.n_ctx
    print(type(length))
    print(type(batch_size))
    if length == 0:
        length = hparams.n_ctx // 2
    # elif length > len_hparams:
    #     raise ValueError("Can't get samples longer than window size: %s" % len_hparams)

    with tf.Session(graph=tf.Graph()) as sess:
        context = tf.placeholder(tf.int32, [batch_size, None])
        np.random.seed(seed)
        tf.set_random_seed(seed)
        output = sample.sample_sequence(
            hparams=hparams, length=length,
            context=context,
            batch_size=batch_size,
            temperature=temperature, top_k=top_k, top_p=top_p
        )

        saver = tf.train.Saver()
        ckpt = tf.train.latest_checkpoint(os.path.join(BASE_DIR,'application\models', '117M'))
        saver.restore(sess, ckpt)


        raw_text = input_data
        context_tokens = enc.encode(raw_text)
        generated = 0
        for _ in range(nsamples // batch_size):
            out = sess.run(output, feed_dict={
                context: [context_tokens for _ in range(batch_size)]
            })[:, len(context_tokens):]
            for i in range(batch_size):
                    generated += 1
                    text = enc.decode(out[i])
                    print("=" * 40 + " SAMPLE " + str(generated) + " " + "=" * 40)
                    print(text)
            out_text.append(text)
    return out_text