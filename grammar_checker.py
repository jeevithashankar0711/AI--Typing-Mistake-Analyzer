import re
def check_grammar(text):
    mistakes = []
    pattern = r"\bi\b"
    for match in re.finditer(pattern, text):
        mistakes.append({
            "wrong": "i",
            "suggestions": ["I"],
            "message": "The pronoun 'I' must be capitalized.",
            "offset": match.start()
        })
    pattern = r"\b[Ii]\s+(has)\b"
    for match in re.finditer(pattern, text):
        mistakes.append({
            "wrong": match.group(1),
            "suggestions": ["have"],
            "message": "Use 'have' with 'I'.",
            "offset": match.start(1)
        })
    pattern = r"\b(He|She|It)\s+(go)\b"
    for match in re.finditer(pattern, text):
        mistakes.append({
            "wrong": match.group(2),
            "suggestions": ["goes"],
            "message": "Use 'goes' with He, She or It.",
            "offset": match.start(2)
        })
    pattern = r"\b(They|they)\s+(was)\b"
    for match in re.finditer(pattern, text):
        mistakes.append({
            "wrong": match.group(2),
            "suggestions": ["were"],
            "message": "Use 'were' with They.",
            "offset": match.start(2)
        })
    pattern = r"\b(He|She|It)\s+(are)\b"
    for match in re.finditer(pattern, text):
        mistakes.append({
            "wrong": match.group(2),
            "suggestions": ["is"],
            "message": "Use 'is' with He, She or It.",
            "offset": match.start(2)
        })
    return mistakes