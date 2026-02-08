# # backend/features/chat/prompts.py

# from langchain_core.prompts import PromptTemplate

# # Rewrite: 출력 길이 강제
# REWRITE_PROMPT = PromptTemplate(
#     template="""검색어 최적화 봇입니다.

# [대화]
# {history}

# [질문]
# {question}

# **중요 규칙:**
# 1. 출력은 **반드시 1-5단어** 이내
# 2. 조사, 어미 제거 (예: "을", "를", "해줘", "먹고싶다")
# 3. 핵심 요리명만 추출
# 4. 예시:
#    - "두쫀쿠 먹고싶다" → "두쫀쿠"
#    - "김치찌개 만드는 법 알려줘" → "김치찌개"
#    - "더 매운 걸로" → "매운 김치찌개" (대화에서 김치찌개 언급됨)

# **출력 (단어만, 설명 금지):**""",
#     input_variables=["history", "question"]
# )

# GRADE_PROMPT = PromptTemplate(
#     template="""[질문] {question}
# [문서] {context}

# 질문의 핵심 요리명이 문서 제목에 정확히 있으면 'yes', 아니면 'no'.
# 답변은 'yes' 또는 'no' 단 한 단어만:""",
#     input_variables=["question", "context"]
# )


# GENERATE_PROMPT = PromptTemplate(
#     template="""검색 결과 요약 봇입니다. 검색 결과만 사용하고, 절대 재작성하지 마세요!

# [검색 결과]
# {context}

# [대화]
# {history}

# [질문]
# {question}

# **올바른 예시:**
# 검색 결과: "재료: 카다이프 150g, 피스타치오 크림 50g"
# → 출력: **재료:** 카다이프 150g, 피스타치오 크림 50g

# **잘못된 예시 (금지!):**
# 검색 결과: "재료: 카다이프 150g"
# → 출력: **재료:** 밀가루 200g, 계란 2개 (❌ 검색 결과에 없음!)

# **규칙:**
# 1. 검색 결과의 재료명을 **정확히 그대로** 복사해서 사용하되, 알레르기/비선호 재료는 **자동 제외**
# 2. 없는 재료 추가 절대 금지
# 3. 재료명 변경 절대 금지
# 4. 컨텍스트 첫 부분에 "알레르기 재료" 또는 "비선호 음식"이 있으면 **절대 사용 금지**
# 5. 알레르기 재료가 포함된 레시피면 **다른 레시피 선택** 또는 **대체 재료 제안**

# **출력:**
# **[요리명]**
# ⏱️ XX분 | 📊 난이도 | 👥 X인분
# **소개:** 한 문장
# **재료:** 검색 결과 재료 그대로 (쉼표로 나열, 5-7개, 알레르기/비선호 재료 제외)

# 답변:""",
#     input_variables=["context", "history", "question"]
# )

# backend/features/chat/prompts.py

from langchain_core.prompts import PromptTemplate

REWRITE_PROMPT = PromptTemplate(
    template="""[대화]
{history}

[질문]
{question}

**요리명 1-5단어 (조사 제거):**""",
    input_variables=["history", "question"]
)

GRADE_PROMPT = PromptTemplate(
    template="""질문: {question}
문서: {context}

요리명 매칭? yes/no:""",
    input_variables=["question", "context"]
)

GENERATE_PROMPT = PromptTemplate(
    template="""[검색 결과]
{context}

[질문]
{question}

{modification_constraints}

# 규칙
- 출력 개수: "여러/많이/추천/N개" 없으면 1개만
- 인원수: {servings}인분 (재료 양도 {servings}인분 기준)
- 재료: 쉼표 나열, 줄바꿈 금지, 양 필수
- 금지어: 데코, 토핑, 적당량, 취향껏, 약간
- "제외:" 재료, 알레르기/비선호 재료 사용 금지
- 소개: 객관적 포멀 (금지: 이모티콘, ~, 알려드릴게요)
- 조리법 출력 금지

# 출력 형식 (정확히 따를 것)
**[요리명]**
⏱️ XX분 | 📊 난이도 | 👥 {servings}인분
**소개:** 객관적 1줄
**재료:** 재료1 양, 재료2 양 (한 줄, 쉼표 구분)

# 예시
**[딸기 케이크]**
⏱️ 30분 | 📊 초급 | 👥 {servings}인분
**소개:** 딸기와 생크림을 활용한 디저트 케이크.
**재료:** 딸기 300g, 생크림 200ml, 설탕 50g

답변:""",
    input_variables=["context", "history", "question", "servings", "modification_constraints"]
)