# Shortlink Blocklist

단축 URL(숏링크), IP 로거, 사칭 도메인을 차단하는 AdGuard / uBlock Origin용 필터입니다.

## 구독

AdGuard 설정 → 필터 → 사용자 정의 → 사용자 정의 필터 추가에 아래 주소를 넣습니다.

```
https://raw.githubusercontent.com/totalin1324/shortlink-filter/main/shortlink_filter.txt
```

"신뢰할 수 있는 필터" 체크는 필요 없습니다.

## 왜 막는가

- 클릭 전까지 목적지가 보이지 않아 피싱·스팸에 쓰입니다.
- 중간 서버가 클릭 시각, IP, 기기 정보를 수집합니다.
- 일부는 목적지 앞에 광고 페이지를 끼워 넣습니다.

## 포함 기준

| 구분 | 기준 | 예 |
|---|---|---|
| 포함 | 임의의 목적지로 보낼 수 있는 단축 서비스 | `bit.ly`, `t.co`, `me2.do` |
| 포함 | IP 로거와 그 별칭 도메인 | `iplogger.org`, `grabify.link` |
| 포함 | 유명 서비스 사칭 도메인 | `alliexpress.kr`, `teiegram.kr` |
| 제외 | 목적지가 자사로 고정된 단축 도메인 | `fb.me`, `wp.me`, `nyti.ms` |
| 제외 | 리다이렉터가 아닌 일반 서비스 | `t.me`, `linktr.ee`, `name.com` |
| 제외 | 무료 호스팅·서브도메인 제공처 | `x10.mx`, `cjb.net` |

`goo.gl`은 본 도메인만 차단하고 `maps.app.goo.gl` 등 서브도메인은 허용합니다.

## 규칙 형식

- 한 줄에 도메인 하나: `||example.com^$all`
- 전부 소문자, 알파벳순 정렬, 중복 없음

## 오차단 제보 / 추가 요청

Issues에 도메인과 근거(어디서 봤는지, 어떤 페이지가 막히는지)를 적어 주세요.

## 변경 이력

- 2026-11-17: 최초 공개 (898개 규칙)
