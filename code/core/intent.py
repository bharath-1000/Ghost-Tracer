"""
Multilingual intent detection engine for GHOST TRACER.
Identifies whether a request authorizes personal data deletion or represents
a non-deletion action (access, correction, opt-out, password reset, negation, or withdrawal).
Supports English, Spanish, Portuguese, French, Korean, and Japanese.
"""

import re
from typing import Dict, Any

# Explicit negation and withdrawal phrases (highest priority)
NEGATION_PATTERNS = [
    r"\bdo not delete\b",
    r"\bdon't delete\b",
    r"\bplease do not delete\b",
    r"\bno borrar\b",
    r"\bno borren\b",
    r"\bno eliminen\b",
    r"\bno apague\b",
    r"\bnão apague\b",
    r"\bnão exclua\b",
    r"\bne supprimez pas\b",
    r"\bne pas supprimer\b",
    r"삭제하지 마세요",
    r"삭제하지 마십시오",
    r"지우지 마세요",
    r"削除しないで",
    r"消さないで",
    r"\bwithdrew\b",
    r"\bwithdrawn\b",
    r"\bcancel my deletion\b",
    r"\bfoi um engano\b"
]

# Valid deletion verbs and intent markers across 6 languages
DELETION_PATTERNS = [
    r"\bdelete\b",
    r"\bdeletion\b",
    r"\berase\b",
    r"\beradicate\b",
    r"\bpurge\b",
    r"\bremove my customer account\b",
    r"\bremove my account\b",
    r"\bpermanently (erase|delete)\b",
    r"\bclose my account permanently\b",
    r"\bborrar\b",
    r"\bborrado\b",
    r"\bborren\b",
    r"\beliminar\b",
    r"\beliminen\b",
    r"\belimina\b",
    r"\beliminación\b",
    r"\bbaja de mi cuenta\b",
    r"\bexcluir\b",
    r"\bexclusão\b",
    r"\bsupprimer\b",
    r"\bsupprimez\b",
    r"\bsuppression\b",
    r"삭제",
    r"소멸",
    r"消去",
    r"削除"
]

# Pure non-deletion request patterns (Access, Marketing, Correction, Password Reset)
NON_DELETION_PATTERNS = [
    # Data access / export / copy
    r"\bsend me a copy\b",
    r"\bexport (my|all)?\b",
    r"\bdownload my data\b",
    r"\baccess to my personal data\b",
    r"\bcopia de (todos )?mis datos\b",
    r"\btélécharger mes données\b",
    r"\bdemande d'accès\b",
    r"데이터 사본",
    r"내역 사본",
    r"データのコピー",
    r"データのエクスポート",

    # Marketing opt-out only (without account deletion)
    r"\bunsubscribe\b",
    r"\bnewsletter\b",
    r"\bboletín de noticias\b",
    r"\be-mails de marketing apenas\b",
    r"配信を停止",
    r"수신 거부",

    # Correction / update
    r"\bmodifier mon adresse\b",
    r"\bactualicen mi\b",
    r"\bupdate my (shipping|payment|credit card|phone)\b",
    r"\bhow do i update\b",
    r"주소 변경",
    r"연락처 변경",
    r"情報の変更",
    r"クレジットカード情報を変更",

    # Password reset
    r"\breset (my )?password\b",
    r"\bpassword reset\b",
    r"비밀번호를 재설정",
    r"비밀번호 재설정",
    r"パスワードのリセット"
]

def detect_language(text: str) -> str:
    if re.search(r"[\uac00-\ud7a3]", text):
        return "ko"
    if re.search(r"[\u3040-\u30ff\u4e00-\u9faf]", text):
        return "ja"
    lower = text.lower()
    if any(w in lower for w in ["supprimer", "supprimez", "compte", "données", "s'il vous plaît"]):
        return "fr"
    if any(w in lower for w in ["excluir", "exclusão", "meu cadastro", "minha conta", "engano"]):
        return "pt"
    if any(w in lower for w in ["borrar", "eliminar", "eliminen", "cuenta", "boletín", "datos", "baja"]):
        return "es"
    return "en"

def classify_intent(text: str) -> Dict[str, Any]:
    if not text or not text.strip():
        return {
            "is_deletion": False,
            "intent_type": "UNKNOWN",
            "language": "en",
            "reason": "Empty request text"
        }

    lang = detect_language(text)
    clean_text = text.strip()

    # 1. Highest Priority: Check for explicit negation or withdrawal
    for pattern in NEGATION_PATTERNS:
        match = re.search(pattern, clean_text, re.IGNORECASE)
        if match:
            return {
                "is_deletion": False,
                "intent_type": "NEGATION",
                "language": lang,
                "matched_pattern": match.group(0),
                "reason": "Request contains explicit negation or withdrawal of deletion"
            }

    # 2. Check for explicit deletion intent
    has_deletion_intent = False
    deletion_match = None
    for pattern in DELETION_PATTERNS:
        match = re.search(pattern, clean_text, re.IGNORECASE)
        if match:
            has_deletion_intent = True
            deletion_match = match.group(0)
            break

    # 3. Check for non-deletion intents (e.g. data export, address update, newsletter opt-out)
    for pattern in NON_DELETION_PATTERNS:
        match = re.search(pattern, clean_text, re.IGNORECASE)
        if match:
            if has_deletion_intent and any(w in clean_text.lower() for w in ["account", "cadastro", "compte", "cuenta", "profile", "usuario"]):
                break
            return {
                "is_deletion": False,
                "intent_type": "NON_DELETION",
                "language": lang,
                "matched_pattern": match.group(0),
                "reason": "Request is for non-deletion action (data access, correction, marketing, or password)"
            }

    if has_deletion_intent:
        return {
            "is_deletion": True,
            "intent_type": "DELETION",
            "language": lang,
            "matched_pattern": deletion_match,
            "reason": "Authorized request for personal data erasure"
        }

    # Default fallback
    return {
        "is_deletion": False,
        "intent_type": "UNKNOWN",
        "language": lang,
        "reason": "No recognized deletion authorization keywords found"
    }
