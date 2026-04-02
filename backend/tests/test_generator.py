from app.rag.generator import BaseLLMProvider, ExtractiveLLMProvider, get_llm_provider


def test_extractive_provider_is_base():
    provider = ExtractiveLLMProvider()
    assert isinstance(provider, BaseLLMProvider)


def test_extractive_with_empty_chunks():
    provider = ExtractiveLLMProvider()
    result = provider.generate("What is Python?", [])
    assert result == "No relevant information found for your query."


def test_extractive_with_single_chunk():
    provider = ExtractiveLLMProvider()
    chunks = [{"chunk_text": "Python is a programming language."}]
    result = provider.generate("What is Python?", chunks)
    assert "Python is a programming language." in result


def test_extractive_with_multiple_chunks():
    provider = ExtractiveLLMProvider()
    chunks = [
        {"chunk_text": "Python is a programming language."},
        {"chunk_text": "It is widely used for data science."},
    ]
    result = provider.generate("What is Python?", chunks)
    assert "Python is a programming language." in result
    assert "It is widely used for data science." in result


def test_extractive_result_starts_with_preamble():
    provider = ExtractiveLLMProvider()
    chunks = [{"chunk_text": "Some text."}]
    result = provider.generate("query", chunks)
    assert result.startswith("Based on the retrieved documents:")


def test_get_llm_provider_returns_extractive_by_default():
    provider = get_llm_provider()
    assert isinstance(provider, ExtractiveLLMProvider)
