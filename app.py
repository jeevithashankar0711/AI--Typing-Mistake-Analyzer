import tkinter as tk
import time
from ai_analyzer import analyze_text


start_time = None


# ==================================================
# TIMER
# ==================================================

def start_timer(event=None):

    global start_time

    if start_time is None:
        start_time = time.time()


# ==================================================
# HIGHLIGHT MISTAKES
# ==================================================

def highlight_mistakes(text, result):

    text_box.tag_remove("spelling", "1.0", tk.END)
    text_box.tag_remove("grammar", "1.0", tk.END)

    # ---------------- SPELLING ----------------

    for mistake in result["spelling"]:

        wrong = mistake["wrong"]

        start = "1.0"

        while True:

            position = text_box.search(
                wrong,
                start,
                stopindex=tk.END
            )

            if not position:
                break

            end = f"{position}+{len(wrong)}c"

            text_box.tag_add(
                "spelling",
                position,
                end
            )

            start = end

    # ---------------- GRAMMAR ----------------

    for mistake in result["grammar"]:

        wrong = mistake["wrong"]

        if not wrong.strip():
            continue

        start = "1.0"

        while True:

            position = text_box.search(
                wrong,
                start,
                stopindex=tk.END
            )

            if not position:
                break

            end = f"{position}+{len(wrong)}c"

            text_box.tag_add(
                "grammar",
                position,
                end
            )

            start = end


# ==================================================
# TYPING LEVEL
# ==================================================

def get_typing_level(wpm, accuracy):

    if accuracy >= 90 and wpm >= 40:
        return "Excellent"

    elif accuracy >= 80 and wpm >= 30:
        return "Good"

    elif accuracy >= 70:
        return "Average"

    else:
        return "Needs Improvement"


# ==================================================
# CREATE DASHBOARD CARD
# ==================================================

def create_card(parent, title, value, row, column):

    card = tk.Frame(
        parent,
        bg="white",
        bd=1,
        relief="solid",
        width=180,
        height=90
    )

    card.grid(
        row=row,
        column=column,
        padx=8,
        pady=8,
        sticky="nsew"
    )

    card.grid_propagate(False)

    title_label = tk.Label(
        card,
        text=title,
        font=("Arial", 10),
        bg="white",
        fg="#6b7280"
    )

    title_label.pack(
        pady=(12, 3)
    )

    value_label = tk.Label(
        card,
        text=value,
        font=("Arial", 18, "bold"),
        bg="white",
        fg="#2563eb"
    )

    value_label.pack()


# ==================================================
# ANALYZE
# ==================================================

def analyze():

    global start_time

    text = text_box.get(
        "1.0",
        tk.END
    ).strip()

    if not text:

        result_box.delete(
            "1.0",
            tk.END
        )

        result_box.insert(
            tk.END,
            "Please enter some text."
        )

        return

    if start_time is None:
        start_time = time.time()

    # ==================================================
    # TIME
    # ==================================================

    elapsed_time = time.time() - start_time

    # ==================================================
    # WORD COUNT
    # ==================================================

    words = text.split()

    word_count = len(words)

    # ==================================================
    # WPM
    # ==================================================

    minutes = elapsed_time / 60

    if minutes > 0:

        wpm = word_count / minutes

    else:

        wpm = 0

    # ==================================================
    # AI ANALYSIS
    # ==================================================

    result = analyze_text(text)

    spelling_mistakes = result["spelling"]

    grammar_mistakes = result["grammar"]

    spelling_count = len(spelling_mistakes)

    grammar_count = len(grammar_mistakes)

    total_mistakes = (
        spelling_count +
        grammar_count
    )

    # ==================================================
    # ACCURACY
    # ==================================================

    if word_count > 0:

        correct_words = max(
            0,
            word_count - total_mistakes
        )

        accuracy = (
            correct_words /
            word_count
        ) * 100

    else:

        accuracy = 0

    # ==================================================
    # TYPING LEVEL
    # ==================================================

    typing_level = get_typing_level(
        wpm,
        accuracy
    )

    # ==================================================
    # HIGHLIGHT
    # ==================================================

    highlight_mistakes(
        text,
        result
    )

    # ==================================================
    # UPDATE DASHBOARD
    # ==================================================

    accuracy_value.config(
        text=f"{accuracy:.1f}%"
    )

    wpm_value.config(
        text=f"{wpm:.1f}"
    )

    mistake_value.config(
        text=str(total_mistakes)
    )

    level_value.config(
        text=typing_level
    )

    spelling_value.config(
        text=str(spelling_count)
    )

    grammar_value.config(
        text=str(grammar_count)
    )

    # ==================================================
    # ERROR ANALYSIS
    # ==================================================

    if spelling_count > grammar_count:

        common_error = "Spelling"

    elif grammar_count > spelling_count:

        common_error = "Grammar"

    elif spelling_count == 0 and grammar_count == 0:

        common_error = "No Errors"

    else:

        common_error = "Both"

    if total_mistakes == 0:

        suggestion = (
            "Excellent! No spelling or grammar "
            "mistakes were detected."
        )

    elif spelling_count > grammar_count:

        suggestion = (
            "Focus on spelling and careful typing "
            "to improve accuracy."
        )

    elif grammar_count > spelling_count:

        suggestion = (
            "Focus on sentence structure and "
            "basic grammar rules."
        )

    else:

        suggestion = (
            "Practice both spelling and grammar "
            "to improve your accuracy."
        )

    # ==================================================
    # CLEAR RESULT
    # ==================================================

    result_box.delete(
        "1.0",
        tk.END
    )

    # ==================================================
    # PERFORMANCE
    # ==================================================

    result_box.insert(
        tk.END,
        "TYPING PERFORMANCE\n",
        "heading"
    )

    result_box.insert(
        tk.END,
        "==================\n\n"
    )

    result_box.insert(
        tk.END,
        f"Word Count      : {word_count}\n"
        f"Time Taken      : {elapsed_time:.1f} seconds\n"
        f"WPM             : {wpm:.1f}\n"
        f"Accuracy        : {accuracy:.1f}%\n"
        f"Total Mistakes  : {total_mistakes}\n\n"
    )

    # ==================================================
    # ERROR ANALYSIS
    # ==================================================

    result_box.insert(
        tk.END,
        "ERROR ANALYSIS\n",
        "heading"
    )

    result_box.insert(
        tk.END,
        "==============\n\n"
    )

    result_box.insert(
        tk.END,
        f"Spelling Errors : {spelling_count}\n"
        f"Grammar Errors  : {grammar_count}\n"
        f"Total Errors    : {total_mistakes}\n"
        f"Most Common     : {common_error}\n\n"
    )

    # ==================================================
    # IMPROVEMENT
    # ==================================================

    result_box.insert(
        tk.END,
        "IMPROVEMENT SUGGESTION\n",
        "heading"
    )

    result_box.insert(
        tk.END,
        "======================\n\n"
    )

    result_box.insert(
        tk.END,
        suggestion + "\n\n"
    )

    # ==================================================
    # CORRECTION REPORT
    # ==================================================

    result_box.insert(
        tk.END,
        "CORRECTION REPORT\n",
        "heading"
    )

    result_box.insert(
        tk.END,
        "=================\n\n"
    )

    # ==================================================
    # SPELLING
    # ==================================================

    result_box.insert(
        tk.END,
        "SPELLING MISTAKES\n",
        "subheading"
    )

    result_box.insert(
        tk.END,
        "-----------------\n\n"
    )

    if spelling_mistakes:

        count = 1

        for mistake in spelling_mistakes:

            wrong = mistake["wrong"]

            suggestions = mistake["suggestions"]

            result_box.insert(
                tk.END,
                f"{count}. Wrong Word : {wrong}\n"
            )

            if suggestions:

                result_box.insert(
                    tk.END,
                    "   Suggestions : "
                    + ", ".join(suggestions)
                    + "\n\n"
                )

            else:

                result_box.insert(
                    tk.END,
                    "   Suggestions : No suggestion\n\n"
                )

            count += 1

    else:

        result_box.insert(
            tk.END,
            "No spelling mistakes.\n\n"
        )

    # ==================================================
    # GRAMMAR
    # ==================================================

    result_box.insert(
        tk.END,
        "GRAMMAR MISTAKES\n",
        "subheading"
    )

    result_box.insert(
        tk.END,
        "----------------\n\n"
    )

    if grammar_mistakes:

        count = 1

        for mistake in grammar_mistakes:

            wrong = mistake["wrong"]

            suggestions = mistake["suggestions"]

            message = mistake.get(
                "message",
                ""
            )

            result_box.insert(
                tk.END,
                f"{count}. Wrong : {wrong}\n"
            )

            if suggestions:

                result_box.insert(
                    tk.END,
                    "   Correction : "
                    + suggestions[0]
                    + "\n"
                )

            if message:

                result_box.insert(
                    tk.END,
                    "   Reason     : "
                    + message
                    + "\n"
                )

            result_box.insert(
                tk.END,
                "\n"
            )

            count += 1

    else:

        result_box.insert(
            tk.END,
            "No grammar mistakes.\n\n"
        )


# ==================================================
# CLEAR ALL
# ==================================================

def clear_all():

    global start_time

    text_box.delete(
        "1.0",
        tk.END
    )

    result_box.delete(
        "1.0",
        tk.END
    )

    text_box.tag_remove(
        "spelling",
        "1.0",
        tk.END
    )

    text_box.tag_remove(
        "grammar",
        "1.0",
        tk.END
    )

    # Reset dashboard

    accuracy_value.config(
        text="--"
    )

    wpm_value.config(
        text="--"
    )

    mistake_value.config(
        text="--"
    )

    level_value.config(
        text="--"
    )

    spelling_value.config(
        text="--"
    )

    grammar_value.config(
        text="--"
    )

    start_time = None


# ==================================================
# MAIN WINDOW
# ==================================================

window = tk.Tk()

window.title(
    "AI Typing Mistake Analyzer"
)

window.geometry(
    "1000x900"
)

window.configure(
    bg="#f4f6f8"
)


# ==================================================
# TITLE
# ==================================================

title = tk.Label(
    window,
    text="AI Typing Mistake Analyzer",
    font=("Arial", 24, "bold"),
    bg="#f4f6f8",
    fg="#1f2937"
)

title.pack(
    pady=(20, 5)
)


subtitle = tk.Label(
    window,
    text="AI-powered spelling, grammar and typing performance analysis",
    font=("Arial", 11),
    bg="#f4f6f8",
    fg="#6b7280"
)

subtitle.pack(
    pady=(0, 15)
)


# ==================================================
# DASHBOARD FRAME
# ==================================================

dashboard_frame = tk.Frame(
    window,
    bg="#f4f6f8"
)

dashboard_frame.pack(
    padx=30,
    pady=5,
    fill="x"
)


# ==================================================
# DASHBOARD TITLE
# ==================================================

dashboard_title = tk.Label(
    dashboard_frame,
    text="Performance Dashboard",
    font=("Arial", 15, "bold"),
    bg="#f4f6f8",
    fg="#1f2937"
)

dashboard_title.grid(
    row=0,
    column=0,
    columnspan=3,
    pady=(5, 5)
)


# ==================================================
# DASHBOARD CARDS
# ==================================================

create_card(
    dashboard_frame,
    "Accuracy",
    "--",
    1,
    0
)

create_card(
    dashboard_frame,
    "WPM",
    "--",
    1,
    1
)

create_card(
    dashboard_frame,
    "Total Mistakes",
    "--",
    1,
    2
)

create_card(
    dashboard_frame,
    "Typing Level",
    "--",
    2,
    0
)

create_card(
    dashboard_frame,
    "Spelling Errors",
    "--",
    2,
    1
)

create_card(
    dashboard_frame,
    "Grammar Errors",
    "--",
    2,
    2
)


# ==================================================
# GET CARD VALUE LABELS
# ==================================================

cards = dashboard_frame.winfo_children()

# Card indexes:
# 1 = Accuracy
# 2 = WPM
# 3 = Total Mistakes
# 4 = Typing Level
# 5 = Spelling Errors
# 6 = Grammar Errors

accuracy_value = cards[1].winfo_children()[1]
wpm_value = cards[2].winfo_children()[1]
mistake_value = cards[3].winfo_children()[1]

level_value = cards[4].winfo_children()[1]
spelling_value = cards[5].winfo_children()[1]
grammar_value = cards[6].winfo_children()[1]


# ==================================================
# INPUT FRAME
# ==================================================

input_frame = tk.Frame(
    window,
    bg="white",
    bd=1,
    relief="solid"
)

input_frame.pack(
    padx=30,
    pady=10,
    fill="x"
)


input_label = tk.Label(
    input_frame,
    text="Enter Your Text",
    font=("Arial", 13, "bold"),
    bg="white",
    fg="#1f2937"
)

input_label.pack(
    anchor="w",
    padx=15,
    pady=(15, 5)
)


text_box = tk.Text(
    input_frame,
    height=9,
    font=("Arial", 12),
    wrap="word",
    bd=0
)

text_box.pack(
    padx=15,
    pady=(0, 15),
    fill="x"
)


text_box.bind(
    "<KeyPress>",
    start_timer
)


# ==================================================
# HIGHLIGHT COLORS
# ==================================================

text_box.tag_configure(
    "spelling",
    foreground="red",
    underline=True
)

text_box.tag_configure(
    "grammar",
    foreground="orange",
    underline=True
)


# ==================================================
# BUTTON FRAME
# ==================================================

button_frame = tk.Frame(
    window,
    bg="#f4f6f8"
)

button_frame.pack(
    pady=10
)


# ==================================================
# ANALYZE BUTTON
# ==================================================

analyze_button = tk.Button(
    button_frame,
    text="Analyze Text",
    font=("Arial", 12, "bold"),
    bg="#2563eb",
    fg="white",
    padx=25,
    pady=8,
    bd=0,
    command=analyze
)

analyze_button.pack(
    side="left",
    padx=8
)


# ==================================================
# CLEAR BUTTON
# ==================================================

clear_button = tk.Button(
    button_frame,
    text="Clear",
    font=("Arial", 12, "bold"),
    bg="#6b7280",
    fg="white",
    padx=30,
    pady=8,
    bd=0,
    command=clear_all
)

clear_button.pack(
    side="left",
    padx=8
)


# ==================================================
# RESULT FRAME
# ==================================================

result_frame = tk.Frame(
    window,
    bg="white",
    bd=1,
    relief="solid"
)

result_frame.pack(
    padx=30,
    pady=10,
    fill="both",
    expand=True
)


result_label = tk.Label(
    result_frame,
    text="Detailed Analysis Report",
    font=("Arial", 13, "bold"),
    bg="white",
    fg="#1f2937"
)

result_label.pack(
    anchor="w",
    padx=15,
    pady=(15, 5)
)


# ==================================================
# SCROLLBAR
# ==================================================

scrollbar = tk.Scrollbar(
    result_frame
)

scrollbar.pack(
    side="right",
    fill="y"
)


# ==================================================
# RESULT BOX
# ==================================================

result_box = tk.Text(
    result_frame,
    height=15,
    font=("Consolas", 11),
    wrap="word",
    bd=0,
    yscrollcommand=scrollbar.set
)

result_box.pack(
    padx=15,
    pady=(0, 15),
    fill="both",
    expand=True
)


scrollbar.config(
    command=result_box.yview
)


# ==================================================
# RESULT STYLES
# ==================================================

result_box.tag_configure(
    "heading",
    font=("Arial", 12, "bold")
)

result_box.tag_configure(
    "subheading",
    font=("Arial", 11, "bold")
)


# ==================================================
# START APPLICATION
# ==================================================

window.mainloop()