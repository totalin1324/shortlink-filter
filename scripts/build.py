#!/usr/bin/env python3
"""필터 정리 + 버전 헤더 자동 갱신.

사용: python3 scripts/build.py shortlink_filter.txt [excluded.txt]
- 규칙을 소문자로 통일하고, 구역(본문 주석 사이)별로 정렬하고, 전체 중복을 제거한다.
- 형식이 틀린 줄이 있으면 줄 번호와 함께 실패한다.
- excluded.txt가 있으면 거기 적힌 도메인은 필터에서 뺀다.
- 규칙이 실제로 바뀐 경우에만 `! Version:` / `! Last modified:` 를 갱신한다.
"""
import hashlib
import os
import re
import sys
from datetime import datetime, timedelta, timezone

DOMAIN = r"(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z]{2,}"
RULE_HOST = re.compile(rf"^\|\|({DOMAIN})\^\$all$")
RULE_URL = re.compile(rf"^\|https?://({DOMAIN})/\$all$")
MANAGED = ("! version:", "! last modified:", "! checksum-rules:")


def rule_domain(rule):
    m = RULE_HOST.match(rule) or RULE_URL.match(rule)
    return m.group(1) if m else None


def main():
    path = sys.argv[1]
    excl_path = sys.argv[2] if len(sys.argv) > 2 else "excluded.txt"
    lines = open(path, encoding="utf-8").read().splitlines()

    excluded = set()
    if os.path.exists(excl_path):
        for l in open(excl_path, encoding="utf-8"):
            l = l.split("#")[0].strip().lower()
            if l:
                excluded.add(l)

    # 맨 위 연속된 주석 = 헤더
    i = 0
    header = []
    old_sum = None
    while i < len(lines) and (lines[i].startswith("!") or not lines[i].strip()):
        l = lines[i].rstrip()
        if l.lower().startswith("! checksum-rules:"):
            old_sum = l.split(":", 1)[1].strip()
        if l and not l.lower().startswith(MANAGED) and l != "!":
            header.append(l)
        i += 1

    # 본문: 주석을 만나면 새 구역
    sections = [[None, []]]
    seen = set()
    errors = []
    for n, raw in enumerate(lines[i:], start=i + 1):
        l = raw.strip()
        if not l:
            continue
        if l.startswith("!"):
            sections.append([l, []])
            continue
        l = l.lower()
        d = rule_domain(l)
        if d is None:
            errors.append(f"  {n}번 줄: {raw}")
            continue
        if d in excluded or l in seen:
            continue
        seen.add(l)
        sections[-1][1].append(l)

    if errors:
        print("형식이 잘못된 규칙:\n" + "\n".join(errors))
        sys.exit(1)

    body = []
    for title, rules in sections:
        if title:
            body.append(title)
        body += sorted(rules, key=lambda r: (rule_domain(r), r))

    rules_only = [b for b in body if not b.startswith("!")]
    new_sum = hashlib.sha1("\n".join(rules_only).encode()).hexdigest()[:12]

    if new_sum == old_sum:
        # 규칙 변화 없음: 버전은 그대로 두고 정리만
        keep = [l.rstrip() for l in lines[:i] if l.lower().startswith(MANAGED)]
    else:
        now = datetime.now(timezone(timedelta(hours=9)))  # KST
        keep = [
            f"! Version: {now:%Y.%m.%d.%H%M}",
            f"! Last modified: {now:%Y-%m-%d %H:%M} KST",
            f"! Checksum-rules: {new_sum}",
        ]

    out = header + keep + ["!"] + body
    open(path, "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")
    print(f"규칙 {len(rules_only)}개, 버전 {'유지' if new_sum == old_sum else '갱신'}")


if __name__ == "__main__":
    main()
