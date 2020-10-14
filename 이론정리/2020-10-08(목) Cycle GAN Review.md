# Cycle GAN

[Monet CycleGAN Tutorial](https://www.kaggle.com/amyjang/monet-cyclegan-tutorial)

[0]

Cycle Gan 의 Cycle은 generator 가 2개 있어서,
Generator1으로 만들어 낸 이미지를 Generator2를 이용해서 다시 input image 처럼 되돌리는
과정을 cycle 이라고 하고, 이를 discriminator을 이용하여 loss 를 계산해서 더욱 정교한 이미지로
만들어주는데 GAN을 이용하기 때문에 Cycle Gan 이라는 이름이 생겼다.

![Cycle%20GAN%20b8c0232a79c4443eba74b3e1b8369bb4/687474703a2f2f6572696b6c696e6465726e6f72656e2e73652f696d616765732f6379636c6567616e2e706e67.png](Cycle%20GAN%20b8c0232a79c4443eba74b3e1b8369bb4/687474703a2f2f6572696b6c696e6465726e6f72656e2e73652f696d616765732f6379636c6567616e2e706e67.png)

# 그림 1 Cycle gan 구조

[9]

Generator 을 Unet 을 이용하여서 만들었다고 한다.

Unet 은 이미지 세그멘테이션 작업을 수행하기 위해서 만들어진 모델이다.
이미지 세그멘테이션은 예를들어 항공 사진을 가지고 도로, 건물, 공원 등으로 구획화 시키는것이다.

Generator 로 Unet 을 사용한것은 원하는 이미지를 구획화 하여 그 부분에 대해서 각각
sytle transfer 를 시키기 위함으로 보인다.

Unet 의 대표적인 기술 중 skip-connection을 설명을 해야할 차례다.

이는 한 layer 의 output이 대응되는 layer 에 또다른 input 으로 들어가는 것이다.

![Cycle%20GAN%20b8c0232a79c4443eba74b3e1b8369bb4/main-qimg-d5a93e82cb553c7d6db9b0b46a4a56d4.png](Cycle%20GAN%20b8c0232a79c4443eba74b3e1b8369bb4/main-qimg-d5a93e82cb553c7d6db9b0b46a4a56d4.png)

# 그림 2 Unet 구조

그림2의 회색 선이 skip connection 을 설명하는 그림이다.

이외의 과정은 단순한 convolution, Transposed convolution 과정과 일치한다.

[11]

Generator 은 그림2를 다 수행한 모습이다

[12]

Discriminator은 그림2에서 왼쪽 절반만 시용하여 재구성(reconstruction)을 하지 않고, 스칼라 값만을 출력하도록 만들었다.

[13]

11,12에서 정의한 generator, discriminator을 2개씩 만들었다.

하나는 모네 제너레이터 ( 사진을 모네풍으로 변환)

또다른 하나는 포토 제너레이터 (모네풍의 사진을 다시 사진으로 변환)

또다른 하나는 모네 디스크리미네이터 ( 모네풍으로 변환된 사진이 얼마나 사실같은지 (모네가 직접 그린것 같은지)

마지막 하나는 포토 디스크리미네이터 (모네의 그림을 사진처럼 변환시킨 사진이 얼마나 진짜 사진 같은지)

그림1의 Generator, Discriminator 이 모두 마련되었다.

![Cycle%20GAN%20b8c0232a79c4443eba74b3e1b8369bb4/cyclegan_loss.jpg](Cycle%20GAN%20b8c0232a79c4443eba74b3e1b8369bb4/cyclegan_loss.jpg)

그림3, cycle gan 모델 구조

 [15]

Generator, Discriminator로 Cycle GAN 구조를 정의해보자

model 안에는 2개의 generator, 2개의 discriminator가 존재한다. 

m_gen, m_disc, p_gen, p_disc

m_gen으로 일반 사진을 모네 화풍의 그림으로 바꾼것(fake_monet)을 p_gen을 이용하여 다시 일반 사진(cycled_photo)으로 바꾼다.

마찬가지로, 모네의 그림을  p_gen에 넣어 가짜 사진(fake_photo)으로 만들고, 다시 가짜 사진을 m_gen에 넣어 모네 그림(cycled_monet)으로 변경한다.

또한, 모네의 사진을 m_gen에 넣어 모네의 사진 그대로(same monet)를 출력하길 기대해본다. 

사진을 p_gen에 넣어 일반 사진 그대로(same photo)를 출력하길 기대해본다.

m_disc 는 real_monet 와 fake monet 을 각각 판단하여 결과를 내놓는다. (각각, disc_real_monet, disc_fake_monet)

또한 p_disc는 real_photo 와 fake_photo를 각각 판단하여 결과를 내놓는다. (각각, disc_real_photo, disc_fake_photo)

이제, 이것들의 loss 를 계산한다. 

total generator loss 는 gen loss +  cycle loss + identity loss의 합으로 이루어진다.

cycle_loss_fn ⇒ real_image, cycled_image의 값을 1:1로 비교하여 평균을 내어 구한다. 

identity_loss_fn ⇒ real_image , same_image의 값을 1:1로 비교하여 평균을 내어 구한다. 

gen_loss_fn ⇒ disc_fake_monet 로 값을 구함 

disc_loss_fn(discriminator_loss) ⇒ discriminator를 위한 loss function, disc_real_monet, disc, fake_monet을 input으로 받아 monet_disc_loss를 출력
disc_real_photo, disc_fake_photo를 input으로 받아 photo_disc_loss를 출력

(real 과 fake 를 비교하여 loss 를 내놓는다.)

을 사용한다. 

[16 ~ 19]

loss 를 정의해야 한다. 

[16]은 discriminator 을 학습시킬때 필요한 loss

[17]은 generator을 학습시킬때 필요한 loss, 

[18]은 cycle loss (변환이 얼마나 잘되었는지를 나타냄, real_image, cycled_image의 값을 1:1로 비교하여 평균을 내어 구한다

[19]는 identity loss ( 변환을 한 이미지를 다시 변환하였을때 얼마나 원본과 같은지의 loss), real_image , same_image의 값을 1:1로 비교하여 평균을 내어 구한다. 

[20]

learning rate와, optimizer을 정의해주고 

[21]

정의한 모델을 생성하고

[22] 학습한다.