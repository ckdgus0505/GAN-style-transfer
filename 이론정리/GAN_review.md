# 논문 리뷰
# Ian J.Goodfellow, [Generative Adversarial Nets]

## 목차
0. Abstract
1. Introduction
2. Related work
3. Adversarial nets
4. Theoretical Results
5. Experiments
6. Advantages and disadvantages
7. Conclusions and future work

## 논문리뷰에 앞서 알아둬야 할 함수, 변수, 기호
### D : 판별 모델
- output : 0~1 하나의 값으로 스칼라에 해당
### G : 생성 모델
- output: 확률
### p :   확률 분포
- p(z) : z 입력 시, 해당 변수의 분포를 나타냄
### θ : paremeter(weight)
- θg : 생성 모델 가중치
- θd : 판별 모델 가중치
###  z : random seeds


## 0. Abstract
: 동시에 두 모델을 학습하는 adversarial process를 통해 생성모델을 평가 하는 새로운 프레임워크를 제시

### What are models in G and D

1. generative model G  : 생성 모델
- captures the data distribution
- discriminative model D 
- The training procedure G 
: maximize the probability of D making a mistake
- output: 확률

2. discriminative model D : 판별 모델 
- estimates the probability that a sample came from the training data rather than G
- output : 0~1 하나의 값으로 스칼라에 해당

### Unique solution has exists

- Let's suppose that has In the space of arbitrary functions G and D 
- G recovering the training data dirstibution
- D equal to 1/2 everywhere
- G and D are defined by multilayer perceptrons
- the entire system can be trained with backpropagation

### GAN's properties

- no need for any Markov chains or unrolled approximate inference networks during training or generation of samples
- demostrate the potential of the framework through qualitative & quantitative evalutaion of the generated samples

### 한글 총 요약 
: GAN은 동시에 두 가지의 모델을 학습해야 하는데 생성 모델과, 판별 모델 두 모델이다.
생성 모델은 데이터의 분포를 파악하고, 판별 모델은 들어온 샘플이 생성모델에서 나오지 않았을 확률을 반환한다.
즉, 진짜인지 만들어진 가짜인지 파악하는 것이다.
생성 모델은 판별모델이 최소화되도록 학습한다.
학습이 완료되면 모든 데이터 분포에서 판별모델의 결과가 1/2가 나온다
즉, 진짜인지 가짜인지의 확률이 1/2에 해당한다

## 3. Adversarial nets

### Property  of Adversatial nets 
- most straightforward to apply when the models are both mutilayer perceptrons

### What is Adversarial nets

1. To learn the generator's distribution p.g over data x
- First, we define a prior on input noise variable p.z(z)
-  p.z(z) : 노이즈 확률분포로 해당 분포에서 노이즈 샘플인 z를 추출해서 생성 모델에 입력값으로 넣음
- Then represent a mapping to data space as G(z; θg)
- G(z; θg) : 생성 모델의 가중치가 θg일 때, 인풋으로 노이즈를 넣고 나온 결과
: what is G? differentiable function represented by a multilayer perceptron with parameters θg
- Second, we define a second multilayer perceptron D(x; θd)
-  D(x; θd) : 판별 모델의 가중치가  θd 일 때, 인풋으로 x를 넣은 결과
- D's output is a single scalar
- D(x) represents the probability that x came from the data rather than p.g
- And, We train D to maximize the probability of assigning the correct label to both training examples and samples from G
- Simultaneously train G to minimize log(1 − D(G(z))) 
: In other words, D and G play the following two-player minimax game with value function V (G, D)
- Here is expression of  V (G, D),
**min(G) max(D) V (D, G) = Ex∼pdata(x) [log D(x)] + Ez∼pz(z) [log(1 − D(G(z)))]**
- Next, present a theoretical analysis of adversarial nets
- the training criterion allows one to recover the data generating distribution G and D are given enough capacity in the non-parametric limit

### 한글요약
- GAN을 구현하는 가장 직접적인 방법은 판별, 생성 모델 모두 mlp를 이용해서 구현하는 것이다.
- 데이터 x에 대한 생성자의 분포 p.g를 학습하기 위해서 p.z(z)를 정의해야 한다. 이후 G(z; θg)로 표현되는 데이터 스페이스에 매핑을 나타낸다. 또한 두 번째 모델  D(x; θd)를 정의한다. D(x)는 x가 p.g에서 나오지 않았을 확률을 나타낸다.
- G에서 나오는 샘플들에 옳은 라벨을 붙일 확률을 높이도록 D를 학습해야 한다. 동시에 G는 log(1 − D(G(z))) 가 최소가 되게 해야 한다

## 4. Theroical Results
: The generator G implicitly defines a probability distribution pg as the distribution of the samples
G(z) obtained when z ∼ p.z

### Algorithm 1
- Algorithm 1 to converge to a good estimator of P.data, if given enough capacity and training time
- Minibatch stochastic gradient descent training of generative adversarial nets. 
- The number of steps to apply to the discriminator, k, is a hyperparameter. 
- In our experiments, we used k = 1, the least expensive option

### 4.1 Global Optimality of P.g = P.data
- 어떠한 G에 대해서도 잘 구분해내는 최적의 D를 가정하자.
- Proposition 1. G가 고정이면 최적의 D는 **D.G(x) = p.data(x)/ p.data(x) + p.g(x)** 이다

## 4.2 Convergence of Algorithm1
-   만약 생성모델, 판별 모델이 충분한 수용성이 있다면(학습이 잘 된다면), 알고리즘1의 매 단계에서 discriminator는 주어진 생성모델에 대하여 최적에 도달하고 p.g는 다음의 식을 향상시키기 위하여 업데이트 되어 p.g는 p.data로 수렴한다(p.g = p.data)
- **Ex∼pdata [log D∗G(x)] + Ex∼pg[log(1 − D∗G(x))]**

## 6. Advantages and disadvantages
### Advantages
- 생성모델의 분포 p.g(x)를 명시하지 않는다
- 따라서 학습하는 동안 판별모델은 생성모델과 잘 동기화(synchronize)되어야 한다
- 판별모델이 충분히 학습되기 전에 생성모델이 너무 많이 학습되면 안된다
### Disadvantages
- markov chain이 필요 없고, backpropagation만으로 학습이 가능하다.
- markov chain이란? 현재의 사건이 이전 사건에 영향을 받는다
- 학습하는데 inference는 필요하지 않음


