<div align="center">

# Chat Service Backend

### FastAPI → Supabase → Authentication → Redis

사용자 인증과 데이터베이스를 연결하고  
대화와 메시지를 저장하는 백엔드 구조를 학습한 저장소입니다.

`Auth` · `Database` · `Conversation` · `Cache`

</div>

---

## About

FastAPI와 Supabase를 연결해  
**회원 인증, 프로필, 대화, 메시지 데이터 흐름**을 구현했습니다.

Redis 캐시까지 추가하면서  
인증된 사용자의 데이터를 처리하는 백엔드 구조를 연습했습니다.

---

## What I Built

| Area | Practice |
| :---: | :--- |
| Backend | FastAPI · APIRouter |
| Database | Supabase · PostgreSQL |
| Authentication | Signup · Login · Bearer Token |
| User | Profile 조회 · 수정 |
| Conversation | 생성 · 조회 · 수정 · 삭제 |
| Message | 저장 · 조회 |
| Cache | Redis · TTL · Cache Invalidation |

---

## Core Flow

<div align="center">

### Auth → User → Conversation → Message → Cache

</div>

```text
Client
  ↓
Signup / Login
  ↓
Access Token
  ↓
FastAPI
  ↓
Authentication
  ↓
Supabase
  ↓
Conversation / Message
  ↓
Redis Cache
```

사용자 인증 이후 현재 사용자를 확인하고,  
해당 사용자의 데이터만 처리하는 흐름을 연습했습니다.

---

## API

### Authentication

| Method | Endpoint | Description |
| :---: | :--- | :--- |
| `POST` | `/auth/signup` | 회원가입 |
| `POST` | `/auth/login` | 로그인 및 Access Token 발급 |

### My Account

| Method | Endpoint | Description |
| :---: | :--- | :--- |
| `GET` | `/me` | 현재 사용자 확인 |
| `GET` | `/me/profile` | 내 프로필 조회 |
| `PATCH` | `/me/profile` | 내 프로필 수정 |
| `GET` | `/me/conversations` | 내 대화 목록 조회 |
| `POST` | `/me/conversations` | 내 대화 생성 |

### Conversations

| Method | Endpoint | Description |
| :---: | :--- | :--- |
| `POST` | `/conversations` | 대화 생성 |
| `GET` | `/conversations` | 사용자별 대화 조회 |
| `PATCH` | `/conversations/{id}` | 대화 제목 수정 |
| `DELETE` | `/conversations/{id}` | 대화 삭제 |
| `POST` | `/conversations/{id}/messages` | 메시지 저장 |
| `GET` | `/conversations/{id}/messages` | 메시지 목록 조회 |

---

## Data Flow

<div align="center">

### User → Conversation → Message

</div>

```text
User
 └─ Profile
     │
     └─ Conversation
          │
          ├─ Message
          ├─ Message
          └─ Message
```

---

<details>
<summary><b>View learning details</b></summary>

<br>

### Authentication

Supabase Auth를 이용해 회원가입과 로그인을 구현했습니다.

### Current User

Bearer Token을 통해 현재 사용자를 확인합니다.

### Supabase

사용자, 대화, 메시지 데이터를 저장하고 조회합니다.

### Redis

메시지 조회 결과를 캐싱하고,  
새 메시지 저장 시 기존 캐시를 무효화합니다.

### Security

인증된 사용자가 자신의 데이터에 접근하는 구조를 연습했습니다.

</details>

---

## Project Structure

```text
2026-db-2_chat-service/
│
├── app/
│   ├── main.py
│   ├── db.py
│   ├── deps.py
│   ├── schemas.py
│   ├── cache.py
│   ├── redis_client.py
│   │
│   └── routers/
│       ├── auth.py
│       ├── conversations.py
│       └── me.py
│
├── sql/
├── .env.example
├── pyproject.toml
├── uv.lock
└── README.md
```

---

## What I Learned

<div align="center">

### Database → Auth → Conversation → Cache

</div>

FastAPI에서 데이터베이스를 사용하는 것뿐 아니라  
**인증된 사용자를 기준으로 데이터를 저장하고 조회하는 흐름**을 이해하는 데 집중했습니다.

Supabase는 원본 데이터 저장소로, Redis는 조회 성능을 위한 캐시로 사용하면서  
각 구성요소의 역할 차이도 함께 학습했습니다.

---

<div align="center">

`Learn` · `Build` · `Test` · `Review` · `Improve`

</div>
