from dataclasses import dataclass


@dataclass
class DetectedIssue:
    severity: str
    category: str
    line: int | None
    message: str
    suggestion: str


class CodeAnalyzer:

    def analyze(self, code: str, language: str):
        issues = []
        lines = code.splitlines()

        for line_number, line in enumerate(lines, start=1):
            stripped = line.strip()

            # Security: eval()
            if "eval(" in stripped:
                issues.append(
                    DetectedIssue(
                        severity="HIGH",
                        category="Security",
                        line=line_number,
                        message="Use of eval() can execute arbitrary code.",
                        suggestion="Avoid eval() and use safer parsing methods."
                    )
                )

            # Security: hard-coded credentials
            if "password" in stripped.lower() and "=" in stripped:
                issues.append(
                    DetectedIssue(
                        severity="HIGH",
                        category="Security",
                        line=line_number,
                        message="Possible hard-coded password or credential.",
                        suggestion="Use environment variables or a secrets manager."
                    )
                )

            # Code quality: print()
            if stripped.startswith("print("):
                issues.append(
                    DetectedIssue(
                        severity="LOW",
                        category="Code Quality",
                        line=line_number,
                        message="print() is being used for application output.",
                        suggestion="Use a logging framework for production applications."
                    )
                )

            # Maintainability: TODO
            if "TODO" in stripped:
                issues.append(
                    DetectedIssue(
                        severity="LOW",
                        category="Maintainability",
                        line=line_number,
                        message="TODO comment indicates unfinished work.",
                        suggestion="Resolve the TODO or create a tracked issue."
                    )
                )

        # Large file
        if len(lines) > 100:
            issues.append(
                DetectedIssue(
                    severity="MEDIUM",
                    category="Maintainability",
                    line=None,
                    message="The file contains more than 100 lines.",
                    suggestion="Consider splitting large modules into smaller components."
                )
            )

        score = self._calculate_score(issues)
        summary = self._create_summary(issues, score)

        # Convert DetectedIssue objects into dictionaries.
        # This gives the local analyzer the same output
        # format as the AI analyzer.
        normalized_issues = [
            {
                "severity": issue.severity,
                "category": issue.category,
                "line": issue.line,
                "message": issue.message,
                "suggestion": issue.suggestion
            }
            for issue in issues
        ]

        return {
            "score": score,
            "summary": summary,
            "issues": normalized_issues
        }

    def _calculate_score(self, issues):
        score = 10

        for issue in issues:
            if issue.severity == "HIGH":
                score -= 3

            elif issue.severity == "MEDIUM":
                score -= 2

            elif issue.severity == "LOW":
                score -= 1

        return max(0, score)

    def _create_summary(self, issues, score):
        if not issues:
            return "No obvious issues were detected."

        return (
            f"Found {len(issues)} potential issue(s). "
            f"Overall code quality score: {score}/10."
        )