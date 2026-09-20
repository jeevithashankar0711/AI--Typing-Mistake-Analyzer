import language_tool_python
tool = language_tool_python.LanguageTool("en-US")
def check_spelling(text):
    mistakes = []
    matches = tool.check(text)
    for match in matches:
        if match.rule_issue_type != "misspelling":
            continue
        wrong = text[
            match.offset:
            match.offset + match.error_length
        ]
        if wrong.lower() == "i":
            continue
        if wrong.isupper():
            continue
        if wrong and wrong[0].isupper():
            continue
        suggestions = match.replacements[:3]
        mistakes.append({
            "wrong": wrong,
            "suggestions": suggestions
        })
    return mistakes