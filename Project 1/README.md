# FastAPI 파라미터 처리 가이드

## 1. 자동 타입 변환

FastAPI는 타입 힌트를 사용하면 URL 파라미터를 자동으로 변환해줍니다.

```python
# Default 타입: string
@app.get("/users/{user_id}")
def get_user(user_id):  # str로 받아짐
    return {"user_id": user_id}

# 타입 힌트 사용
@app.get("/users/{user_id}")
def get_user(user_id: int):  # 자동으로 int 변환
    return {"user_id": user_id}
```

**지원 타입**: `int`, `float`, `str`, `bool`, `datetime`, `date`, `UUID`, `Enum`

- `Enum` 예시

```python
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"

@app.get("/users/{user_id}")
def get_user(user_id: int, role: UserRole):
    return {"user_id": user_id, "role": role}

# ✅ 유효한 요청들:
# /users/123?role=admin
# /users/123?role=user
# /users/123?role=guest

# ❌ 에러 발생:
# /users/123?role=invalid  (422 Validation Error)
```

## 2. URL 디코딩

FastAPI는 URL 인코딩된 특수문자를 자동으로 디코딩합니다.

```python
@app.get("/search")
def search(q: str):
    return {"query": q}
```

**디코딩 예시**:

- `/search?q=hello%20world` → `q = "hello world"`
- `/search?q=%ED%95%9C%EA%B5%AD%EC%96%B4` → `q = "한국어"`
- `/users/john%40doe.com` → `username = "john@doe.com"`

**주요 인코딩**:

- `%20` → 공백 " "
- `%40` → "@"
- `%23` → "#"
- `%2F` → "/"

## 3. 쿼리 파라미터

### 기본 쿼리 파라미터

```python
@app.get("/items/")
def get_items(skip: int = 0, limit: int = 10):  # 기본값 설정
    return {"skip": skip, "limit": limit}

@app.get("/search/")
def search(q: str, category: str):  # 기본값 없음 = required
    return {"query": q, "category": category}
```

### Pydantic 모델 (FastAPI 0.115.0+)

쿼리 파라미터를 Pydantic 모델로 그룹화할 수 있습니다.

```python
from typing import Annotated
from fastapi import Query
from pydantic import BaseModel, Field

class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    tags: list[str] = []

@app.get("/items/")
def get_items(filter_query: Annotated[FilterParams, Query()]):
    return filter_query

# 사용 예: /items/?limit=50&offset=10&tags=python&tags=fastapi
```

**주의**: Path 파라미터에서는 여전히 기본 타입들만 사용 가능합니다.

## 4. Request Body (POST 메서드)

POST, PUT, DELETE, PATCH 메서드에서는 Pydantic 모델을 Request Body로 사용할 수 있습니다.

### 기본 Request Body

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.post("/items/")
def create_item(item: Item):
    return item

# JSON 요청 예시:
# {
#   "name": "Laptop",
#   "description": "Gaming laptop",
#   "price": 999.99,
#   "tax": 99.99
# }
```

### 자동 타입 변환 및 검증

FastAPI는 JSON 요청 body를 자동으로 Pydantic 모델로 변환하고 검증합니다:

- **파싱**: JSON 데이터를 자동으로 Python 객체로 변환
- **타입 변환**: 각 필드를 올바른 타입으로 자동 변환
- **검증**: 모델 스키마에 맞는지 검증
- **에러 처리**: 잘못된 데이터 시 422 에러 자동 반환

### Path, Query, Body 파라미터 동시 사용

```python
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item, q: str | None = None):
    return {"item_id": item_id, "item": item, "q": q}

# FastAPI가 자동으로 구분:
# - item_id: Path 파라미터 (URL에서)
# - item: Request Body (JSON에서)
# - q: Query 파라미터 (URL 쿼리에서)
```

**curl 요청 예시**:

```bash
# q 파라미터 없이
curl -X PUT "http://localhost:8000/items/123" \
  -H "Content-Type: application/json" \
  -d '{"name": "Updated Laptop", "price": 1299.99}'

# q 파라미터 포함
curl -X PUT "http://localhost:8000/items/123?q=electronics" \
  -H "Content-Type: application/json" \
  -d '{"name": "Updated Laptop", "price": 1299.99}'

# 응답 예시:
# {
#   "item_id": 123,
#   "item": {"name": "Updated Laptop", "price": 1299.99, "description": null, "tax": null},
#   "q": "electronics"
# }
```

## 5. 파라미터 순서와 구분

FastAPI는 타입을 보고 파라미터를 자동으로 구분하므로 **순서는 상관없습니다**.

**자동 구분 규칙**:

- Path에 선언된 변수 → **Path 파라미터**
- 기본 타입 (`int`, `str` 등) → **Query 파라미터**
- Pydantic 모델 → **Request Body**

**권장 순서** (가독성을 위해):

```python
def update_item(
    item_id: int,        # Path 파라미터
    item: Item,          # Request Body
    q: str = None        # Query 파라미터
):
```
