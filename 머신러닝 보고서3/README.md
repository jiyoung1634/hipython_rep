# 🚗 중고차 가격 예측 모델 보고서

---

## 📂 프로젝트 개요

이 프로젝트는 중고차 시장 데이터를 활용해 **중고차 가격을 예측하는 회귀 모델을 개발**하고, 다양한 머신러닝 모델의 성능을 비교 분석합니다.

**목표**: 최적의 중고차 가격 예측 모델을 선정합니다.
---

## 🗂️ 데이터셋

- 주요 변수:
  - `title`: 중고차 매물 게시물 제목
  - `price_in_aed`: 해당 중고차 매물의 가격 -> 예측 목표 변수
  - `kilometers`: 해당 중고차가 주행한 총 주행 거리
  - `body_condition`: 차량 외관의 상태
  - `mechanical_condition`: 차량 내부 기계적인 상태
  - `seller_type`: 차량을 판매하는 판매자의 종류 
  - `body_type`: 차량의 차체 형태
  - `no_of_cylinders`: 차량 엔진의 실린더 개수
  - `transmission_type`: 차량의 변속기 종류
  - `regional_specs` : 차량이 어떤 지역 규격에 맞춰져 있는지 나타냄
  - `horsepower` : 차량 엔진의 마력
  - `fuel_type`: 차량의 연료 종류
  - `steering_side`: 차량 운전석의 스티어링 휠 위치
  - `year`: 차량의 제조 연도
  - `color`: 차량의 외관 색상
  - `emirate`: 차량 매물이 위치한 아랍에미리트의 토후국(emirate)
  - `motors_trim`: 차량 모델 내의 특정 트림(Trim) 또는 세부 모델명
  - `company`: : 차량의 제조사 (브랜드)
  - `model`: 차량의 모델명
  - `date_posted`: 매물이 게시된 날짜
---

## 🔧 주요 전처리 내용

- `title` 컬럼 제거
- 범주형 컬럼 -> 숫자형 컬럼으로 처리
- 스케일링: 선형회귀모델/랜덤포레스트모델 StandardScaler 적용

---

## 🤖 적용한 회귀 모델

| 구분 | 모델 종류 |
|------|-----------|
| 기본 회귀 | Linear Regression, Random Forest Regressor |
| 스케일링 적용 | 다항 회귀 & 규제 회귀 + StandardScaler  |
| 교차검증 적용 | Cross_val_score 기반 Linear & RandomForest 회귀 |

---

## 📈 모델별 성능 비교


| Model                      | RMSE              | R2 Score          | Evaluation Method           |
|:---------------------------|:------------------|:------------------|:----------------------------|
| Linear Regression          | 4.201674e+05      | 3.800000e-01      | Train/Test Split            |
| Random Forest              | 3.162725e+05      | 6.500000e-01      | Train/Test Split            |
| Linear Regression (Scaled) | 4.201674e+05      | 3.800000e-01      | Train/Test Split            |
| Random Forest (Scaled)     | 3.171985e+05      | 6.500000e-01      | Train/Test Split            |
| Linear Regression (CV)     | 2.728264e+15      | -1.346860e+20     | K-Fold Cross-Validation (Avg) |
| Random Forest (CV)         | 1.800404e+05 🥇     | 8.200000e-01 🥇     | K-Fold Cross-Validation (Avg) |
| XGBoost                    | 3.298193e+05      | 6.200000e-01      | Train/Test Split (Early Stopping) |

---

## ✅ 결론

* 모델 학습 및 평가 결과, 랜덤 포레스트 회귀 모델이 중고차 가격 예측에 있어 가장 우수한 성능을 보이는 것으로 확인되었습니다. 특히 **교차 검증을 통해 평가된 Random Forest (CV) 모델**은 RMSE 1.80e+05로 가장 낮은 오차를 기록했으며, R2 Score 0.82로 가장 높은 설명력을 보여주었습니다. 이는 모델이 중고차 가격의 변동성을 약 82% 설명할 수 있음을 의미하며, 실제 가격을 상당히 정확하게 예측하고 있음을 시사합니다.

* 반면, 선형 회귀 모델은 교차 검증 과정에서 비정상적으로 높은 RMSE와 매우 낮은 R2 Score를 기록하며 모델의 안정성 및 예측 능력에 심각한 문제가 있음을 드러냈습니다. 이는 선형 회귀 모델이 데이터 내의 복잡한 비선형 관계나 이상치에 취약하며, 이러한 특성을 고려하지 않고서는 안정적인 성능을 기대하기 어렵다는 것을 보여줍니다.

---

## 📌 향후 개선 방향

+ **모델 성능 최적화**: 현재 선정된 랜덤 포레스트 모델에 대한 심층적인 하이퍼파라미터 튜닝을 수행하여 RMSE를 추가로 낮추고 R2 Score를 높이는 것을 목표로 합니다.

+ **모델 일반화 및 안정성 강화**: 선형 회귀 모델에서 나타난 불안정성 문제를 분석하고, 강력한 이상치 처리 기법 및 정규화 기법 적용을 통해 모델의 견고성을 확보할 수 있습니다. 더 나아가 XGBoost, LightGBM 등 다른 부스팅 계열 모델의 도입을 검토하여 예측 성능을 비교하고 최적의 모델을 탐색합니다.

+ **예측 불확실성 분석**: 단일 예측값 제공을 넘어, 특정 중고차에 대한 가격 예측 범위 또는 신뢰 구간을 제시하여 사용자에게 더 유용한 정보를 제공할 수 있도록 모델의 불확실성 분석 기능을 추가합니다.
---

## 🧑‍💻 개발 환경

- Python 
- pandas, numpy, matplotlib, seaborn
- scikit-learn
- Visual Studio Code (VS Code)

---
