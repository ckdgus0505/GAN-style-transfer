# Generative Adversarial Network  

## GAN이란?  
- Generative Adversarial Network의 약자로 Generator가 경쟁적으로 대립 (Adversarial)시켜 학습을 시키는 신경망을 말한다.  

### Generative  
- Gererator가 **그럴듯한 가짜 데이터**를 만들어내는 내는 모델.  
- '그럴듯한 가짜'라는 것은 실제 data의 분포와 비슷한 데이터를 만들어 낸다는 소리.  

### Adversarial  
- GAN이 두 개의 Model을 적대적으로 경쟁시키면 발전시킴.  

### Example   

![image](https://user-images.githubusercontent.com/32921115/104803734-88a46f00-5814-11eb-9e61-efbd1100e176.png)

- Generator : 위조지폐범, 목표는 그럴듯한 위조지폐를 만들어 Discriminator(경찰)을 속이는 것  
- Discriminator : 경찰, 목표는 진짜 지폐와 위조지폐를 구분하는 것  
- 이 둘을 계속 learning 시키면 언젠가는 진짜 지폐와 다를 것 없는 가짜 지폐를 만들어내는 Generator를 얻을 수 있음. (Adversarial Training)  

## 아키텍처  

![image](https://user-images.githubusercontent.com/32921115/104805680-39127300-5815-11eb-90b6-ddb1310943e5.png)

## Loss Function  

![image](https://user-images.githubusercontent.com/32921115/104805727-91497500-5815-11eb-947f-69a20e9f23f0.png)

### Discriminator
- 왼쪽 항 : D(x)는 실제 데이터 x를 보고 판별하는 예측 확률값. log는 0에서 1로 향할수록 값이 커지므로, **왼쪽 항은 Discriminator 입장에서는 값이 크면 좋음.**  
- 오른쪽 항 : D(G(z))는 Discriminator가 가짜 데이터를 보고 판별하는 예측 값. Discriminator는 진짜만 1, 가짜는 0으로 판별하고 싶어하므로 **0에 가까운 값을 출력해야 함.**, log(1-x) 함수는 0에서 1로 갈수록 값이 작아지므로, **오른쪽 항도 마찬가지로 값이 크면 좋음**  
- 즉, **Discriminator 입장에서 Loss Fucntion의 값이 커야 성능이 좋다고 말할 수 있음.**

### Generator  
- 오른쪽 항 : **Generator의 목표는 D(G(z))의 값이 1이 되게 만들어야 한다.** log(1-x) 함수는 0에서 1로 갈수록 값이 작아지므로, Generator 입장에서 **오른쪽 항의 값은 작아져야 한다.**  
- 즉, **Generator 입장에서 Loss Fucntion이 작은 값을 가져야 성능이 좋다고 말할 수있다.** 이는 곳 우리의 목적과 같음.  
- 맨 처음의 D(G(z))의 값은 0에 가까울 것 -> Loss가 큼.  
