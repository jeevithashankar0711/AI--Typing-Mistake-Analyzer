from spelling_checker import check_spelling
from grammar_checker import check_grammar
def analyze_text(text):
    spelling_mistakes = check_spelling(text)
    grammar_mistakes = check_grammar(text)
    spelling_count = len(spelling_mistakes)
    grammar_count = len(grammar_mistakes)
    total_mistakes = spelling_count + grammar_count
    return {
        "spelling": spelling_mistakes,
        "grammar": grammar_mistakes,
        "spelling_count": spelling_count,
        "grammar_count": grammar_count,
        "total_mistakes": total_mistakes
    }
