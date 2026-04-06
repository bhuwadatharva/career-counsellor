import { useState, useEffect } from "react";

const API_BASE = "https://career-counsellor-22cy.onrender.com";

const css = `
  @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Mono:ital,wght@0,300;0,400;0,500;1,400&family=DM+Sans:wght@300;400;500&display=swap');
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  :root {
    --black: #0a0a0a; --white: #f5f5f0;
    --grey-100: #1a1a1a; --grey-200: #252525; --grey-300: #333;
    --grey-400: #555; --grey-500: #888; --grey-600: #aaa;
    --grey-700: #ccc; --grey-800: #e5e5e5;
    --font-display: 'Bebas Neue', sans-serif;
    --font-mono: 'DM Mono', monospace;
    --font-body: 'DM Sans', sans-serif;
  }
  html { scroll-behavior: smooth; }
  body { background: var(--black); color: var(--white); font-family: var(--font-body); font-size: 15px; line-height: 1.6; min-height: 100vh; overflow-x: hidden; }
  body::before { content: ''; position: fixed; inset: 0; background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.04'/%3E%3C/svg%3E"); pointer-events: none; z-index: 1000; opacity: 0.4; }
  .page { min-height: 100vh; position: relative; }
  .site-header { border-bottom: 1px solid var(--grey-300); padding: 20px 40px; display: flex; align-items: center; justify-content: space-between; position: sticky; top: 0; background: rgba(10,10,10,0.96); backdrop-filter: blur(12px); z-index: 100; }
  .logo { font-family: var(--font-display); font-size: 22px; letter-spacing: 3px; }
  .logo span { color: var(--grey-500); }
  .header-tag { font-family: var(--font-mono); font-size: 11px; color: var(--grey-500); letter-spacing: 2px; text-transform: uppercase; }
  .error-page { min-height: calc(100vh - 61px); display: flex; align-items: center; justify-content: center; padding: 40px 24px; }
  .error-card { max-width: 560px; width: 100%; border: 1px solid #5a2020; background: #120808; padding: 40px; }
  .error-card h2 { font-family: var(--font-display); font-size: 32px; letter-spacing: 2px; color: #c97070; margin-bottom: 16px; }
  .error-card p { font-size: 14px; color: var(--grey-600); line-height: 1.7; margin-bottom: 12px; }
  .error-card code { font-family: var(--font-mono); font-size: 12px; color: var(--grey-500); background: var(--grey-100); padding: 2px 8px; display: inline-block; margin-top: 4px; }
  .error-card .retry-btn { margin-top: 24px; padding: 12px 28px; border: 1px solid var(--grey-400); background: transparent; color: var(--grey-500); font-family: var(--font-mono); font-size: 12px; letter-spacing: 2px; cursor: pointer; transition: all 0.2s; }
  .error-card .retry-btn:hover { color: var(--white); border-color: var(--grey-600); }
  .intake-page { display: flex; min-height: calc(100vh - 61px); }
  .intake-left { width: 420px; flex-shrink: 0; border-right: 1px solid var(--grey-300); padding: 60px 48px; display: flex; flex-direction: column; justify-content: center; background: var(--grey-100); position: relative; overflow: hidden; }
  .intake-left::before { content: 'CAREER\ACOUNSELLOR'; white-space: pre; position: absolute; bottom: -20px; left: -10px; font-family: var(--font-display); font-size: 120px; line-height: 0.85; color: var(--grey-200); letter-spacing: -2px; pointer-events: none; user-select: none; }
  .intake-left h1 { font-family: var(--font-display); font-size: 52px; line-height: 1; letter-spacing: 2px; margin-bottom: 16px; position: relative; z-index: 1; }
  .intake-left h1 em { font-style: normal; color: var(--grey-500); display: block; font-size: 36px; }
  .intake-left p { font-size: 14px; color: var(--grey-600); line-height: 1.7; position: relative; z-index: 1; max-width: 300px; }
  .intake-steps { margin-top: 40px; display: flex; flex-direction: column; gap: 12px; position: relative; z-index: 1; }
  .step-item { display: flex; align-items: center; gap: 12px; font-family: var(--font-mono); font-size: 12px; color: var(--grey-500); }
  .step-num { width: 24px; height: 24px; border: 1px solid var(--grey-400); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 10px; flex-shrink: 0; }
  .intake-right { flex: 1; padding: 60px 64px; display: flex; align-items: center; justify-content: center; }
  .intake-form { width: 100%; max-width: 520px; }
  .form-title { font-family: var(--font-mono); font-size: 11px; letter-spacing: 3px; color: var(--grey-500); text-transform: uppercase; margin-bottom: 32px; display: flex; align-items: center; gap: 12px; }
  .form-title::after { content: ''; flex: 1; height: 1px; background: var(--grey-300); }
  .field-group { margin-bottom: 24px; }
  .field-label { display: block; font-family: var(--font-mono); font-size: 11px; letter-spacing: 2px; color: var(--grey-500); text-transform: uppercase; margin-bottom: 8px; }
  .field-input { width: 100%; background: var(--grey-100); border: 1px solid var(--grey-300); color: var(--white); font-family: var(--font-body); font-size: 15px; padding: 14px 16px; outline: none; transition: border-color 0.2s; appearance: none; -webkit-appearance: none; }
  .field-input:focus { border-color: var(--grey-600); }
  .field-input option { background: var(--grey-100); }
  .field-row { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
  .work-style-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }
  .work-style-btn { padding: 12px; background: var(--grey-100); border: 1px solid var(--grey-300); color: var(--grey-600); font-family: var(--font-mono); font-size: 12px; letter-spacing: 1px; cursor: pointer; transition: all 0.2s; text-align: center; }
  .work-style-btn:hover { border-color: var(--grey-500); color: var(--white); }
  .work-style-btn.active { background: var(--white); border-color: var(--white); color: var(--black); }
  .submit-btn { width: 100%; padding: 18px; background: var(--white); color: var(--black); border: none; font-family: var(--font-display); font-size: 20px; letter-spacing: 4px; cursor: pointer; transition: all 0.2s; margin-top: 8px; position: relative; overflow: hidden; }
  .submit-btn::after { content: ''; position: absolute; inset: 0; background: var(--black); transform: translateX(-100%); transition: transform 0.3s ease; }
  .submit-btn:hover::after { transform: translateX(0); }
  .submit-btn span { position: relative; z-index: 1; }
  .submit-btn:hover span { color: var(--white); }
  .submit-btn:disabled { opacity: 0.4; cursor: not-allowed; }
  .quiz-page { max-width: 760px; margin: 0 auto; padding: 48px 24px 80px; }
  .quiz-header { margin-bottom: 48px; }
  .quiz-meta { display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px; }
  .quiz-label { font-family: var(--font-mono); font-size: 11px; letter-spacing: 3px; color: var(--grey-500); text-transform: uppercase; }
  .quiz-counter { font-family: var(--font-display); font-size: 28px; color: var(--grey-400); letter-spacing: 2px; }
  .quiz-counter span { color: var(--white); }
  .progress-track { height: 2px; background: var(--grey-300); overflow: hidden; }
  .progress-fill { height: 100%; background: var(--white); transition: width 0.4s ease; }
  .student-tag { margin-top: 16px; display: inline-flex; align-items: center; gap: 8px; background: var(--grey-100); border: 1px solid var(--grey-300); padding: 6px 14px; font-family: var(--font-mono); font-size: 12px; color: var(--grey-500); }
  .student-tag strong { color: var(--white); }
  .question-card { animation: slideIn 0.3s ease; }
  @keyframes slideIn { from { opacity: 0; transform: translateY(16px); } to { opacity: 1; transform: translateY(0); } }
  .q-category { font-family: var(--font-mono); font-size: 10px; letter-spacing: 3px; color: var(--grey-500); text-transform: uppercase; margin-bottom: 12px; display: flex; align-items: center; gap: 8px; }
  .q-category::before { content: ''; width: 20px; height: 1px; background: var(--grey-500); }
  .q-text { font-family: var(--font-display); font-size: 38px; line-height: 1.1; letter-spacing: 1px; margin-bottom: 8px; color: var(--white); }
  .q-subtitle { font-size: 14px; color: var(--grey-500); margin-bottom: 32px; font-style: italic; }
  .multi-badge { display: inline-flex; align-items: center; gap: 6px; background: var(--grey-200); border: 1px solid var(--grey-300); padding: 4px 10px; font-family: var(--font-mono); font-size: 10px; letter-spacing: 2px; color: var(--grey-500); margin-bottom: 20px; }
  .options-list { display: flex; flex-direction: column; gap: 10px; }
  .option-btn { display: flex; align-items: flex-start; gap: 16px; padding: 18px 20px; background: var(--grey-100); border: 1px solid var(--grey-300); cursor: pointer; transition: all 0.18s; text-align: left; width: 100%; color: var(--grey-700); }
  .option-btn:hover { border-color: var(--grey-500); color: var(--white); background: var(--grey-200); }
  .option-btn.selected { background: var(--white); border-color: var(--white); color: var(--black); }
  .option-id { font-family: var(--font-display); font-size: 22px; line-height: 1; flex-shrink: 0; width: 24px; letter-spacing: 1px; }
  .option-btn.selected .option-id { color: var(--grey-400); }
  .option-text { font-size: 14px; line-height: 1.55; padding-top: 2px; }
  .quiz-nav { display: flex; align-items: center; justify-content: space-between; margin-top: 36px; padding-top: 28px; border-top: 1px solid var(--grey-300); }
  .nav-btn { padding: 12px 28px; font-family: var(--font-mono); font-size: 12px; letter-spacing: 2px; cursor: pointer; transition: all 0.2s; border: 1px solid var(--grey-300); background: transparent; color: var(--grey-500); }
  .nav-btn:hover:not(:disabled) { color: var(--white); border-color: var(--grey-500); }
  .nav-btn:disabled { opacity: 0.2; cursor: not-allowed; }
  .nav-btn.primary { background: var(--white); color: var(--black); border-color: var(--white); font-family: var(--font-display); font-size: 18px; padding: 14px 40px; letter-spacing: 3px; }
  .nav-btn.primary:hover:not(:disabled) { background: var(--grey-800); }
  .nav-btn.primary:disabled { opacity: 0.3; }
  .q-dots { display: flex; gap: 4px; flex-wrap: wrap; max-width: 300px; }
  .q-dot { width: 6px; height: 6px; background: var(--grey-300); transition: background 0.2s; }
  .q-dot.answered { background: var(--white); }
  .q-dot.current { background: var(--grey-600); }
  .loading-page { min-height: calc(100vh - 61px); display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 32px; }
  .loading-title { font-family: var(--font-display); font-size: 56px; letter-spacing: 4px; animation: pulse 1.5s ease-in-out infinite; }
  @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.3; } }
  .loading-steps { display: flex; flex-direction: column; gap: 10px; align-items: center; }
  .loading-step { font-family: var(--font-mono); font-size: 12px; letter-spacing: 2px; color: var(--grey-500); display: flex; align-items: center; gap: 10px; transition: color 0.4s; }
  .loading-step.active { color: var(--white); }
  .loading-step.done { color: var(--grey-400); }
  .step-dot { width: 6px; height: 6px; border-radius: 50%; background: var(--grey-400); transition: background 0.4s; }
  .loading-step.active .step-dot { background: var(--white); animation: blink 0.8s infinite; }
  .loading-step.done .step-dot { background: var(--grey-600); }
  @keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.2} }
  .result-page { max-width: 1100px; margin: 0 auto; padding: 0 24px 80px; }
  .result-hero { border-bottom: 1px solid var(--grey-300); padding: 48px 0 40px; display: grid; grid-template-columns: 1fr auto; gap: 40px; align-items: start; }
  .result-tag { font-family: var(--font-mono); font-size: 11px; letter-spacing: 3px; color: var(--grey-500); text-transform: uppercase; margin-bottom: 16px; display: flex; align-items: center; gap: 10px; }
  .result-tag::before { content: ''; width: 24px; height: 1px; background: var(--grey-500); }
  .result-name { font-family: var(--font-display); font-size: 72px; line-height: 0.95; letter-spacing: 2px; margin-bottom: 8px; }
  .result-domain { font-family: var(--font-display); font-size: 40px; letter-spacing: 2px; color: var(--grey-500); line-height: 1; margin-bottom: 20px; }
  .result-goal { font-size: 15px; color: var(--grey-600); max-width: 560px; line-height: 1.7; border-left: 2px solid var(--grey-400); padding-left: 16px; }
  .result-stats { display: flex; flex-direction: column; gap: 16px; min-width: 180px; }
  .stat-box { border: 1px solid var(--grey-300); padding: 16px 20px; text-align: center; }
  .stat-value { font-family: var(--font-display); font-size: 44px; letter-spacing: 2px; line-height: 1; color: var(--white); }
  .stat-label { font-family: var(--font-mono); font-size: 10px; letter-spacing: 2px; color: var(--grey-500); text-transform: uppercase; margin-top: 4px; }
  .path-id-box { border: 1px solid var(--grey-300); padding: 10px 16px; font-family: var(--font-mono); font-size: 11px; color: var(--grey-500); text-align: center; letter-spacing: 1px; }
  .result-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1px; background: var(--grey-300); border: 1px solid var(--grey-300); margin-top: 1px; }
  .result-grid.full { grid-template-columns: 1fr; }
  .result-grid.thirds { grid-template-columns: 1fr 1fr 1fr; }
  .r-cell { background: var(--black); padding: 32px 36px; }
  .r-cell.dark { background: var(--grey-100); }
  .cell-label { font-family: var(--font-mono); font-size: 10px; letter-spacing: 3px; color: var(--grey-500); text-transform: uppercase; margin-bottom: 20px; display: flex; align-items: center; gap: 10px; }
  .cell-label::after { content: ''; flex: 1; height: 1px; background: var(--grey-300); }
  .score-bar-row { display: flex; align-items: center; gap: 12px; margin-bottom: 12px; }
  .score-bar-label { font-size: 12px; color: var(--grey-600); width: 200px; flex-shrink: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .score-bar-label.top { color: var(--white); font-size: 13px; }
  .score-bar-track { flex: 1; height: 2px; background: var(--grey-300); }
  .score-bar-fill { height: 100%; background: var(--white); transition: width 1s ease; }
  .score-bar-fill.dim { background: var(--grey-400); }
  .score-pct { font-family: var(--font-mono); font-size: 11px; color: var(--grey-500); width: 32px; text-align: right; }
  .skill-item { display: flex; align-items: center; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid var(--grey-200); gap: 12px; }
  .skill-name { font-family: var(--font-mono); font-size: 12px; color: var(--grey-700); }
  .skill-status { font-family: var(--font-mono); font-size: 11px; white-space: nowrap; }
  .status-ok { color: #6b9b6b; }
  .status-critical { color: #c97070; }
  .status-high { color: #c9a070; }
  .status-medium { color: var(--grey-500); }
  .milestones-list { display: flex; flex-direction: column; }
  .milestone-row { display: grid; grid-template-columns: 40px 1fr; position: relative; }
  .milestone-row::before { content: ''; position: absolute; left: 19px; top: 40px; bottom: 0; width: 1px; background: var(--grey-300); }
  .milestone-row:last-child::before { display: none; }
  .milestone-num { width: 40px; height: 40px; border: 1px solid var(--grey-300); display: flex; align-items: center; justify-content: center; font-family: var(--font-display); font-size: 18px; color: var(--grey-500); flex-shrink: 0; background: var(--black); position: relative; z-index: 1; }
  .milestone-content { padding: 0 0 32px 24px; }
  .milestone-title { font-family: var(--font-display); font-size: 24px; letter-spacing: 1px; color: var(--white); margin-bottom: 8px; line-height: 1.1; }
  .milestone-skills { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 12px; }
  .skill-chip { font-family: var(--font-mono); font-size: 10px; letter-spacing: 1px; padding: 3px 8px; border: 1px solid var(--grey-300); color: var(--grey-500); }
  .milestone-projects { font-size: 13px; color: var(--grey-500); margin-bottom: 12px; font-style: italic; }
  .resource-link { display: flex; align-items: center; gap: 8px; font-family: var(--font-mono); font-size: 11px; color: var(--grey-600); text-decoration: none; padding: 6px 0; transition: color 0.2s; border-bottom: 1px solid var(--grey-200); }
  .resource-link:hover { color: var(--white); }
  .resource-link::before { content: '↗'; font-size: 10px; }
  .res-hours { margin-left: auto; color: var(--grey-400); font-size: 10px; }
  .tool-item { display: flex; align-items: flex-start; gap: 16px; padding: 16px 0; border-bottom: 1px solid var(--grey-200); }
  .tool-badge { font-family: var(--font-mono); font-size: 9px; letter-spacing: 1px; padding: 3px 6px; border: 1px solid var(--grey-400); color: var(--grey-500); white-space: nowrap; flex-shrink: 0; margin-top: 2px; }
  .tool-info { flex: 1; }
  .tool-title { font-size: 13px; color: var(--white); margin-bottom: 2px; }
  .tool-url { font-family: var(--font-mono); font-size: 10px; color: var(--grey-500); text-decoration: none; }
  .tool-url:hover { color: var(--grey-700); }
  .tag-list { display: flex; flex-wrap: wrap; gap: 8px; }
  .tag { font-family: var(--font-mono); font-size: 11px; letter-spacing: 1px; padding: 6px 12px; border: 1px solid var(--grey-300); color: var(--grey-600); }
  .tag.white { background: var(--white); color: var(--black); border-color: var(--white); }
  .salary-row { display: flex; gap: 24px; margin-bottom: 16px; }
  .salary-item { flex: 1; }
  .salary-flag { font-family: var(--font-mono); font-size: 10px; color: var(--grey-500); letter-spacing: 2px; margin-bottom: 6px; }
  .salary-value { font-family: var(--font-display); font-size: 28px; letter-spacing: 1px; color: var(--white); line-height: 1.1; }
  .action-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1px; background: var(--grey-300); border: 1px solid var(--grey-300); margin-top: 1px; }
  .action-card { background: var(--black); padding: 28px 32px; }
  .action-label { font-family: var(--font-mono); font-size: 9px; letter-spacing: 3px; color: var(--grey-500); text-transform: uppercase; margin-bottom: 12px; }
  .action-text { font-size: 14px; color: var(--grey-700); line-height: 1.65; }
  .action-text.highlight { color: var(--white); font-family: var(--font-mono); font-size: 12px; }
  .advice-block { border: 1px solid var(--grey-300); margin-top: 1px; padding: 40px 48px; background: var(--grey-100); position: relative; overflow: hidden; }
  .advice-block::before { content: '"'; position: absolute; top: -20px; left: 24px; font-family: var(--font-display); font-size: 200px; color: var(--grey-200); line-height: 1; pointer-events: none; }
  .advice-text { font-family: var(--font-body); font-size: 20px; line-height: 1.7; color: var(--grey-700); position: relative; z-index: 1; max-width: 800px; }
  .advice-text strong { color: var(--white); font-weight: 500; }
  .agent-strip { border: 1px solid var(--grey-300); padding: 16px 24px; margin-top: 1px; display: flex; align-items: center; gap: 32px; background: var(--grey-100); flex-wrap: wrap; }
  .agent-item { display: flex; align-items: center; gap: 8px; font-family: var(--font-mono); font-size: 11px; color: var(--grey-500); }
  .agent-item span { color: var(--white); }
  .agent-dot { width: 6px; height: 6px; background: var(--grey-400); border-radius: 50%; }
  .restart-bar { display: flex; align-items: center; justify-content: center; padding: 40px 0 0; gap: 20px; }
  .restart-btn { padding: 14px 40px; background: transparent; border: 1px solid var(--grey-400); color: var(--grey-500); font-family: var(--font-mono); font-size: 12px; letter-spacing: 2px; cursor: pointer; transition: all 0.2s; }
  .restart-btn:hover { color: var(--white); border-color: var(--grey-600); }
  @media (max-width: 768px) {
    .intake-page { flex-direction: column; }
    .intake-left { width: 100%; padding: 32px 24px; }
    .intake-left::before { display: none; }
    .intake-right { padding: 32px 24px; }
    .result-hero { grid-template-columns: 1fr; }
    .result-name { font-size: 48px; }
    .result-domain { font-size: 28px; }
    .result-grid, .result-grid.thirds { grid-template-columns: 1fr; }
    .action-grid { grid-template-columns: 1fr; }
    .score-bar-label { width: 130px; font-size: 11px; }
    .agent-strip { gap: 16px; }
  }
`;

function SiteHeader({ page }) {
  const labels = {
    intake: "STEP 1 OF 3 — PROFILE",
    quiz: "STEP 2 OF 3 — ASSESSMENT",
    result: "CAREER PATH GENERATED",
  };
  return (
    <header className="site-header">
      <div className="logo">
        CAREER<span>.</span>AI
      </div>
      <div className="header-tag">{labels[page] || ""}</div>
    </header>
  );
}

function ErrorPage({ title, lines, onBack }) {
  return (
    <div className="error-page">
      <div className="error-card">
        <h2>⚠ {title}</h2>
        {lines.map((l, i) => (
          <p key={i}>{l}</p>
        ))}
        <button className="retry-btn" onClick={onBack}>
          ← GO BACK
        </button>
      </div>
    </div>
  );
}

function IntakePage({ onSubmit }) {
  const [form, setForm] = useState({
    name: "",
    current_year: "",
    total_years: "4",
    degree_type: "B.Tech",
    preferred_work_style: "both",
  });
  const set = (k, v) => setForm((f) => ({ ...f, [k]: v }));
  const valid = form.name.trim() && form.current_year;
  return (
    <div className="page intake-page">
      <div className="intake-left">
        <h1>
          YOUR CAREER<em>STARTS HERE.</em>
        </h1>
        <p>
          Answer 15 behavioural questions. The AI infers your domain and skill
          level from how you respond — no manual input needed.
        </p>
        <div className="intake-steps">
          {[
            ["01", "Fill your profile"],
            ["02", "Answer 15 questions"],
            ["03", "Get your career path"],
          ].map(([n, t]) => (
            <div className="step-item" key={n}>
              <div className="step-num">{n}</div>
              {t}
            </div>
          ))}
        </div>
      </div>
      <div className="intake-right">
        <div className="intake-form">
          <div className="form-title">STUDENT PROFILE</div>
          <div className="field-group">
            <label className="field-label">Full Name</label>
            <input
              className="field-input"
              placeholder="Rahul Sharma"
              value={form.name}
              onChange={(e) => set("name", e.target.value)}
            />
          </div>
          <div className="field-group">
            <label className="field-label">Degree Type</label>
            <select
              className="field-input"
              value={form.degree_type}
              onChange={(e) => set("degree_type", e.target.value)}
            >
              {["B.Tech", "BCA", "MCA", "B.Sc CS", "M.Tech", "B.E."].map(
                (d) => (
                  <option key={d}>{d}</option>
                ),
              )}
            </select>
          </div>
          <div className="field-row field-group">
            <div>
              <label className="field-label">Current Year</label>
              <select
                className="field-input"
                value={form.current_year}
                onChange={(e) => set("current_year", e.target.value)}
              >
                <option value="">Select</option>
                {[1, 2, 3, 4, 5].map((y) => (
                  <option key={y} value={y}>
                    Year {y}
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label className="field-label">Total Years</label>
              <select
                className="field-input"
                value={form.total_years}
                onChange={(e) => set("total_years", e.target.value)}
              >
                {[3, 4, 5].map((y) => (
                  <option key={y} value={y}>
                    {y} Years
                  </option>
                ))}
              </select>
            </div>
          </div>
          <div className="field-group">
            <label className="field-label">Preferred Work Style</label>
            <div className="work-style-grid">
              {["remote", "onsite", "both"].map((s) => (
                <button
                  key={s}
                  className={`work-style-btn${form.preferred_work_style === s ? " active" : ""}`}
                  onClick={() => set("preferred_work_style", s)}
                >
                  {s.toUpperCase()}
                </button>
              ))}
            </div>
          </div>
          <button
            className="submit-btn"
            disabled={!valid}
            onClick={() => onSubmit(form)}
          >
            <span>BEGIN ASSESSMENT →</span>
          </button>
        </div>
      </div>
    </div>
  );
}

function QuizPage({ profile, onComplete, onError }) {
  const [questions, setQuestions] = useState(null);
  const [current, setCurrent] = useState(0);
  const [answers, setAnswers] = useState({});

  useEffect(() => {
    fetch(`${API_BASE}/questions`)
      .then((r) => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        return r.json();
      })
      .then((d) => setQuestions(d.questions))
      .catch((err) =>
        onError("Cannot Load Questions", [
          `Could not reach ${API_BASE}/questions`,
          `Error: ${err.message}`,
          "Make sure your FastAPI server is running:",
          "uvicorn main:app --reload --port 8000",
          "And that CORS is enabled in main.py",
        ]),
      );
  }, []);

  if (!questions)
    return (
      <div className="loading-page">
        <div className="loading-title">LOADING</div>
        <p
          style={{
            fontFamily: "var(--font-mono)",
            color: "var(--grey-500)",
            fontSize: 12,
            letterSpacing: 2,
          }}
        >
          CONNECTING TO {API_BASE}...
        </p>
      </div>
    );

  const q = questions[current];
  const total = questions.length;
  const selected = answers[q.id] || [];
  const isAnswered = selected.length > 0;
  const isLast = current === total - 1;

  const toggle = (optId) => {
    if (q.multi_select) {
      const cur = answers[q.id] || [];
      setAnswers((a) => ({
        ...a,
        [q.id]: cur.includes(optId)
          ? cur.filter((x) => x !== optId)
          : [...cur, optId],
      }));
    } else {
      setAnswers((a) => ({ ...a, [q.id]: [optId] }));
    }
  };

  return (
    <div className="page">
      <div className="quiz-page">
        <div className="quiz-header">
          <div className="quiz-meta">
            <div className="quiz-label">BEHAVIOURAL ASSESSMENT</div>
            <div className="quiz-counter">
              <span>{current + 1}</span> / {total}
            </div>
          </div>
          <div className="progress-track">
            <div
              className="progress-fill"
              style={{ width: `${((current + 1) / total) * 100}%` }}
            />
          </div>
          <div
            style={{
              marginTop: 12,
              display: "flex",
              alignItems: "center",
              justifyContent: "space-between",
            }}
          >
            <div className="student-tag">
              <span>FOR</span>
              <strong>{profile.name}</strong>
              <span>·</span>
              <span>
                {profile.degree_type} Y{profile.current_year}
              </span>
            </div>
            <div className="q-dots">
              {questions.map((_, i) => (
                <div
                  key={i}
                  className={`q-dot${answers[questions[i].id]?.length ? " answered" : ""}${i === current ? " current" : ""}`}
                />
              ))}
            </div>
          </div>
        </div>
        <div className="question-card" key={q.id}>
          <div className="q-category">{q.category}</div>
          <div className="q-text">{q.text}</div>
          <div className="q-subtitle">{q.subtitle}</div>
          {q.multi_select && (
            <div className="multi-badge">
              ✦ MULTI-SELECT — pick all that apply
            </div>
          )}
          <div className="options-list">
            {q.options.map((opt) => (
              <button
                key={opt.id}
                className={`option-btn${selected.includes(opt.id) ? " selected" : ""}`}
                onClick={() => toggle(opt.id)}
              >
                <span className="option-id">{opt.id}</span>
                <span className="option-text">{opt.text}</span>
              </button>
            ))}
          </div>
        </div>
        <div className="quiz-nav">
          <button
            className="nav-btn"
            onClick={() => setCurrent((c) => c - 1)}
            disabled={current === 0}
          >
            ← BACK
          </button>
          {isLast ? (
            <button
              className="nav-btn primary"
              onClick={() => onComplete({ ...profile, answers })}
              disabled={!isAnswered}
            >
              GENERATE PATH
            </button>
          ) : (
            <button
              className="nav-btn primary"
              onClick={() => setCurrent((c) => c + 1)}
              disabled={!isAnswered}
            >
              NEXT →
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

function LoadingPage() {
  const [active, setActive] = useState(0);
  const steps = [
    "ANALYZING PROFILE",
    "DECIDING DOMAIN",
    "RETRIEVING KNOWLEDGE",
    "READING JOB MARKET",
    "BUILDING MILESTONES",
    "SYNTHESIZING PATH",
  ];
  useEffect(() => {
    let i = 0;
    const t = setInterval(() => {
      i++;
      setActive(i);
      if (i >= steps.length) clearInterval(t);
    }, 900);
    return () => clearInterval(t);
  }, []);
  return (
    <div className="loading-page">
      <div className="loading-title">PROCESSING</div>
      <div className="loading-steps">
        {steps.map((s, i) => (
          <div
            key={s}
            className={`loading-step${i === active ? " active" : ""}${i < active ? " done" : ""}`}
          >
            <div className="step-dot" />
            {s}
          </div>
        ))}
      </div>
    </div>
  );
}

function ResultPage({ data, onRestart }) {
  const ip = data.inferred_profile;
  const scores = Object.entries(ip.domain_scores).sort((a, b) => b[1] - a[1]);
  const sc = (s) =>
    s.includes("✅")
      ? "status-ok"
      : s.includes("🔴")
        ? "status-critical"
        : s.includes("🟠")
          ? "status-high"
          : "status-medium";
  const clean = (s) => s.replace(/🔴|🟠|🟡|✅/g, "").trim();
  return (
    <div className="page">
      <div className="result-page">
        <div className="result-hero">
          <div>
            <div className="result-tag">CAREER PATH GENERATED</div>
            <div className="result-name">
              {data.user_name.split(" ")[0].toUpperCase()}
              <br />
              {data.user_name.split(" ").slice(1).join(" ").toUpperCase()}
            </div>
            <div className="result-domain">
              {data.recommended_domain.toUpperCase()}
            </div>
            <div className="result-goal">{data.career_goal}</div>
          </div>
          <div className="result-stats">
            <div className="stat-box">
              <div className="stat-value">
                {Math.round(data.confidence_score * 100)}%
              </div>
              <div className="stat-label">CONFIDENCE</div>
            </div>
            <div className="stat-box">
              <div className="stat-value">{data.years_remaining}</div>
              <div className="stat-label">YRS REMAINING</div>
            </div>
            <div className="stat-box">
              <div className="stat-value">{data.monthly_milestones.length}</div>
              <div className="stat-label">MILESTONES</div>
            </div>
            <div className="path-id-box">PATH {data.path_id}</div>
          </div>
        </div>
        <div className="agent-strip">
          {[
            ["MODEL", data.agent_model],
            ["RAG", data.rag_backend],
            ["STEPS", data.agent_steps_executed + " executed"],
            ["SKILL", ip.skill_level.toUpperCase()],
            ["GIT", ip.knows_git ? "KNOWN ✓" : "NEEDS LEARNING"],
            ["DOCKER", ip.knows_docker ? "KNOWN ✓" : "NEEDS LEARNING"],
          ].map(([k, v]) => (
            <div className="agent-item" key={k}>
              <div className="agent-dot" />
              {k} <span>{v}</span>
            </div>
          ))}
        </div>
        <div className="result-grid">
          <div className="r-cell dark">
            <div className="cell-label">SUMMARY</div>
            <p
              style={{
                fontSize: 14,
                color: "var(--grey-600)",
                lineHeight: 1.75,
                marginBottom: 20,
              }}
            >
              {data.summary}
            </p>
            <p
              style={{
                fontSize: 13,
                color: "var(--grey-500)",
                lineHeight: 1.7,
                borderLeft: "2px solid var(--grey-300)",
                paddingLeft: 14,
              }}
            >
              {data.why_this_domain}
            </p>
          </div>
          <div className="r-cell">
            <div className="cell-label">DOMAIN SCORES</div>
            {scores.map(([d, s], i) => (
              <div className="score-bar-row" key={d}>
                <div className={`score-bar-label${i === 0 ? " top" : ""}`}>
                  {d}
                </div>
                <div className="score-bar-track">
                  <div
                    className={`score-bar-fill${i > 0 ? " dim" : ""}`}
                    style={{ width: `${s * 100}%` }}
                  />
                </div>
                <div className="score-pct">{Math.round(s * 100)}%</div>
              </div>
            ))}
          </div>
        </div>
        <div className="result-grid">
          <div className="r-cell">
            <div className="cell-label">INFERRED INTERESTS</div>
            <div className="tag-list" style={{ marginBottom: 24 }}>
              {ip.inferred_interests.map((t) => (
                <div className="tag" key={t}>
                  {t}
                </div>
              ))}
            </div>
            <div className="cell-label" style={{ marginTop: 8 }}>
              JOB ROLES
            </div>
            <div className="tag-list">
              {data.job_roles.map((r, i) => (
                <div className={`tag${i === 0 ? " white" : ""}`} key={r}>
                  {r}
                </div>
              ))}
            </div>
          </div>
          <div className="r-cell dark">
            <div className="cell-label">SKILL GAP ANALYSIS</div>
            {Object.entries(data.skill_gap_analysis).map(([skill, status]) => (
              <div className="skill-item" key={skill}>
                <div className="skill-name">{skill}</div>
                <div className={`skill-status ${sc(status)}`}>
                  {clean(status)}
                </div>
              </div>
            ))}
          </div>
        </div>
        <div className="result-grid thirds">
          <div className="r-cell dark">
            <div className="cell-label">SALARY RANGE</div>
            <div className="salary-row">
              <div className="salary-item">
                <div className="salary-flag">INDIA</div>
                <div className="salary-value">{data.salary_range_india}</div>
              </div>
            </div>
            <div className="salary-row">
              <div className="salary-item">
                <div className="salary-flag">GLOBAL</div>
                <div className="salary-value">{data.salary_range_global}</div>
              </div>
            </div>
          </div>
          <div className="r-cell">
            <div className="cell-label">TOP COMPANIES</div>
            <div className="tag-list">
              {data.top_companies_hiring.map((c) => (
                <div className="tag" key={c}>
                  {c}
                </div>
              ))}
            </div>
          </div>
          <div className="r-cell dark">
            <div className="cell-label">CERTIFICATIONS</div>
            {data.certifications.map((c, i) => (
              <div
                key={c}
                style={{
                  padding: "10px 0",
                  borderBottom: "1px solid var(--grey-200)",
                  display: "flex",
                  gap: 10,
                }}
              >
                <span
                  style={{
                    fontFamily: "var(--font-mono)",
                    fontSize: 11,
                    color: "var(--grey-500)",
                  }}
                >
                  {String(i + 1).padStart(2, "0")}
                </span>
                <span
                  style={{
                    fontSize: 13,
                    color: "var(--grey-700)",
                    lineHeight: 1.4,
                  }}
                >
                  {c}
                </span>
              </div>
            ))}
          </div>
        </div>
        <div className="result-grid full">
          <div className="r-cell">
            <div className="cell-label">LEARNING MILESTONES</div>
            <div className="milestones-list">
              {data.monthly_milestones.map((m) => (
                <div className="milestone-row" key={m.phase}>
                  <div className="milestone-num">{m.phase}</div>
                  <div className="milestone-content">
                    <div className="milestone-title">{m.title}</div>
                    <div className="milestone-skills">
                      {m.skills_to_gain.map((s) => (
                        <div className="skill-chip" key={s}>
                          {s}
                        </div>
                      ))}
                    </div>
                    <div className="milestone-projects">
                      ↳ {m.projects.join(" · ")}
                    </div>
                    {m.resources.map((r) => (
                      <a
                        href={r.url}
                        target="_blank"
                        rel="noreferrer"
                        className="resource-link"
                        key={r.url + r.title}
                      >
                        {r.title}
                        <span className="res-hours">
                          {r.estimated_hours}h · {r.difficulty}
                        </span>
                      </a>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
        <div className="result-grid full">
          <div className="r-cell dark">
            <div className="cell-label">
              ESSENTIAL TOOLS — MANDATORY FOR EVERY DEVELOPER
            </div>
            {data.essential_tools.map((t) => (
              <div className="tool-item" key={t.url}>
                <div className="tool-badge">{t.difficulty.toUpperCase()}</div>
                <div className="tool-info">
                  <div className="tool-title">{t.title}</div>
                  <a
                    href={t.url}
                    target="_blank"
                    rel="noreferrer"
                    className="tool-url"
                  >
                    {t.url} · ~{t.estimated_hours}h
                  </a>
                </div>
              </div>
            ))}
          </div>
        </div>
        <div className="action-grid">
          <div className="action-card">
            <div className="action-label">⚡ DO THIS WEEK</div>
            <div className="action-text highlight">{data.immediate_action}</div>
          </div>
          <div
            className="action-card"
            style={{ background: "var(--grey-100)" }}
          >
            <div className="action-label">⚠️ BIGGEST RISK</div>
            <div className="action-text">{data.biggest_risk}</div>
          </div>
          <div className="action-card">
            <div className="action-label">📈 6-MONTH CHECK</div>
            <div className="action-text">{data.success_metric_6months}</div>
          </div>
        </div>
        <div className="advice-block">
          <div className="advice-text">
            {data.advice.split(data.user_name).map((part, i, arr) =>
              i < arr.length - 1 ? (
                <span key={i}>
                  {part}
                  <strong>{data.user_name}</strong>
                </span>
              ) : (
                <span key={i}>{part}</span>
              ),
            )}
          </div>
        </div>
        <div className="restart-bar">
          <button className="restart-btn" onClick={onRestart}>
            ← START OVER
          </button>
          <span
            style={{
              fontFamily: "var(--font-mono)",
              fontSize: 11,
              color: "var(--grey-500)",
              letterSpacing: 1,
            }}
          >
            Generated {new Date(data.generated_at).toLocaleString()}
          </span>
        </div>
      </div>
    </div>
  );
}

export default function App() {
  const [page, setPage] = useState("intake");
  const [profile, setProfile] = useState(null);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleIntake = (form) => {
    setProfile({
      ...form,
      current_year: +form.current_year,
      total_years: +form.total_years,
    });
    setPage("quiz");
  };

  const handleError = (title, lines) => {
    setError({ title, lines });
    setPage("error");
  };

  const handleQuizComplete = async (payload) => {
    setPage("loading");
    try {
      const res = await fetch(`${API_BASE}/recommend`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || `HTTP ${res.status}`);
      }
      const data = await res.json();
      setResult(data);
      setPage("result");
    } catch (e) {
      handleError("Cannot Generate Career Path", [
        `Could not reach ${API_BASE}/recommend`,
        `Error: ${e.message}`,
        "Make sure your FastAPI server is running:",
        "uvicorn main:app --reload --port 8000",
      ]);
    }
  };

  const restart = () => {
    setPage("intake");
    setProfile(null);
    setResult(null);
    setError(null);
  };

  return (
    <>
      <style>{css}</style>
      <SiteHeader page={page} />
      {page === "intake" && <IntakePage onSubmit={handleIntake} />}
      {page === "quiz" && (
        <QuizPage
          profile={profile}
          onComplete={handleQuizComplete}
          onError={handleError}
        />
      )}
      {page === "loading" && <LoadingPage />}
      {page === "result" && <ResultPage data={result} onRestart={restart} />}
      {page === "error" && (
        <ErrorPage title={error.title} lines={error.lines} onBack={restart} />
      )}
    </>
  );
}
