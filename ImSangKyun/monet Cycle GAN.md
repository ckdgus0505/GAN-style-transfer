# Monet Cycle GAN 정리

Monet Cycle GAN Tutorial : [https://www.kaggle.com/amyjang/monet-cyclegan-tutorial](https://www.kaggle.com/amyjang/monet-cyclegan-tutorial)
해당 내용의 이론 및 원리를 해석 및 정리하였습니다

# Import

```python
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import tensorflow_addons as tfa

from kaggle_datasets import KaggleDatasets
import matplotlib.pyplot as plt
import numpy as np

try:
    tpu = tf.distribute.cluster_resolver.TPUClusterResolver()
    print('Device:', tpu.master())
    tf.config.experimental_connect_to_cluster(tpu)
    tf.tpu.experimental.initialize_tpu_system(tpu)
    strategy = tf.distribute.experimental.TPUStrategy(tpu)
except:
    strategy = tf.distribute.get_strategy()
print('Number of replicas:', strategy.num_replicas_in_sync)

AUTOTUNE = tf.data.experimental.AUTOTUNE
    
print(tf.__version__)
```

Kaggle Tutorial 에서는 Tensorflow와 Google Corab을 이용한것으로 파악되며 일부 함수 및 메소드는 google corab과 연동되는 부분이 있어 이부분은 제거해야합니다.

TPU란? : Google Cloud의 Tensor Processing Unit의 약자로 Google 제품을 지원하는 커스텀 머신러닝 ASIC이다.

tf.distribute.cluster_resolver.TPUClusterResolver() : Cluster Resolver for Google Cloud TPUS.

tf.config.experimental_connect_to_cluster(tpu) : 할당된(주어진) 클러스터에 연결

tf.tpu.experimental.initialize_tpu_system(tpu) : TPU 디바이스 초기화

tf.distribute.experimental.TPUStrategy(tpu) : TPU들과 TPU Pod들과 동기화

즉 Google Cloud와 연동되는 함수들로 우리는 이 함수들을 사용할 필요는 없다.

```python

```

# Load Data

```python
GCS_PATH = KaggleDatasets().get_gcs_path()
MONET_FILENAMES = tf.io.gfile.glob(str(GCS_PATH + '/monet_tfrec/*.tfrec'))
print('Monet TFRecord Files:', len(MONET_FILENAMES))

PHOTO_FILENAMES = tf.io.gfile.glob(str(GCS_PATH + '/photo_tfrec/*.tfrec'))
print('Photo TFRecord Files:', len(PHOTO_FILENAMES))
```


두번째 줄의 keras.initializers.RandomNormal(mean=0.0, stddev=0.02) 이 또한 normaldistribution을 생성하는 코드인데 왜 두개를 따로따로 만들었는지는 아직 모르겠다. return된 tensor의 타입이 다른것인지는 나중에 확인해볼 필요가 있음

result = keras.Sequential() : Sequential 모델 생성

resual.add(layers.Conv2D(.....)) : tf.keras.layers.Conv2D는 2D convolution layer를 생성하는 함수이다. 

EX)

```python
tf.keras.layers.Conv2D(
    filters, kernel_size, strides=(1, 1), padding='valid', data_format=None,
    dilation_rate=(1, 1), groups=1, activation=None, use_bias=True,
    kernel_initializer='glorot_uniform', bias_initializer='zeros',
    kernel_regularizer=None, bias_regularizer=None, activity_regularizer=None,
    kernel_constraint=None, bias_constraint=None, **kwargs
)
```

![./etc/Keras Conv2D Params.PNG](./etc/Keras Conv2D Params.PNG)

