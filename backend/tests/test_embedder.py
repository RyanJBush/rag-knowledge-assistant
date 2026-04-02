import numpy as np

from app.rag.embedder import Embedder


def test_encode_returns_numpy_array(mock_sentence_transformer):
    embedder = Embedder()
    result = embedder.encode(["hello world"])
    assert isinstance(result, np.ndarray)


def test_encode_single_text_shape(mock_sentence_transformer):
    embedder = Embedder()
    result = embedder.encode(["test sentence"])
    assert result.ndim == 2
    assert result.shape[0] == 1
    assert result.shape[1] == 384


def test_encode_multiple_texts_shape(mock_sentence_transformer):
    embedder = Embedder()
    texts = ["first", "second", "third"]
    result = embedder.encode(texts)
    assert result.shape == (3, 384)


def test_singleton_shares_model(mock_sentence_transformer):
    e1 = Embedder()
    e2 = Embedder()
    assert e1._model is e2._model


def test_encode_called_with_correct_arguments(mock_sentence_transformer):
    embedder = Embedder()
    texts = ["query text"]
    embedder.encode(texts)
    mock_sentence_transformer.encode.assert_called_with(texts, convert_to_numpy=True)
