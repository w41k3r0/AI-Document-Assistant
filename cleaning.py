def clean_text(text):
    lines = text.split("\n")

    cleaned_lines = []

    for line in lines:
        cleaned_lines.append(line.strip())

    cleaned_text = "\n".join(cleaned_lines)

    return cleaned_text
