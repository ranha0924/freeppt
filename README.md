# 통합과학 LAB — 소개 발표자료

[**통합과학 LAB**](https://free-fall-experiment.vercel.app/)(“만지는 과학 실험실”) 서비스를 소개하는 웹 슬라이드 **12장**.
사이트와 똑같은 **흑백 레트로 매킨토시 감성 + Galmuri 픽셀 폰트**로 만들었고, 실제 화면 스크린샷이 들어 있습니다.

## 보기 / 발표

- **`index.html`** 을 브라우저로 열면 바로 실행됩니다. (폰트·이미지·QR이 모두 내장된 **자기완결형 단일 파일** — 오프라인·자체 호스팅 OK)
- 넘기기: **← / →**, **Space**, 화면 **클릭**, 하단 **◀ ▶** 버튼

## 구성 (12장)

1. 표지 · 통합과학 LAB
2. 왜 ‘만지는’ 실험실인가
3. 첫인상 — 레트로 Mac 데스크톱
4. 쓰는 법 — 개념 → 체험 → 퀴즈
5. 실험 라인업 — 3단원 10실험
6. 하이라이트 — 자유낙하(실제 물리엔진 + v-t 그래프)
7. 하이라이트 — 3D DNA · 원소 선 스펙트럼 · 별의 진화
8. 교육적 설계 — 교과서 연계 · 시험 포인트 · 오답 해설
9. 차별점 — 교사 AI 저작 파이프라인
10. 교사가 직접 만들기 — 개념 저작 화면
11. 지금 열어보기 — URL · QR
12. 마무리

## 수정 · 다시 빌드

슬라이드 문구/구성은 템플릿 `src/deck.src.html` 에서 고치고 다시 빌드합니다.

```bash
pip install fonttools brotli "qrcode[pil]"

# Galmuri 폰트 4종을 src/fonts/ 에 둔다 (용량이 커서 git 미포함)
npm pack galmuri && tar xf galmuri-*.tgz
cp package/dist/{Galmuri11.ttf,Galmuri11-Bold.ttf,Galmuri14.ttf,GalmuriMono11.ttf} src/fonts/

python src/build.py        # → index.html 생성
```

빌드 스크립트(`src/build.py`)는 사용된 글자만 서브셋한 woff2 폰트, `src/assets/`의 스크린샷, QR 코드를 모두 data URI로 인라인 삽입합니다.

### 폴더 구조

```
index.html            자기완결형 최종 발표덱 (배포/발표용)
src/
  deck.src.html       슬라이드 템플릿 (플레이스홀더 포함)
  build.py            폰트 서브셋 · 이미지/QR 인라인 → index.html
  assets/*.png        실제 화면 스크린샷
  fonts/              Galmuri TTF 4종 (git 미포함 — 위 안내대로 준비)
```

## 폰트

[Galmuri](https://github.com/quiple/galmuri) © quiple, [SIL Open Font License](https://openfontlicense.org/) — npm 패키지 `galmuri`.
