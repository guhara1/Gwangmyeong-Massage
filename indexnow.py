#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IndexNow 즉시 색인 통보 (Bing · Naver · Yandex · Seznam 공유)

사용법:
  python3 indexnow.py                # sitemap.xml의 모든 URL 제출
  python3 indexnow.py /reservation/  # 특정 경로(여러 개 가능) 제출
  python3 indexnow.py https://.../  # 전체 URL 직접 지정도 가능

의존성 없음(표준 라이브러리만 사용). 글을 올리거나 페이지를 수정한 뒤 실행하면
변경 URL을 검색엔진에 즉시 통보합니다.
"""
import sys
import os
import json
import re
import urllib.request

from build import SITE_URL, INDEXNOW_KEY

ENDPOINT = "https://api.indexnow.org/indexnow"
HOST = re.sub(r"^https?://", "", SITE_URL).rstrip("/")
KEY_LOCATION = f"{SITE_URL}/{INDEXNOW_KEY}.txt"


def sitemap_urls():
    path = os.path.join(os.path.dirname(__file__), "sitemap.xml")
    with open(path, encoding="utf-8") as f:
        return re.findall(r"<loc>(.*?)</loc>", f.read())


def to_url(arg):
    if arg.startswith("http"):
        return arg
    return SITE_URL + (arg if arg.startswith("/") else "/" + arg)


def main(argv):
    urls = [to_url(a) for a in argv] if argv else sitemap_urls()
    payload = {
        "host": HOST,
        "key": INDEXNOW_KEY,
        "keyLocation": KEY_LOCATION,
        "urlList": urls,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        ENDPOINT, data=data,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    print(f"IndexNow 제출: {len(urls)}개 URL → {ENDPOINT}")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            print(f"응답: HTTP {resp.status} {resp.reason}")
            # 200/202 = 성공 접수
    except urllib.error.HTTPError as e:
        print(f"HTTP 오류: {e.code} {e.reason}\n{e.read().decode('utf-8','ignore')}")
        sys.exit(1)
    except Exception as e:
        print(f"오류: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
