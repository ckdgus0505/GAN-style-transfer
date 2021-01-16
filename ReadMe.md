# GAN Style Transfer


# project about
이 프로젝트는 GAN을 이용하여 사진의 style을 여러 화가들의 화풍으로 변경해주는것을 목표로 하는 프로젝트 입니다. 처음에는 GAN을 이용하여 그 결과물을 단기간동안 web으로 서비스 할 예정이고, 이후에는 모델에 GAN의 variation을 적용하여서 학습 효율을 높이는 작업을 할 예정입니다. 

This project is about style transfer which converts the style of the photo to other painter's styles using GAN. At first, we serve the output of GAN using the web temporarily. After that, we apply GAN's variation to make the model more works well.

# 프로젝트 요약
Cycle GAN을 이용하여 paired data가 없이도 학습이 가능하도록 하였습니다.

Cycle GAN 의 Generator에는 U-Net, Discriminator 에는 fully connected layer을 적용하였고,
미국의 tv 애니메이션인 The simpsons 의 스타일을 학습하여
input 영상을 simpson 풍의 영상으로 변환하여 출력해줍니다.

# Team Name : GAN때문이야

## Member
|소속|이름  | 비고|
|--|--|--|
|컴퓨터 과학과|정창현|팀장, 모델 설계|
|컴퓨터 과학과|임상균|모델 설계|
|컴퓨터 과학과|홍우기||
|휴먼지능정보학과|추희승|데이터 관련 프로그램 설계|
|컴퓨터 과학과|강대훈|데이터 관련 프로그램 설계|
|컴퓨터 과학과|안지민|모델 설계|

## 모델
[/model](./model)

# 프로젝트 결과
> original

![original](./images/original.gif)


> converted

![converted](./images/converted.gif)


---
# 참고자료

- [Generative Adversarial Nets](https://proceedings.neurips.cc/paper/2014/hash/5ca3e9b122f61f8f06494c97b1afccf3-Abstract.html)
-[Unpaired Image-To-Image Translation Using Cycle-Consistent Adversarial Networks](https://openaccess.thecvf.com/content_iccv_2017/html/Zhu_Unpaired_Image-To-Image_Translation_ICCV_2017_paper.html)
- [U-Net: Convolutional Networks for Biomedical Image Segmentation](https://link.springer.com/chapter/10.1007/978-3-319-24574-4_28)
- [Deep Residual Learning for Image Recognition](https://openaccess.thecvf.com/content_cvpr_2016/html/He_Deep_Residual_Learning_CVPR_2016_paper.html)
- [Cycle GAN Github](https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix)
- [Simpsons Homepage](https://www.fox.com/the-simpsons/)



