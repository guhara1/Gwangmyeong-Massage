# 색인 가속 가이드 (네이버 · 구글 · 빙)

가장 빠른 색인을 위한 구성입니다. 핵심은 **① 사이트맵/RSS 제출 ② IndexNow 즉시 통보
③ 구글 Indexing API** 의 조합입니다.

> 참고: 구글·빙의 옛 `sitemap ping`(`/ping?sitemap=`) 엔드포인트는 2023년에 **폐지**되었습니다.
> 더 이상 동작하지 않으므로, 아래 방식이 현재 가장 빠른 경로입니다.

---

## 생성되는 파일 (`python3 build.py`)

| 파일 | 용도 |
|---|---|
| `sitemap.xml` | 전 페이지 + `lastmod` (구글/네이버/빙 공통) |
| `rss.xml` | 네이버 서치어드바이저 **RSS 제출**용 |
| `robots.txt` | 전 검색엔진 허용 + 네이버 `Yeti` 명시 + 사이트맵 2종 |
| `e88fb3ce6f6df267e9cd6add7b084730.txt` | **IndexNow 인증 키 파일** (루트 게시 필수) |

---

## 1단계 — 검색엔진에 사이트 등록 (최초 1회)

### 네이버 서치어드바이저 (searchadvisor.naver.com)
1. 사이트 등록 → 소유확인 (메인 `<head>`에 인증 메타 이미 삽입됨)
2. **요청 → 사이트맵 제출**: `sitemap.xml`
3. **요청 → RSS 제출**: `rss.xml`
4. (선택) **웹페이지 수집** 에서 주요 URL 직접 수집 요청

### 구글 서치콘솔 (search.google.com/search-console)
1. 도메인/URL 속성 추가 → 소유확인
2. **Sitemaps** 에 `sitemap.xml` 제출
3. **URL 검사 → 색인 생성 요청** 으로 핵심 페이지 즉시 요청

### 빙 웹마스터 (bing.com/webmasters)
1. 사이트 추가(구글 서치콘솔에서 가져오기 가능)
2. 사이트맵 제출 — 빙은 IndexNow도 함께 사용

---

## 2단계 — IndexNow 즉시 통보 (Bing · Naver · Yandex · Seznam)

키 파일이 `https://gwangmyeong-massage.netlify.app/<KEY>.txt` 로 게시되어 있어야 합니다(빌드 시 자동 생성).

```bash
python3 indexnow.py                 # sitemap의 모든 URL 통보
python3 indexnow.py /reservation/   # 특정 페이지만 통보(수정/신규 시 권장)
```

- 의존성 없음(표준 라이브러리). 응답 200/202면 정상 접수입니다.
- **글/페이지를 추가하거나 수정한 뒤 실행**하면 즉시 재크롤이 유도됩니다.

---

## 3단계 — 구글 Indexing API (구글은 IndexNow 미참여)

```bash
# 최초 1회 준비
#  - GCP에서 Indexing API 사용 설정 → 서비스 계정 JSON 키 발급
#  - 서치콘솔 속성에 서비스 계정 이메일을 '소유자'로 추가
pip install google-auth requests
export GOOGLE_APPLICATION_CREDENTIALS=/path/service-account.json

python3 google_indexing.py                 # 전체
python3 google_indexing.py /notice/        # 특정 페이지
```

- 일일 쿼터(기본 200건)가 있으니 **변경된 URL만** 보내는 것이 좋습니다.

---

## 4단계 — 자동화 (글 올릴 때마다 자동 통보)

`.github/workflows/index-ping.yml` 가 **푸시 시 자동 실행**됩니다(기본 `main`/`master`).

1. 사이트맵/RSS 재생성 → 2. 60초 대기(배포 시간) → 3. IndexNow 통보
4. 시크릿 `GOOGLE_SA_JSON`(서비스 계정 JSON 전체)을 등록하면 구글 Indexing API도 자동 실행

수동 실행: GitHub → Actions → "색인 통보" → Run workflow (경로 입력 가능).

> 현재 작업 브랜치는 `claude/modest-hamilton-j4u6wa` 입니다. 워크플로는 `main`/`master` 기준이므로,
> 운영 브랜치에 병합되면 자동 동작합니다. 그 전에는 로컬에서 `indexnow.py`로 수동 통보하세요.

---

## 키 관리 주의
- `INDEXNOW_KEY`(build.py)와 루트의 `<KEY>.txt` 내용은 **항상 일치**해야 합니다.
- 키를 바꾸면 기존 `*.txt`를 지우고 다시 빌드하세요.
