import tensorflow as tf
import numpy as np

x = tf.Variable(3.0)

with tf.GradientTape() as g :
    y = x * x

dy_dx = g.gradient(x,y)

print(dy_dx.numpy())