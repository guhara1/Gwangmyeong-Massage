#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google Indexing API 색인 통보 (구글은 IndexNow 미참여)

사전 준비(1회):
  1) Google Cloud 프로젝트에서 "Indexing API" 사용 설정
  2) 서비스 계정 생성 → JSON 키 다운로드
  3) Google Search Console에서 해당 사이트(또는 도메인 속성)의
     '소유자'로 서비스 계정 이메일을 추가
  4) 의존성 설치:  pip install google-auth requests

사용법:
  export GOOGLE_APPLICATION_CREDENTIALS=/path/service-account.json
  python3 google_indexing.py                # sitemap.xml의 모든 URL 제출
  python3 google_indexing.py /reservation/  # 특정 경로(여러 개 가능)

참고: 공식적으로 Indexing API는 JobPosting/BroadcastEvent 대상이지만,
URL_UPDATED 통보로 일반 페이지의 크롤 우선순위를 높이는 용도로 널리 쓰입니다.
일일 쿼터(기본 200건)가 있으니 변경된 URL만 보내는 것이 좋습니다.
"""
import sys
import os
import re

SCOPES = ["https://www.googleapis.com/auth/indexing"]
ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"

from build import SITE_URL  # noqa: E402


def sitemap_urls():
    path = os.path.join(os.path.dirname(__file__), "sitemap.xml")
    with open(path, encoding="utf-8") as f:
        return re.findall(r"<loc>(.*?)</loc>", f.read())


def to_url(arg):
    if arg.startswith("http"):
        return arg
    return SITE_URL + (arg if arg.startswith("/") else "/" + arg)


def main(argv):
    try:
        from google.oauth2 import service_account
        from google.auth.transport.requests import AuthorizedSession
    except ImportError:
        sys.exit("의존성 필요: pip install google-auth requests")

    cred_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not cred_path or not os.path.exists(cred_path):
        sys.exit("환경변수 GOOGLE_APPLICATION_CREDENTIALS 에 서비스 계정 JSON 경로를 지정하세요.")

    creds = service_account.Credentials.from_service_account_file(cred_path, scopes=SCOPES)
    session = AuthorizedSession(creds)

    urls = [to_url(a) for a in argv] if argv else sitemap_urls()
    print(f"Google Indexing API 제출: {len(urls)}개 URL")
    ok = 0
    for u in urls:
        r = session.post(ENDPOINT, json={"url": u, "type": "URL_UPDATED"}, timeout=30)
        status = "OK" if r.status_code == 200 else f"ERR {r.status_code}"
        if r.status_code == 200:
            ok += 1
        print(f"  [{status}] {u}")
        if r.status_code != 200:
            print("    ", r.text[:300])
    print(f"완료: {ok}/{len(urls)} 성공")


if __name__ == "__main__":
    main(sys.argv[1:])
