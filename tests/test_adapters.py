from app.adapters.outbound.llm.groq_adapter import GroqLLMAdapter


def test_groq_adapter_import():
    assert GroqLLMAdapter is not None


def test_groq_adapter_has_required_methods():
    assert hasattr(GroqLLMAdapter, "complete_structured")
    assert hasattr(GroqLLMAdapter, "stream")


def test_groq_adapter_does_not_expose_sdk():
    adapter = GroqLLMAdapter.__new__(GroqLLMAdapter)
    assert not hasattr(adapter, "client")  # or sdk object leak
    assert not hasattr(adapter, "_sdk")     # internal must stay private