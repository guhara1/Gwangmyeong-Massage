# 간다GO · 광명 출장마사지 / 광명시 홈타이 지역 SEO 사이트

광명시 방문형 마사지·홈타이 예약 안내 정적 사이트입니다. 구글 SEO·네이버 검색 설명문·
구글 스팸 정책을 준수하도록 대표 행정동 통합, 역세권 단일화 원칙으로 설계했습니다.

- **상호:** 간다GO
- **전화예약:** 0508-202-4719
- **메타 description:** 모든 페이지 80자 이내

## 페이지 구성 (총 15개)

| 구분 | URL |
|---|---|
| 메인 | `/` (루트 도메인 = 메인페이지) |
| 광명동 | `/gwangmyeong/gwangmyeong-dong-chuljangmassage/` |
| 철산동 | `/gwangmyeong/cheolsan-dong-chuljangmassage/` |
| 하안동 | `/gwangmyeong/haan-dong-chuljangmassage/` |
| 소하동 | `/gwangmyeong/soha-dong-chuljangmassage/` |
| 일직동 | `/gwangmyeong/iljik-dong-chuljangmassage/` |
| 학온동 | `/gwangmyeong/hagon-dong-chuljangmassage/` |
| 광명역 | `/gwangmyeong/gwangmyeong-station-chuljangmassage/` |
| 철산역 | `/gwangmyeong/cheolsan-station-chuljangmassage/` |
| 광명사거리역 | `/gwangmyeong/gwangmyeongsageori-station-chuljangmassage/` |
| 예약 안내 | `/reservation/` |
| 이용 전 확인사항 | `/notice/` |
| 홈타이 이용 가이드 | `/homethai-guide/` |
| 개인정보 처리방침 | `/privacy/` |
| 고객센터 | `/contact/` |

> 광명1~7동 → 광명동, 철산1~4동 → 철산동, 하안1~4동 → 하안동, 소하1~2동 → 소하동으로
> 통합했고, 일직동·학온동만 단독 페이지입니다. 같은 역의 노선별 중복 페이지는 만들지 않습니다.

## 빌드 방법

콘텐츠는 `pages.py`, 레이아웃/스키마는 `build.py`에서 관리합니다.

```bash
python3 build.py
```

실행하면 각 페이지의 `index.html`, `sitemap.xml`, `robots.txt`가 생성되고
description 80자 점검 결과가 출력됩니다.

## 도메인 / 배포 (Cloudflare Pages)

- 도메인은 `https://gwangmyeong-massage.pages.dev` 기준입니다.
  바꾸려면 `build.py`의 `SITE_URL`만 교체 후 다시 빌드하세요(canonical·OG·sitemap 일괄 반영).
- **메인페이지는 루트 `/`** 입니다. 도메인을 누르면 바로 메인이 열립니다.
  과거 슬러그 `/gwangmyeong-chuljangmassage/`는 `_redirects`로 루트(301)로 보냅니다.
- 파비콘: `favicon.svg`, `favicon.ico`, `favicon-32.png`, `icon-180/192/512.png`,
  PWA용 `site.webmanifest` 포함.
- 실제 오프라인 사업장 주소가 없으므로 `LocalBusiness` 스키마는 사용하지 않습니다.
  주소가 확정되면 `build.py`의 JSON-LD에 추가할 수 있습니다.

## 색인 가속 (네이버·구글·빙)

`sitemap.xml`(lastmod) · `rss.xml`(네이버 RSS 제출) · `robots.txt`(Yeti 명시) ·
IndexNow 키 파일을 빌드 시 자동 생성합니다. 즉시 통보 스크립트와 자동화 포함:

```bash
python3 indexnow.py                 # Bing·Naver·Yandex 즉시 통보
python3 google_indexing.py          # 구글 Indexing API (서비스 계정 필요)
```

자세한 설정·자동화는 **[INDEXING.md](INDEXING.md)** 참고.

## SEO 적용 메모

- 스키마: `WebPage` + `BreadcrumbList` + `Organization` (전 페이지)
- H1 1개 + 의미 단위 H2 구조, 페이지별 고유 생활권 본문
- 메인↔행정동↔역세권 내부링크 설계 반영
- 합법적 방문형 안내 문구만 사용(불법·선정·허위 후기·과장 표현 배제)
