# -*- coding: utf-8 -*-
"""
간다GO · 광명 출장마사지 / 광명시 홈타이 지역 SEO 사이트 정적 생성기

- 공유 레이아웃(헤더/내비/푸터/스키마) + 페이지별 고유 본문
- 모든 페이지 메타 description 80자 이내
- 구글/네이버 SEO 및 스팸 정책 준수(대표 행정동 통합, 역세권 단일화)

도메인은 SITE_URL 한 곳만 바꾸면 canonical/sitemap에 일괄 반영됩니다.
"""
import os
import html
import datetime

YEAR = datetime.date.today().year

# ---------------------------------------------------------------------------
# 사이트 공통 설정
# ---------------------------------------------------------------------------
SITE_URL = "https://gwangmyeong-massage.pages.dev"   # 실제 도메인
BRAND = "간다GO"
PHONE = "0508-202-4719"
PHONE_TEL = "tel:0508-202-4719"
OUT = os.path.dirname(os.path.abspath(__file__))

# IndexNow(빙·네이버·얀덱스 즉시 색인 통보) 인증 키 — 변경 금지(키 파일과 일치해야 함)
INDEXNOW_KEY = "e88fb3ce6f6df267e9cd6add7b084730"
BUILD_DATE = datetime.date.today().isoformat()

# 상단 메뉴 (URL은 사이트 루트 기준)
NAV = [
    ("광명 출장마사지 안내", "/"),
    ("지역별 안내", [
        ("광명동", "/gwangmyeong/gwangmyeong-dong-chuljangmassage/"),
        ("철산동", "/gwangmyeong/cheolsan-dong-chuljangmassage/"),
        ("하안동", "/gwangmyeong/haan-dong-chuljangmassage/"),
        ("소하동", "/gwangmyeong/soha-dong-chuljangmassage/"),
        ("일직동", "/gwangmyeong/iljik-dong-chuljangmassage/"),
        ("학온동", "/gwangmyeong/hagon-dong-chuljangmassage/"),
    ]),
    ("역세권별 안내", [
        ("광명역 출장마사지", "/gwangmyeong/gwangmyeong-station-chuljangmassage/"),
        ("철산역 출장마사지", "/gwangmyeong/cheolsan-station-chuljangmassage/"),
        ("광명사거리역 출장마사지", "/gwangmyeong/gwangmyeongsageori-station-chuljangmassage/"),
    ]),
    ("예약 안내", "/reservation/"),
    ("이용 전 확인사항", "/notice/"),
    ("홈타이 이용 가이드", "/homethai-guide/"),
    ("고객센터", "/contact/"),
]


def esc(s):
    return html.escape(s, quote=True)


def nav_html(current):
    items = []
    for label, target in NAV:
        if isinstance(target, list):
            sub_items = []
            for l, t in target:
                cur = ' aria-current="page"' if t == current else ""
                sub_items.append(f'<li><a href="{t}"{cur}>{esc(l)}</a></li>')
            subs = "".join(sub_items)
            items.append(
                f'<li class="has-sub"><button type="button" aria-haspopup="true">{esc(label)}</button>'
                f'<ul class="sub">{subs}</ul></li>'
            )
        else:
            cur = ' aria-current="page"' if target == current else ""
            items.append(f'<li><a href="{target}"{cur}>{esc(label)}</a></li>')
    return "<ul class=\"nav-list\">" + "".join(items) + "</ul>"


def breadcrumb_html(crumbs):
    """crumbs: list of (name, url|None)"""
    parts = []
    for i, (name, url) in enumerate(crumbs):
        if url and i != len(crumbs) - 1:
            parts.append(f'<a href="{url}">{esc(name)}</a>')
        else:
            parts.append(f'<span aria-current="page">{esc(name)}</span>')
    return '<nav class="breadcrumb" aria-label="breadcrumb">' + ' <span class="sep">›</span> '.join(parts) + "</nav>"


def jsonld(page_title, description, url, crumbs):
    import json
    org = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": BRAND,
        "url": SITE_URL + "/",
        "telephone": PHONE,
        "areaServed": "경기도 광명시",
        "contactPoint": {
            "@type": "ContactPoint",
            "telephone": PHONE,
            "contactType": "reservations",
            "areaServed": "KR",
            "availableLanguage": "Korean",
        },
    }
    webpage = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": page_title,
        "description": description,
        "url": SITE_URL + url,
        "inLanguage": "ko-KR",
        "isPartOf": {"@type": "WebSite", "name": f"{BRAND} 광명 출장마사지", "url": SITE_URL + "/"},
    }
    breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "name": name,
                "item": SITE_URL + (u if u else url),
            }
            for i, (name, u) in enumerate(crumbs)
        ],
    }
    blocks = [webpage, breadcrumb, org]
    return "\n".join(
        f'<script type="application/ld+json">\n{json.dumps(b, ensure_ascii=False, indent=2)}\n</script>'
        for b in blocks
    )


def related_html(title, links):
    items = "".join(f'<li><a href="{u}">{esc(t)}</a></li>' for t, u in links)
    return (
        f'<section class="related" aria-label="{esc(title)}">'
        f'<h2>{esc(title)}</h2><ul class="related-list">{items}</ul></section>'
    )


def cta_html():
    return (
        '<aside class="cta">'
        f'<p class="cta-brand">{esc(BRAND)} 전화예약</p>'
        f'<a class="cta-phone" href="{PHONE_TEL}">{PHONE}</a>'
        '<p class="cta-note">예약 가능 시간·방문 가능 지역·추가 이동비는 통화로 먼저 확인해 주세요.</p>'
        '</aside>'
    )


PAGE_TPL = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="keywords" content="{keywords}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="{robots}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="{brand} 광명 출장마사지">
<meta property="og:locale" content="ko_KR">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Nanum+Myeongjo:wght@400;700;800&family=Noto+Sans+KR:wght@300;400;500;700&display=swap" rel="stylesheet">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="apple-touch-icon" href="/icon-180.png">
<link rel="manifest" href="/site.webmanifest">
<meta name="theme-color" content="#0d6e5a">
{head_extra}<link rel="stylesheet" href="/css/style.css">
{jsonld}
</head>
<body>
<a class="skip" href="#main">본문 바로가기</a>
<header class="site-header">
  <div class="bar">
    <a class="logo" href="/">{brand}<span>광명 출장마사지 · 홈타이</span></a>
    <a class="header-phone" href="{phone_tel}">전화예약 {phone}</a>
    <button class="menu-toggle" type="button" aria-label="메뉴 열기" aria-expanded="false">메뉴</button>
  </div>
  <nav class="site-nav" aria-label="주 메뉴">{nav}</nav>
</header>
<main id="main">
  <div class="container">
    {breadcrumb}
    {body}
    {related}
    {cta}
  </div>
</main>
<footer class="site-footer">
  <div class="container">
    <div class="foot-grid">
      <div class="foot-col foot-about">
        <p class="foot-brand">{brand}</p>
        <p class="foot-desc">경기 광명시 전지역을 안내하는 방문형 마사지·홈타이 예약 안내 서비스입니다. 정확한 방문 가능 지역과 예약 기준을 투명하게 안내합니다.</p>
        <a class="foot-build" href="https://t.me/googleseolab" target="_blank" rel="noopener noreferrer">
          <span class="ico" aria-hidden="true">✦</span> 웹사이트 제작문의
        </a>
      </div>
      <nav class="foot-col" aria-label="이용 안내">
        <p class="foot-label">이용 안내</p>
        <ul class="foot-menu">
          <li><a href="/reservation/">예약 안내</a></li>
          <li><a href="/notice/">이용 전 확인사항</a></li>
          <li><a href="/homethai-guide/">홈타이 이용 가이드</a></li>
          <li><a href="/contact/">고객센터</a></li>
        </ul>
      </nav>
      <nav class="foot-col" aria-label="지역별 안내">
        <p class="foot-label">지역별 안내</p>
        <ul class="foot-menu">
          <li><a href="/gwangmyeong/gwangmyeong-dong-chuljangmassage/">광명동</a></li>
          <li><a href="/gwangmyeong/cheolsan-dong-chuljangmassage/">철산동</a></li>
          <li><a href="/gwangmyeong/haan-dong-chuljangmassage/">하안동</a></li>
          <li><a href="/gwangmyeong/soha-dong-chuljangmassage/">소하동</a></li>
          <li><a href="/gwangmyeong/iljik-dong-chuljangmassage/">일직동</a></li>
          <li><a href="/gwangmyeong/hagon-dong-chuljangmassage/">학온동</a></li>
        </ul>
      </nav>
      <div class="foot-col foot-contact">
        <p class="foot-label">예약 문의</p>
        <p class="foot-phone"><a href="{phone_tel}">{phone}</a></p>
        <p class="foot-meta">상호 · {brand}</p>
        <p class="foot-meta">운영지역 · 경기도 광명시 전지역</p>
        <p class="foot-meta"><a href="/privacy/">개인정보 처리방침</a></p>
      </div>
    </div>
    <div class="foot-bottom">
      <p class="foot-note">본 사이트는 합법적인 방문형 마사지 예약 안내 사이트입니다. 불법·선정적 서비스를 제공하거나 알선하지 않습니다.</p>
      <p class="foot-copy">© {year} {brand}. All rights reserved.</p>
    </div>
  </div>
</footer>
<a class="float-call" href="{phone_tel}" aria-label="전화예약 {phone}">
  <span class="ico" aria-hidden="true">📞</span>
  <span class="txt"><b>전화예약</b>{phone}</span>
</a>
<script>
(function(){{
  var t=document.querySelector('.menu-toggle'),n=document.querySelector('.site-nav');
  if(t&&n){{t.addEventListener('click',function(){{var o=n.classList.toggle('open');t.setAttribute('aria-expanded',o);}});}}
  document.querySelectorAll('.has-sub > button').forEach(function(b){{
    b.addEventListener('click',function(){{b.parentNode.classList.toggle('open');}});
  }});
}})();
</script>
</body>
</html>
"""


def render(path, title, description, keywords, body, crumbs, related, robots="index, follow", head_extra=""):
    canonical = SITE_URL + path
    current = path
    out_dir = OUT + ("" if path == "/" else path)
    os.makedirs(out_dir, exist_ok=True)
    file_path = os.path.join(out_dir, "index.html")
    page = PAGE_TPL.format(
        title=esc(title),
        description=esc(description),
        keywords=esc(keywords),
        canonical=esc(canonical),
        robots=robots,
        brand=esc(BRAND),
        phone=PHONE,
        phone_tel=PHONE_TEL,
        nav=nav_html(current),
        breadcrumb=breadcrumb_html(crumbs),
        body=body,
        related=related,
        cta=cta_html(),
        jsonld=jsonld(title, description, path, crumbs),
        year=YEAR,
        head_extra=head_extra,
    )
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(page)
    return path


# ---------------------------------------------------------------------------
# 페이지 본문 정의
# ---------------------------------------------------------------------------
from pages import PAGES  # noqa: E402


def main():
    paths = []
    for p in PAGES:
        paths.append(
            render(
                path=p["path"],
                title=p["title"],
                description=p["description"],
                keywords=p["keywords"],
                body=p["body"],
                crumbs=p["crumbs"],
                related=related_html(p.get("related_title", "함께 보면 좋은 안내"), p["related"]) if p.get("related") else "",
                robots=p.get("robots", "index, follow"),
                head_extra=p.get("head_extra", ""),
            )
        )

    # 80자 검증
    print("== description 길이 점검 (80자 이내) ==")
    for p in PAGES:
        d = p["description"]
        flag = "OK " if len(d) <= 80 else "OVER"
        print(f"[{flag}] {len(d):>3}자  {p['path']}")

    # ---- sitemap.xml (lastmod 포함) ----
    urls = "".join(
        f"  <url><loc>{esc(SITE_URL + pth)}</loc>"
        f"<lastmod>{BUILD_DATE}</lastmod>"
        f"<changefreq>{'daily' if pth=='/' else 'weekly'}</changefreq>"
        f"<priority>{'1.0' if pth=='/' else '0.8'}</priority></url>\n"
        for pth in paths
    )
    sitemap = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{urls}</urlset>\n"
    )
    with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap)

    # ---- rss.xml (네이버 서치어드바이저 RSS 제출용) ----
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")
    title_map = {p["path"]: (p["title"], p["description"]) for p in PAGES}
    items = []
    for pth in paths:
        t, d = title_map[pth]
        loc = SITE_URL + pth
        items.append(
            "    <item>\n"
            f"      <title>{esc(t)}</title>\n"
            f"      <link>{esc(loc)}</link>\n"
            f"      <description>{esc(d)}</description>\n"
            f"      <guid isPermaLink=\"true\">{esc(loc)}</guid>\n"
            f"      <pubDate>{now}</pubDate>\n"
            "    </item>\n"
        )
    rss = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n'
        "  <channel>\n"
        f"    <title>{esc(BRAND)} 광명 출장마사지 · 홈타이</title>\n"
        f"    <link>{SITE_URL}/</link>\n"
        f"    <description>광명시 방문형 마사지·홈타이 지역별 예약 안내</description>\n"
        "    <language>ko</language>\n"
        f"    <lastBuildDate>{now}</lastBuildDate>\n"
        f'    <atom:link href="{SITE_URL}/rss.xml" rel="self" type="application/rss+xml" />\n'
        f"{''.join(items)}"
        "  </channel>\n"
        "</rss>\n"
    )
    with open(os.path.join(OUT, "rss.xml"), "w", encoding="utf-8") as f:
        f.write(rss)

    # ---- IndexNow 키 파일 ----
    with open(os.path.join(OUT, f"{INDEXNOW_KEY}.txt"), "w", encoding="utf-8") as f:
        f.write(INDEXNOW_KEY + "\n")

    # ---- robots.txt (네이버 Yeti·구글·빙 명시 허용 + 사이트맵) ----
    robots = (
        "# 모든 검색엔진 전체 허용\n"
        "User-agent: *\n"
        "Allow: /\n\n"
        "User-agent: Googlebot\n"
        "Allow: /\n\n"
        "User-agent: Yeti\n"            # 네이버 크롤러
        "Allow: /\n\n"
        "User-agent: bingbot\n"
        "Allow: /\n\n"
        f"Sitemap: {SITE_URL}/sitemap.xml\n"
        f"Sitemap: {SITE_URL}/rss.xml\n"
    )
    with open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots)

    print(f"\n총 {len(paths)}개 페이지 생성 완료.")
    print(f"sitemap.xml / rss.xml / robots.txt / {INDEXNOW_KEY}.txt 생성됨.")


if __name__ == "__main__":
    main()
