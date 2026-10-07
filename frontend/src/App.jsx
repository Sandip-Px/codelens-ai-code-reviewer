import { useEffect, useRef, useState } from "react";
import Editor from "@monaco-editor/react";
import "./App.css";

const exampleCode = `def calculate_total(items):
    total = 0

    for item in items:
        total += eval(item)

    print(total)
    return total`;

function App() {
  const [mode, setMode] = useState("local");
  const [apiStatus, setApiStatus] = useState("checking");
  const [code, setCode] = useState(exampleCode);
  const [language, setLanguage] = useState("python");
  const [review, setReview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState([]);
  const editorRef = useRef(null);

  const handleEditorMount = (editor) => {
    editorRef.current = editor;
  };
  useEffect(() => {
    const loadHistory = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8000/api/reviews/");
        if (!response.ok) throw new Error("Failed to load history");

        const data = await response.json();
        setHistory(data);
      } catch (error) {
        console.error("Could not load review history:", error);
      }
    };

    loadHistory();
  }, []);
  useEffect(() => {
    const checkApi = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8000/health");

        if (!response.ok) {
          throw new Error("API unavailable");
        }

        setApiStatus("connected");
      } catch {
        setApiStatus("offline");
      }
    };

    checkApi();

    const interval = setInterval(checkApi, 30000);

    return () => clearInterval(interval);
  }, []);

  const jumpToLine = (line) => {
    if (!editorRef.current || !line) return;

    editorRef.current.revealLineInCenter(line);

    editorRef.current.setPosition({
      lineNumber: line,
      column: 1,
    });

    editorRef.current.focus();
  };
const openHistory = (item) => {
  setCode(item.code);
  setLanguage(item.language);
  setReview(item);
};


const formatDate = (date) => {
  return new Date(date).toLocaleString([], {
    dateStyle: "medium",
    timeStyle: "short",
  });
};


const reviewCode = async () => {
  if (!code.trim()) return;

  setLoading(true);

  try {
    const response = await fetch(
      "http://127.0.0.1:8000/api/reviews/",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          code,
          language,
          mode,
        }),
      }
    );

    if (!response.ok) {
      throw new Error("Review request failed");
    }

    const data = await response.json();

    setReview(data);

    setHistory((current) => [
      data,
      ...current.filter((item) => item.id !== data.id),
    ]);
  } catch (error) {
    console.error(error);
    alert("Could not connect to the backend.");
  } finally {
    setLoading(false);
  }
};

  return (
    <div className="app">
      <header className="navbar">
        <div className="brand">
          <div className="brand-icon">&lt;/&gt;</div>

          <div>
            <h1>CodeLens</h1>
            <span>Developer Intelligence</span>
          </div>
        </div>

        <div className={`status ${apiStatus}`}>
          <span className="status-dot"></span>

          {apiStatus === "checking" && "Connecting..."}
          {apiStatus === "connected" && "API Connected"}
          {apiStatus === "offline" && "API Offline"}
        </div>
      </header>

      <main className="container">
        <section className="hero">
          <div>
            <p className="eyebrow">DEVELOPER TOOL</p>

            <h2>Ship better code.</h2>

            <p className="subtitle">
              Review your code for security, quality, and maintainability
              issues before they reach production.
            </p>
          </div>
        </section>

        <section className="workspace">
          <div className="editor-card card">
            <div className="card-header">
              <div>
                <h3>Code</h3>
                <span>Paste the code you want to review</span>
              </div>

              <div className="editor-controls">
                <select
                  value={language}
                  onChange={(e) => setLanguage(e.target.value)}
                >
                  <option value="python">Python</option>
                  <option value="javascript">JavaScript</option>
                  <option value="java">Java</option>
                </select>

                <select
                  value={mode}
                  onChange={(e) => setMode(e.target.value)}
                >
                  <option value="local">Local Analysis</option>
                  <option value="ai">AI Analysis</option>
                </select>
              </div>
            </div>

            <div className="editor">
              <Editor
                height="540px"
                language={language}
                value={code}
                onChange={(value) => setCode(value || "")}
                onMount={handleEditorMount}
                theme="vs-dark"
                options={{
                  minimap: {
                    enabled: false,
                  },
                  fontSize: 14,
                  lineNumbers: "on",
                  roundedSelection: false,
                  scrollBeyondLastLine: false,
                  automaticLayout: true,
                  padding: {
                    top: 18,
                    bottom: 18,
                  },
                  tabSize: 4,
                  wordWrap: "off",
                }}
              />
            </div>

            <div className="editor-footer">
              <span>{code.split("\n").length} lines</span>

              <button
                className="review-button"
                onClick={reviewCode}
                disabled={loading}
              >
                {loading ? "Reviewing..." : "Review Code →"}
              </button>
            </div>
          </div>

          <div className="results-card card">
            {!review ? (
              <div className="empty-state">
                <div className="empty-icon">✦</div>

                <h3>Your review will appear here</h3>

                <p>
                  Submit your code to see the quality score, detected issues,
                  and recommendations.
                </p>
              </div>
            ) : (
              <ReviewResults
                review={review}
                onIssueClick={jumpToLine}
              />
            )}
          </div>
        </section>
        <section className="history-section">
          <div className="section-heading">
            <div>
              <span className="eyebrow">History</span>
              <h2>Recent Reviews</h2>
            </div>

            <span className="history-count">
              {history.length} review{history.length === 1 ? "" : "s"}
            </span>
          </div>

          {history.length === 0 ? (
            <div className="history-empty">
              No reviews yet. Run your first code review to see it here.
            </div>
          ) : (
            <div className="history-list">
              {history.map((item) => (
                <button
                  key={item.id}
                  className="history-item"
                  onClick={() => openHistory(item)}
                >
                  <div className="history-main">
                    <strong>Review #{item.id}</strong>
                    <span>{item.language}</span>
                    <span>{formatDate(item.created_at)}</span>
                  </div>

                  <div className="history-meta">
                    <span>
                      {item.issues.length} issue
                      {item.issues.length === 1 ? "" : "s"}
                    </span>

                    <span className="history-score">
                      {item.score ?? "—"}/10
                    </span>

                    <span className="history-arrow">→</span>
                  </div>
                </button>
              ))}
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

function ReviewResults({ review, onIssueClick }) {
  const issues = review.issues || [];

  const score = review.score ?? 0;

  const scoreClass =
    score >= 8
      ? "good"
      : score >= 5
        ? "average"
        : "poor";

  const highCount = issues.filter(
    (issue) => issue.severity === "HIGH"
  ).length;

  const mediumCount = issues.filter(
    (issue) => issue.severity === "MEDIUM"
  ).length;

  const lowCount = issues.filter(
    (issue) => issue.severity === "LOW"
  ).length;

  const severityClass = (severity) => {
    return severity.toLowerCase();
  };

  return (
    <div className="results">
      <div className="results-header">
        <div>
          <p className="eyebrow">REVIEW RESULT</p>
          <h3>Code Quality</h3>
        </div>

        <div className={`score ${scoreClass}`}>
          <strong>{review.score ?? "—"}</strong>
          <span>/10</span>
        </div>
      </div>

      <div className="severity-summary">
        <div className="severity-stat high-stat">
          <strong>{highCount}</strong>
          <span>HIGH</span>
        </div>

        <div className="severity-stat medium-stat">
          <strong>{mediumCount}</strong>
          <span>MEDIUM</span>
        </div>

        <div className="severity-stat low-stat">
          <strong>{lowCount}</strong>
          <span>LOW</span>
        </div>
      </div>

      <div className="summary">
        {review.summary}
      </div>

      <div className="issues-header">
        <h4>Issues</h4>
        <span>{issues.length} detected</span>
      </div>

      {issues.length === 0 ? (
        <div className="success">
          <span>✓</span>
          No obvious issues detected.
        </div>
      ) : (
        <div className="issues">
          {issues.map((issue) => (
            <div className="issue" key={issue.id}>
              <div className="issue-top">
                <span
                  className={`severity ${severityClass(issue.severity)}`}
                >
                  {issue.severity}
                </span>

                <span className="category">
                  {issue.category}
                </span>

                {issue.line && (
                  <button
                    className="line line-button"
                    onClick={() => onIssueClick(issue.line)}
                  >
                    Line {issue.line}
                  </button>
                )}
              </div>

              <p className="issue-message">
                {issue.message}
              </p>

              {issue.suggestion && (
                <div className="suggestion">
                  <strong>Suggestion</strong>

                  <p>{issue.suggestion}</p>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;