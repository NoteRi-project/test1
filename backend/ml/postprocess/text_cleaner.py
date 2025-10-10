# backend/ml/postprocess/text_cleaner.py (교체/추가용)

import re
from typing import Dict, List, Tuple
from dataclasses import dataclass

@dataclass
class CleanerConfig:
    ngram_size: int = 3
    min_word_run: int = 2              # 같은 단어 반복 최소 횟수
    filler_min_run: int = 2            # 필러 최소 반복 횟수
    max_char_run: int = 2              # 같은 글자 연속 허용 최대 (가~~~→가~)
    replacements: Dict[str, str] = None
    fillers: List[str] = None

def _default_replacements():
    return {
        # 오인식 교정(도메인 별로 계속 보강해)
        "규댓성": "휴대성",
        "규덷성": "휴대성",
        "파워치": "파우치",
        "파워치형": "파우치형",
        "환경치나적": "환경 친화적",
        "환경치나적으로": "환경 친화적으로",
        "소 소재": "소재",
        "마켓 팀": "마케팅팀",
        "마켓팀": "마케팅팀",
        "스토리텔": "스토리텔링",
        # 형태 변화들
        "ESG 키워드를 정 정말로": "ESG 키워드를 정말",
        "너무 너무나도": "너무",
    }

def _default_fillers():
    return [
        "음", "어", "어어", "에", "그", "약간", "뭔가", "그러니까", "이제",
        "뭐랄까", "그러면서", "그니까", "약간은",
    ]

class TextCleaner:
    def __init__(self, stopwords=None, ngram_size=3, config: CleanerConfig=None):
        self.stopwords = stopwords or ["감사합니다"]
        self.ngram_size = ngram_size
        self.cfg = config or CleanerConfig(
            ngram_size=ngram_size,
            replacements=_default_replacements(),
            fillers=_default_fillers(),
        )

    # 문자 반복 줄이기: 가~~~~~ → 가~~ (max_char_run)
    def remove_char_runs(self, text: str) -> str:
        n = max(1, self.cfg.max_char_run)
        return re.sub(rf'(.)\1{{{n},}}', r'\1' * n, text)

    # 단어 반복 줄이기: "가만히 가만히 가만히" → "가만히"
    def remove_word_runs(self, text: str) -> str:
        # 연속 동일 단어가 cfg.min_word_run 이상 반복되면 1개로
        pattern = re.compile(r'(\b[\w가-힣]+\b)(?:\s+\1){%d,}' % (self.cfg.min_word_run - 1))
        return pattern.sub(r'\1', text)

    # 필러(군더더기) 반복 제거: "음 음 음" → "음" 또는 제거
    def remove_filler_runs(self, text: str) -> str:
        for f in self.cfg.fillers:
            pattern = re.compile(
                r'(?:\b{}\b[\s]*){{{},}}'.format(re.escape(f), self.cfg.filler_min_run),
                re.IGNORECASE
            )
            text = pattern.sub('', text)
        return text

    # 불용어 제거
    def remove_stopwords(self, text: str) -> str:
        for sw in self.stopwords:
            text = re.sub(rf'\b{re.escape(sw)}\b', '', text)
        return text

    # n-gram 반복 제거 (네가 가진 로직 유지)
    def remove_ngram_repeats(self, text: str, n: int = None) -> str:
        if n is None:
            n = self.ngram_size
        tokens = text.split()
        if len(tokens) < n * 2:
            return text
        out, i = [], 0
        while i < len(tokens):
            out.append(tokens[i])
            if i >= n and i + n <= len(tokens):
                prev_ngram = tokens[i-n+1:i+1]
                next_ngram = tokens[i+1:i+1+n]
                if prev_ngram == next_ngram:
                    i += n
                    continue
            i += 1
        return " ".join(out)

    # 사전 기반 치환 (공백/조사 영향 줄이게 폭넓게 처리)
    def apply_replacements(self, text: str) -> str:
        for k, v in (self.cfg.replacements or {}).items():
            text = re.sub(rf'\b{re.escape(k)}\b', v, text)
            text = text.replace(k, v)  # 안전망
        return text

    # 문장 부호/공백 정규화
    def normalize_spaces_punct(self, text: str) -> str:
        text = re.sub(r"[?!.]{2,}", ".", text)    # ..?!.. → .
        text = re.sub(r"\s{2,}", " ", text)       # 여러 공백 → 1칸
        text = re.sub(r"\s+([,\.])", r"\1", text) # 쉼표/마침표 앞 공백 제거
        text = re.sub(r"\s*([,])\s*", r", ", text)# 쉼표 주변 정리
        return text.strip()

    def clean(self, text: str) -> str:
        if not text:
            return ""
        t = text.strip()
        t = re.sub(r"\.{2,}", "", t)  # 연속점 제거
        t = self.remove_char_runs(t)
        t = self.remove_word_runs(t)
        t = self.remove_ngram_repeats(t)
        t = self.remove_filler_runs(t)
        t = self.apply_replacements(t)
        t = self.remove_stopwords(t)
        t = self.normalize_spaces_punct(t)
        return t
