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

```python
IMAGE_SIZE = [256, 256]

def decode_image(image):
    image = tf.image.decode_jpeg(image, channels=3)
    image = (tf.cast(image, tf.float32) / 127.5) - 1
    image = tf.reshape(image, [*IMAGE_SIZE, 3])
    return image

def read_tfrecord(example):
    tfrecord_format = {
        "image_name": tf.io.FixedLenFeature([], tf.string),
        "image": tf.io.FixedLenFeature([], tf.string),
        "target": tf.io.FixedLenFeature([], tf.string)
    }
    example = tf.io.parse_single_example(example, tfrecord_format)
    image = decode_image(example['image'])
    return image

def load_dataset(filenames, labeled=True, ordered=False):
    dataset = tf.data.TFRecordDataset(filenames)
    dataset = dataset.map(read_tfrecord, num_parallel_calls=AUTOTUNE)
    return dataset

monet_ds = load_dataset(MONET_FILENAMES, labeled=True).batch(1)
photo_ds = load_dataset(PHOTO_FILENAMES, labeled=True).batch(1)
```

KaggleDatasets().get_gcs_path() : 공식 docs를 확인하지는 못하였으나 Kaggle에 업로드해둔 데이터셋을 이용하기위한 API로 확인하였다

우리는 로컬 컴퓨터에 데이터셋을 모아둔 뒤 학습시킬 예정이므로 해당 함수는 제거하고 로컬경로를 써주면 될 것이다.

이후 IMAGE_SIZE = [256, 256]을 통해 image size는 256X256 으로 다룰것임을 확인할 수 있고, RGB값으로 인해 channel=3 을 사용한다.

위의 decode_image와 read_tfrecord, load_dataset은 tensorflow의 tfrec 라는 파일을 이용하여 데이터를 불러오는 방식이므로 우리는 이를 눈여겨 볼 필요는 없다.

pytorch로 번역한 코드는 아래와 같다.

```python
import torch
from torchvision import datasets, transforms

data_dir = '../Datasets/Kaggle Monet Image'
transform = transforms.Compose([transforms.Resize(255), transforms.CenterCrop(224), transforms.ToTensor()])
monet_dataset = datasets.ImageFolder(str(data_dir + '/monet_jpg/'), transform=transform)
photo_dataset = datasets.ImageFolder(str(data_dir + '/photo_jpg'), transform=transform)
monet_dl = torch.utils.data.DataLoader(monet_dataset, batch_size=128, shuffle=True, num_workers=2)
photo_dl = torch.utils.data.DataLoader(photo_dataset, batch_size=128, shuffle=True, num_workers=2)
```

# Build the Generator

```python
OUTPUT_CHANNELS = 3

def downsample(filters, size, apply_instancenorm=True):
    initializer = tf.random_normal_initializer(0., 0.02)
    gamma_init = keras.initializers.RandomNormal(mean=0.0, stddev=0.02)

    result = keras.Sequential()
    result.add(layers.Conv2D(filters, size, strides=2, padding='same',
                             kernel_initializer=initializer, use_bias=False))

    if apply_instancenorm:
        result.add(tfa.layers.InstanceNormalization(gamma_initializer=gamma_init))

    result.add(layers.LeakyReLU())

    return result
```

tf.random_normal_initializer(0., 0.02) : normal distribution(정규분포)으로 초기화된 tensor를 생성하는 코드로

EX) tf.random_normal_initizlizer(mean=0.0, stddev=0.05, seed=None)

mean : a python scalar or a scalar tensor. Mean of the random values to generate

stddev : a python scalar or a scalar tensor. Standard deviation of the random values to generate

seed : A Python integer. Used to create random seeds.
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

![./etc/Keras Conv2D Params.PNG](https://github.com/ckdgus0505/GAN-style-transfer/blob/master/ImSangKyun/etc/Keras%20Conv2D%20Params.PNG)

