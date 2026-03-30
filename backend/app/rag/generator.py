def generate_answer(question: str, contexts: list[str]) -> str:
    if not contexts:
        return "I could not find relevant information in the uploaded documents."

    joined = "\n".join(f"- {ctx}" for ctx in contexts[:3])
    return (
        f"Based on the retrieved documents, here is the best grounded answer to: '{question}'.\n\n"
        f"Relevant context:\n{joined}\n\n"
        "If you want a more precise answer, upload more specific documents or refine the question."
    )
