# 프로젝트 설명
해당 프로젝트는 소설 이용권을 받을 수 있는 이벤트 페이지입니다. django rest framework, jQuery를 이용하여 구현했습니다.


# 프로젝트 유의 사항
- Book 모델의 경우 별도의 앱에 존재해야하지만 구현의 편의상 event 앱에 넣었습니다.
- 투댓이라는 서비스가 Client가 별도로 존재하는 서비스라는 가정 하에 해당 프로젝트에서는 화면을 구성하는 view와 데이터를 주는 APIView를 구분해서 구현하였습니다.
- 이미지는 편의상 인터넷에서 다운 받았습니다. 상업적인 용도로 사용하지 않습니다.
- 환경 변수는 따로 분리하지 않았습니다.(상용 서버로 올리지 않을 것이라는 판단과 과제 평가 효율성 기대)

# 사전 작업
1. 가상환경 구축
2. project level에서 requirement.txt install
3. db 생성
```bash
python manage.py migrate
```
4. 기본 데이터 추가
```bash
python manage.py loaddata initial_data.json
```

# 화면 구성
화면은 리스트를 불러와 화면에 입히는 pages와 그 안에 들어가는 요소인 components로 구성했습니다.

### components
eventCard.js: 이벤트 페이지 내의 카드를 만드는 요소

### pages
eventBookList.js: 카드 요소들을 화면에 입히기 위한 제작


# 데이터 베이스
### Book
소설 테이블입니다. 여기서는 테스트를 위해서 제목 필드 정도만 만들어둔 상태입니다.
| 필드명 | 타입 | 설명 |
| --- | --- | --- |
| title | str | 소설의 제목을 저장하고 있는 필드입니다. |

### Coupon
쿠폰(이용권) 테이블입니다.
| 필드명 | 타입 | 설명 |
| --- | --- | --- |
| book | foreignkey | 어떤 소설에 연관된 쿠폰(이용권)인지에 대한 정보를 가지고 있는 필드입니다. |
| number | str | 쿠폰 번호를 저장하고 있는 필드입니다. 제시된 문제에는 이용권 발급에 대한 부분이라 해당 필드가 필요없을 수 있지만, 차후 문자열로 쿠폰을 진행하는 형태 또한 재밌을 것 같아 추가시켜놓았습니다. |
| quantity | int | 쿠폰 수량을 저장하고 있는 필드입니다. 모델 메소드를 통해 유저 한명이 이용권을 발급 받을 때마다 감소합니다. |
| status | str | 해당 쿠폰의 발급 진행 여부를 판단하는 필드입니다. ACTIVE, COMPLETE 2가지 타입이 존재하면 COMPLETE일 경우 이벤트 페이지에 노출되지 않습니다. |

### UserCouponList
유저가 발급받은 쿠폰 정보를 저장하는 필드입니다.
| 필드명 | 타입 | 설명 |
| --- | --- | --- |
| user | foreignkey | 해당 쿠폰을 발급 받은 유저 정보를 저장하는 필드입니다. |
| coupon | foreignkey | 쿠폰 정보를 저장하고 있는 필드입니다. |
| is_used | bool | 발급받은 쿠폰의 사용여부를 저장하고 있는 필드입니다. |
| created_at | datetime |쿠폰 발급 날짜를 저장하고 있는 필드입니다. |

# API
### 회원가입
POST: /accounts/register/
```json
{
    "username": {{닉네임}},
    "password": {{비밀번호}}
}
```

### 로그인
POST: /accounts/login/
```json
{
    "username": {{닉네임}},
    "password": {{비밀번호}}
}
```

### 로그아웃
GET: /accounts/logout

### 쿠폰 생성
어드민 페이지 이용

### 이벤트 중인 소설 리스트
GET: /event/list

### 이용권 다운로드
POST: /event/download/
```json
{
    "couponNumber": {{쿠폰번호}}
}
```

# 테스트
Unit test에 대한 요구 사항이 있어 코드를 확인한 결과, 오히려 Test Coverage가 낮은 것이 효율적이라고 판단을 내렸습니다.

# 문제해결
- EventListener 중복 적용 이슈
문제 : 이용권 발급 버튼을 다수를 실행할 경우, 2번째 버튼 클릭시 'django.db.utils.OperationalError: database is locked'에러가 1번 3번째 버튼 클릭시 2번 노출되는 식으로 반복
원인 : A Tag 자체에 ClickEventHandler가 중복으로 적용되면서 발생
해결 방법 : 해당 DOM을 그릴 때 A Tag에 적용되어있던 이벤트를 전부 지우고 다시 적용

# 아쉬운 부분
1. Select for Update
Django에서 제공하는 Select for Update를 사용해서 동시에 해당 객체에 접근하면서 발생할 수 있는 문제를 예방했지만, 과도한 트래픽이 몰렸을 때 오히려 성능을 저하시킬 수 있는 요소라 아쉽게 생각합니다. 후에 리소스를 조금 더 사용하면 속도를 중시하는 redis와 같은 in memory cache 기반의 툴을 사용해서 db hit도 줄이는 방법으로 변경하면 좋을 것 같다고 생각합니다.