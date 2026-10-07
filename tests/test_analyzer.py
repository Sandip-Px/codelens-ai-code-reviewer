from app.services.analyzer import CodeAnalyzer


def test_detects_eval():
    analyzer = CodeAnalyzer()

    result = analyzer.analyze(
        "result = eval(user_input)",
        "python"
    )

    assert result["score"] < 10
    assert len(result["issues"]) == 1
    assert result["issues"][0].severity == "HIGH"


def test_clean_code():
    analyzer = CodeAnalyzer()

    result = analyzer.analyze(
        "name = 'Charon'\nprint(name)",
        "python"
    )

    assert len(result["issues"]) == 1
    assert result["issues"][0].category == "Code Quality"