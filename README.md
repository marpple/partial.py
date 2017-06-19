# Functional Python Library - Partial.py

[Site](https://marpple.github.io/partial.py/) | [Docs](https://marpple.github.io/partial.py/docs)

Partial.py는 함수형 파이썬을 더 많은 영역에서 사용하고자, 몇 가지 기능을 확장한 라이브러리입니다. Partial.py는 부분 적용, 파이프라인, 비동기 제어 등의 기능을 제공하고 있습니다.

## 설치하기

### Partial.py 설치

##### git으로 설치하기:

```bash
$ git clone https://github.com/marpple/partial.py.git
$ cd partial.py
$ sudo python setup.py install
```

__혹은__

##### pypi로 설치하기:

```bash
$ pip install partial.py
```

### Partial.py 사용

네임스페이스로 사용할 `_`, `__`, `___`를 불러옵니다.

```python
from partial import _, __, ___
```

## 더 나은 부분 적용 (Partial application)

Partial.py는 이름처럼 부분 적용(Partial application)을 중요하게 생각합니다. 기존의 `_.partial` 함수는 왼쪽에서부터만 인자를 적용해둘 수 있습니다. Partial.py의 `_.partial` 함수는 맨 오른쪽 인자나 맨 오른쪽에서 두 번째에만 인자를 적용해두는 것도 가능하며, 새로운 구분자인 `___`를 활용하여 중간 지점에 인자가 가변적으로 적용되도록 비워둘 수 있습니다.

### _.partial의 일반적 사용

`_.partial`을 실행하면서 인자 자리에 `_`를 넘기면 부분 적용할 인자를 건너띌 수 있습니다. `_`를 이용하면 원하는 곳에만 인자를 부분 적용해둘 수 있습니다. `_`가 있는 자리는 이후 실행시 채워집니다.

```python
pc = _.partial(print, 1)
pc(2)
# 결과: 1 2
# 2 가 오른쪽으로 들어갑니다.
pc(2, 3)
# 결과: 1 2 3
# 2, 3이 오른쪽으로 들어갑니다.

pc = _.partial(print, _, 2)
pc(1)
# 결과: 1 2
# 1이 왼쪽의 _ 자리에 들어갑니다.
pc(1, 3)
# 결과: 1 2 3
# 1이 왼쪽의 _ 자리에 들어가고 3이 오른쪽으로 들어갑니다.

pc = _.partial(print, _, _, 3)
pc(1)
# 결과: 1 undefined 3
# 1이 왼쪽의 _ 자리에 들어가고 두 번째 _는 들어오지 않아 undefined가 됩니다.
pc(1, 2)
# 결과: 1 2 3
# 1과 2가 순서대로 _, _를 채웁니다.
pc(1, 2, 4)
# 결과: 1 2 3 4
# 1과 2가 순서대로 _, _를 채우고 3의 오른쪽으로 4가 들어갑니다.

pc = _.partial(print, _, 2, _, 4)
pc(1, 3, 5)
# 결과: 1 2 3 4 5
# 1을 _ 자리에 채우고 2를 넘겨서 _에 3을 채우고 4의 오른쪽에 5가 들어갑니다.

pc = _.partial(print, _, 2, _, _, 5)
pc(1, 3, 4, 6)
# 결과: 1 2 3 4 5 6
# 1을 _ 자리에 채우고 2를 넘겨서 _에 3을 채우고 다음 _에 4를 채우고 5의 오른쪽에 6이 들어갑니다.
```

### 오른쪽에서부터 인자 적용해두기

`_.partial`을 실행하면 `___`를 기준으로 왼편의 인자들을 왼쪽부터 적용하고 오른편의 인자들을 오른쪽부터 적용할 준비를 해둔 함수를 리턴합니다. 부분 적용된 함수를 나중에 실행하면 그때 받은 인자들로 왼쪽과 오른쪽을 먼저 채운 후, 남은 인자들로 가운데 `___` 자리를 채웁니다.

```python
pc = _.partial(print, ___, 2, 3)
pc(1)
# 결과: 1 2 3
# ___ 자리에 1이 들어가고 2, 3은 맨 오른쪽에 들어갑니다.
pc(1, 4, 5, 6)
# 결과: 1 4 5 6 2 3
# ___ 자리에 1, 4, 5, 6이 들어가고 2, 3은 맨 오른쪽에 들어갑니다.

pc = _.partial(print, _, 2, ___, 6)
pc(1, 3, 4, 5)
# 결과: 1 2 3 4 5 6
# _에 1이 들어가고 2를 넘어가고 ___ 자리에 3, 4, 5가 채워지고 6이 맨 오른쪽에 들어갑니다.
pc(1, 3, 4, 5, 7, 8, 9)
# 결과: 1 2 3 4 5 7 8 9 6
# _에 1이 들어가고 2를 넘어가고 ___ 자리에 3, 4, 5, 7, 8, 9가 채워지고 6이 맨 오른쪽에 들어갑니다.

pc = _.partial(print, _, 2, ___, 5, _, 7)
pc(1)
# 결과: 1 2 5 undefined 7
# _ 자리에 1이 들어가고 2와 5사이는 유동적이므로 모이고 5가 들어간 후 _가 undefined로 대체 되고 7이 들어갑니다.
pc(1, 3, 4)
# 결과: 1 2 3 5 4 7
# _ 자리에 1이 들어가고 2와 5사이에 3이 들어가고 _ 를 4로 채운 후 7이 들어갑니다.
# 왼쪽의 _ 들이 우선 순위가 제일 높고 ___ 보다 오른쪽의 _ 들이 우선순위가 높습니다.
pc(1, 3, 4, 6, 8)
# 결과: 1 2 3 4 6 5 8 7
# _ 자리에 1이 들어가고 2와 5사이에 3, 4, 6이 들어가고 _ 를 8로 채운 후 7이 들어갑니다.
```

### 간결하게 사용하기

`_ == _.partial`입니다. `_.partial`을 `_`로 간결하게 표현할 수 있습니다.

```python
def add (a, b): 
  return a + b
  
add10 = _(add, 10)
print( add10(5) )
# 15
```

## 파이프라인

파이프라인 함수인 `_.pipe`, `_.go` 등은 작은 함수들을 모아 큰 함수를 만드는 함수입니다. 파이프라인으로 함수를 조합하면 왼쪽에서부터 오른쪽, 위에서부터 아래로 표현되어 읽기 쉬운 코드가 됩니다. 체인 방식과 다르게 아무 함수나 사용할 수 있어 자유도가 높습니다. 작은 함수들을 인자와 결과만을 생각하면서 조합하면 됩니다.

### 즉시 실행과 Multiple Results

`_.go`는 파이프라인의 즉시 실행 버전입니다. 첫 번째 인자로 받은 값을 두 번째 인자로 받은 함수에게 넘겨주고 두 번째 인자로 받은 함수의 결과는 세 번째 함수에게 넘겨주는 것을 반복하다가 마지막 함수의 결과를 리턴해줍니다.

```python
_.go(10, # 첫 번째 함수에서 사용할 인자
  lambda a: a * 10, # 연속 실행할 함수 1
  # 100
  lambda a: a - 50, # 연속 실행할 함수 2
  # 50
  lambda a: a + 10) # 연속 실행할 함수 3
  # 60
```

`_.go`는 Multiple Results를 지원합니다. `_.mr` 함수를 함께 사용하면 다음 함수에게 2개 이상의 인자들을 전달할 수 있습니다.

```python
_.go(10, # 첫 번째 함수에서 사용할 인자
  lambda a: _.mr(a * 10, 50), # 두 개의 값을 리턴
  lambda a, b: a - b, # 두 개의 인자 받기
  lambda a: a + 10)
  # 60
```

`_.go`의 첫 번째 인자는 두 번째 인자인 함수가 사용할 인자고 두 번째 부터는 파이프라인에서 사용할 함수들입니다. `_.go`의 두 번째 인자인 함수, 즉 최초 실행될 함수에게 2개 이상의 인자를 넘기고자 한다면 `_.mr`을 사용하면 됩니다. `_.mr`로 인자들을 감싸서 넘겨주면, 다음 함수는 인자를 여러 개로 펼쳐서 받게 됩니다.

```python
_.go(_.mr(2, 3),
  lambda a, b: a + b, # 2 + 3
  lambda a: a * a)
  # 25
```

`_.go`를 이미 정의되어 있는 함수와 조합하면 더욱 읽기 좋아집니다.

```python
def add(a, b):
  return a + b
  
def square(a):
  return a * a
  
_.go(_.mr(2, 3), add, square)
# 25
```

### 파이프라인 함수를 리턴하는 _.pipe

`_.go`가 즉시 실행하는 파이프라인이라면 `_.pipe`는 실행할 준비가 된 함수를 리턴하는 파이프라인 함수입니다. 그외 모든 기능은 `_.go`와 동일합니다.

```python
f1 = _.pipe(add, square)
f1(2, 3)
# 25
```

## 부분 커링

### 커링이 부분적으로 동작하는 함수

Partial.py의 주요 함수들은 커링이 부분적으로 동작하도록 지원하고 있습니다. 아래는 일반적인 사용 모습입니다.

##### 일반적인 방식:

```python
values = lambda data: _.map(data, lambda v, *r: v)
print(values({ 'a': 1, 'b': 2, 'c': 4 }))
# [1, 2, 4]

take3 = lambda data: _.take(data, 3)
take3([1, 2, 3, 4, 5])
# [1, 2, 3]
```

Partial.py의 주요 함수들은 부분 커링이 적용되어 위와 동일한 동작을 아래와 같이 간결하게 표현할 수 있습니다.

##### 부분 커링이 지원될 경우:

```python
values = _.map(lambda v, *r: v)
print(values({ 'a': 1, 'b': 2, 'c': 4 }))
# [1, 2, 4]

take3 = _.take(3)
take3([1, 3, 5, 7, 9])
# [1, 3, 5]
```

### 파이프라인과 함께

부분 커링이 지원되면 파이프라인과 함께 사용할 때, 체인처럼 간결한 표현이 가능합니다.

```python
users = [
  { 'id': 1, 'name': 'ID', 'age': 32 },
  { 'id': 2, 'name': 'HA', 'age': 25 },
  { 'id': 3, 'name': 'BJ', 'age': 32 },
  { 'id': 4, 'name': 'PJ', 'age': 28 },
  { 'id': 5, 'name': 'JE', 'age': 27 },
  { 'id': 6, 'name': 'JM', 'age': 32 },
  { 'id': 7, 'name': 'JI', 'age': 31 }
]

## 일반적인 사용
_.go(users,
  lambda users: _.filter(users, lambda u, *r: u['age'] < 30),
  lambda users: _.pluck(users, 'name'),
  print)
# ["HA", "PJ", "JE"]

## 부분 커링이 된다면
_.go(users,
  _.filter(lambda u, *r: u['age'] < 30),
  _.pluck('name'),
  print)
# ["HA", "PJ", "JE"]

## Underscore.py 체인
underscore\
  .chain(users)\
  .filter(lambda u: u['age'] < 30)\
  .pluck('name')\
  .tap(print)
# ["HA", "PJ", "JE"]
```

`_.go`, `_.pipe` 등의 파이프라인이 받는 재료는 함수이기 때문에 아무 함수나 조합할 수 있습니다. 체인처럼 메서드 등으로 준비되어있지 않아도 되며 Partial.py의 함수만 사용할 필요도 없습니다. Partial.py의 파이프라인은 결과를 여러 개로 리턴할 수 있고, 여러 개의 인자를 받을 수 있고, 다른 라이브러리에 있는 함수든, 직접 만든 함수든, 익명 함수든 모두 쉽게 사용할 수 있습니다.

```python
products = [
  { 'id': 1, 'name': '후드 집업', 'discounted_price': 6000, 'price': 10000  },
  { 'id': 2, 'name': '코잼 후드티', 'discounted_price': 8000, 'price': 8000  },
  { 'id': 3, 'name': 'A1 반팔티', 'discounted_price': 6000, 'price': 6000  },
  { 'id': 4, 'name': '코잼 반팔티', 'discounted_price': 5000, 'price': 6000  }
]

# 할인 상품들을 가격이 낮은 순으로 정렬한 상품 이름들
_.go(products,
  _.filter(lambda p, *r: p['price'] > p['discounted_price']),
  _.sortBy('discounted_price'),
  _.pluck('name'),
  print)
  # ["코잼 반팔티", "후드 집업"]

# 할인이 없는 상품들의 id들
_.go(products,
  _.reject(lambda p, *r: p['price'] > p['discounted_price']),
  _.pluck('id'),
  print)
  # [2, 3]

# 할인 상품 중 할인액이 가장 낮은 상품의 이름
_.go(products,
  _.filter(lambda p, *r: p['price'] > p['discounted_price']),
  _.min(lambda p, *r: p['price'] - p['discounted_price']),
  _.val('name'),
  print)
  # 코잼 반팔티

# 할인액이 가장 높은 상품의 이름
_.go(products,
  _.max(lambda p, *r: p['price'] - p['discounted_price']),
  _.val('name'),
  print)
  # 후드 집업
```

## 비동기

`async`, `await` 키워드와 Partial.py를 함께 사용하면 다양한 비동기 상황을 간단히 제어할 수 있습니다.

### 파이프라인으로 비동기 제어 하기

`_.asy`를 네임스페이스로 갖는 `_.asy.go`, `_.asy.pipe` 등의 파이프라인 함수들은 비동기 제어를 지원합니다.

##### await 키워드와 함께 사용:

```python
async def asy_add(val, *r):
  await asyncio.sleep(1)
  return val + 10
  
## await 키워드를 사용해서 바로 실행하는 _.go.asy
await _.asy.go(10,
  asy_add,
  print)
  # 20
  
## _.asy.pipe로 비동기 함수와 동기 함수 조합해 만든 새로운 함수
asy_pipe = _.asy.pipe(asy_add, print)
await asy_pipe(10) 
# 20

## _.pipe는 비동기 함수를 만나면 자동으로 _.asy.pipe가 됩니다.
asy_pipe = _.pipe(asy_add, print)
await asy_pipe(10)
# 20
```

### 컬렉션을 다루는 비동기 제어 함수

Partial.py의 `_.each`, `_.map`, `_.reduce` 등의 주요 함수들은 `_.asy.go`와 `_.asy.pipe`처럼 동기와 비동기 상황이 모두 대응되도록 되어 있습니다. Partial.py의 함수를 이용하면 비동기 상황에서도 동기 상황과 동일한 코드를 작성할 수 있고, 비동기 함수와 동기 함수의 조합도 가능합니다.

```python
async def asyncDate(*r):
  await asyncio.sleep(1)
  return datetime.datetime.now()

def syncDate(*r):
  return datetime.datetime.now()

_.go(
  [1, 2, 3],
  _.map(syncDate),
  _.map(lambda now, *r: now.strftime('%Y-%m-%d %H:%M:%S')),
  print)
# ['2017-06-16 12:34:39', '2017-06-16 12:34:39', '2017-06-16 12:34:39']

await _.asy.go(
  [1, 2, 3],
  _.map(asyncDate),
  _.map(lambda now, *r: now.strftime('%Y-%m-%d %H:%M:%S')),
  print)
# ['2017-06-16 12:34:39', '2017-06-16 12:34:39', '2017-06-16 12:34:39']
```

위 사례처럼 Partial.py는 `_.pipe`, `_.each`, `_.map`, `_.find`, `_.filter`, `_.reject`, `_.reduce`, `_.some`, `_.every` 등의 함수들에서 자동 비동기 제어 로직을 지원합니다.


## 지연 평가 L

Partial.py의 `L`을 이용하면, 파이프라인 내부에서 함수들의 실행 순서를 재배치하여 적절하게 평가를 지연합니다. 사용법은 간단합니다. Partial.py에서 `L`을 `import`하시면 됩니다. `L`을 통해 지연 평가할 영역을 명시적으로 선택할 수 있습니다. `_.go, _.pipe`등의 파이프라인이 `L`로 시작하여 `L`로 끝날 때까지의 함수들을 재배치하여 성능을 개선합니다.

### 비교

##### 엄격한 평가:
```python
list = [1, 2, 3, 4, 5, 6]
_.go(list,
  _.map(lambda v, *r: v * v), #6번
  _.filter(lambda v, *r: v <20), #6번
  _.take(2),
  print)
# [1, 4]
# 총 12번
```

##### 지연 평가:
```python
list = [1, 2, 3, 4, 5, 6]
_.go(list,
  L.map(lambda v, *r: v * v), #2번
  L.filter(lambda v, *r: v <20), #2번
  L.take(2),
  print)
# [1, 4]
# 총 4번  
```

### 지원 함수들

Partial.js의 지연 평가 지원 함수로는 `L.map`, `L.filter`, `L.reject`, `L.find`, `L.some`, `L.every`, `L.take`가 있습니다. 이 함수들을 순서대로 나열하면 파이프라인이 평가 시점을 변경하여 성능을 개선합니다.

다음과 같은 상황 등에서 동작합니다.

- map->map->map
- map->take
- filter->take
- map->filter->take
- map->filter->map->map
- map->filter->map->take
- map->reject->map->map->filter->map
- map->some
- map->every
- map->find
- map->filter->some
- map->filter->every
- map->filter->find
- filter->map->some
- filter->map->every
- filter->map->reject->find

지연 평가를 시작시키고 유지 시키는 함수는 `map`, `filter`, `reject`이고 끝을 내는 함수는 `take`, `some`, `every`, `find`, 입니다.

```python
users = [
  { 'id': 1, 'name': "ID", 'age': 12 },
  { 'id': 2, 'name': "BJ", 'age': 28 },
  { 'id': 3, 'name': "HA", 'age': 13 },
  { 'id': 4, 'name': "PJ", 'age': 23 },
  { 'id': 5, 'name': "JE", 'age': 29 },
  { 'id': 6, 'name': "JM", 'age': 32 },
  { 'id': 7, 'name': "JE", 'age': 31 },
  { 'id': 8, 'name': "HI", 'age': 15 },
  { 'id': 9, 'name': "HO", 'age': 28 },
  { 'id': 10, 'name': "KO", 'age': 34 }
]

# 10대 2명까지만 찾아내기
_.go(users,
  L.filter(lambda user, *r : user['age'] < 20),
  L.take(2),
  print)
# [{ 'id': 1, 'name': "ID", 'age': 12 }, { 'id': 3, 'name': "HA", 'age': 13 }]
# 3번만 반복

# 10대 2명까지만 찾아내서 이름 수집하기
_.go(users,
  L.filter(lambda user, *r : user['age'] < 20),
  L.map(lambda v, *r : v['name']),
  L.take(2),
  print)
# ["ID", "HA"]
# 3번만 반복
```

### L.strict

`L.strict`를 이용하여 지연 평가를 동작시킬 것인가를 동적으로 변경할 수 있습니다.

##### 숫자로 하기:
```python
strict_or_lazy1 = __(
  _.range,
  L.strict(100),
  L.map(lambda v, *r: v * v),
  L.filter(lambda v, *r: _.bool(v % 2)),
  L.take(10),
  print)

strict_or_lazy1(50)
# [1, 9, 25, 49, 81, 121, 169, 225, 289, 361]
# 50 번 반복 (염격)

strict_or_lazy1(100);
# [1, 9, 25, 49, 81, 121, 169, 225, 289, 361]
# 20 번 반복 (지연)

strict_or_lazy1(15);
# [1, 9, 25, 49, 81, 121, 169]
# 15 번 반복 (엄격)
```

##### 함수로 하기:
```python
strict_or_lazy2 = __(
  _.range,
  L.strict(lambda list, *r : len(list) < 100),
  L.map(lambda v, *r : v * v),
  L.filter(lambda v, *r : bool(v % 2)),
  L.take(10),
  print)

strict_or_lazy2(50)
# [1, 9, 25, 49, 81, 121, 169, 225, 289, 361]
# 50 번 반복 (염격)

strict_or_lazy2(100)
# [1, 9, 25, 49, 81, 121, 169, 225, 289, 361]
# 20 번 반복 (지연)

strict_or_lazy2(15);
# [1, 9, 25, 49, 81, 121, 169]
# 15 번 반복 (엄격)
```
