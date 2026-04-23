from unittest.mock import Mock


def test_chat_completion_returns_first_choice(monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "deepseek-key")
    monkeypatch.setenv("TMDB_API_KEY", "tmdb-key")

    captured = {}

    def fake_post(url, headers, json, timeout):
        captured["url"] = url
        captured["headers"] = headers
        captured["json"] = json
        captured["timeout"] = timeout
        response = Mock()
        response.raise_for_status.return_value = None
        response.json.return_value = {
            "choices": [{"message": {"content": "积极"}}]
        }
        return response

    monkeypatch.setattr("requests.post", fake_post)

    from client import chat_completion

    result = chat_completion([{"role": "user", "content": "分类这条影评"}], temperature=0.2)

    assert result == "积极"
    assert captured["url"] == "https://api.deepseek.com/v1/chat/completions"
    assert captured["headers"]["Authorization"] == "Bearer deepseek-key"
    assert captured["json"]["temperature"] == 0.2
