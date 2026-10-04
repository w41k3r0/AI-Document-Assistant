import re

MISSING_ANSWER = (
    "I could not find enough information in the documents "
    "to answer this question."
)

def prepare_answer(answer, sources):
    answer = answer.strip()
    if not answer:
        raise RuntimeError("No answer was returned by the model.")

    if answer == MISSING_ANSWER:
        return {
            "answer" : MISSING_ANSWER,
            "sources" : [],
        }

    labels = re.findall(r"\[(S\d+)\]", answer)
    if not labels:
        raise RuntimeError("The model's answer contained no citations.")

    sources_by_label = {}

    for source in sources:
        sources_by_label[source["label"]] = source

    cited_souces = []
    seen_labels = set()

    for label in labels:
        if label not in sources_by_label:
            raise RuntimeError(f"The model cited an unknown source: {label}")

        if label not in seen_labels:
            cited_souces.append(sources_by_label[label])
            seen_labels.add(label)

    return {
        "answer" : answer,
        "sources" : cited_souces,
    }