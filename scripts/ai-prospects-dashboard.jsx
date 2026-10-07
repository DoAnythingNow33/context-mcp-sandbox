import { useState, useCallback } from "react";

const INDUSTRIES = [
  "Marketing Agency", "Creative Agency", "PR Agency", "Accounting Firm",
  "Legal Practice", "Real Estate Agency", "Recruiting/Staffing",
  "IT Services / MSP", "E-commerce Brand", "Healthcare Practice",
  "Construction & Trades", "Financial Advisory", "Insurance Brokerage",
  "Architecture / Design Studio", "Event Management",
];

const REGIONS = [
  "United States", "United Kingdom", "Canada", "Australia", "Western Europe",
];

const SIZE_OPTIONS = [
  { label: "Micro (1–10)", value: "1-10 employees" },
  { label: "Small (11–50)", value: "11-50 employees" },
  { label: "Medium (51–200)", value: "51-200 employees" },
];

const PAIN_POINTS = [
  "Content creation bottlenecks",
  "Manual data entry / admin overhead",
  "Slow proposal / document generation",
  "Poor lead follow-up / CRM hygiene",
  "Repetitive customer support queries",
  "Reporting & analytics delays",
];

function Tag({ label, selected, onClick }) {
  return (
    <button
      onClick={onClick}
      style={{
        padding: "6px 14px",
        borderRadius: "20px",
        border: selected ? "2px solid #00FF87" : "2px solid #2a2a3a",
        background: selected ? "rgba(0,255,135,0.12)" : "rgba(255,255,255,0.04)",
        color: selected ? "#00FF87" : "#888",
        fontSize: "12px",
        fontFamily: "'DM Mono', monospace",
        cursor: "pointer",
        transition: "all 0.2s",
        whiteSpace: "nowrap",
      }}
    >
      {label}
    </button>
  );
}

function ProspectCard({ prospect, index }) {
  const [expanded, setExpanded] = useState(false);
  return (
    <div
      style={{
        background: "rgba(255,255,255,0.03)",
        border: "1px solid rgba(255,255,255,0.08)",
        borderRadius: "12px",
        padding: "16px 20px",
        marginBottom: "10px",
        transition: "border-color 0.2s",
        borderLeft: "3px solid #00FF87",
        cursor: "pointer",
        animation: "fadeSlide 0.4s ease both",
        animationDelay: `${Math.min(index * 20, 600)}ms`,
      }}
      onClick={() => setExpanded(!expanded)}
    >
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", gap: "12px" }}>
        <div style={{ flex: 1 }}>
          <div style={{ display: "flex", alignItems: "center", gap: "10px", marginBottom: "4px" }}>
            <span style={{
              background: "rgba(0,255,135,0.15)",
              color: "#00FF87",
              fontSize: "10px",
              fontFamily: "'DM Mono', monospace",
              padding: "2px 8px",
              borderRadius: "10px",
              letterSpacing: "0.05em",
            }}>#{String(index + 1).padStart(2, "0")}</span>
            <strong style={{ color: "#f0f0f0", fontSize: "15px", fontFamily: "'Outfit', sans-serif" }}>
              {prospect.company_name}
            </strong>
          </div>
          <div style={{ color: "#999", fontSize: "12px", fontFamily: "'DM Mono', monospace" }}>
            {prospect.industry} · {prospect.size} · {prospect.location}
          </div>
        </div>
        <div style={{ display: "flex", gap: "8px", flexShrink: 0 }}>
          <span style={{
            background: prospect.channel === "LinkedIn" ? "rgba(10,102,194,0.2)" : "rgba(255,165,0,0.15)",
            color: prospect.channel === "LinkedIn" ? "#5ba3f5" : "#ffaa44",
            fontSize: "11px",
            fontFamily: "'DM Mono', monospace",
            padding: "3px 9px",
            borderRadius: "8px",
          }}>{prospect.channel}</span>
          <span style={{
            background: "rgba(255,255,255,0.06)",
            color: "#ccc",
            fontSize: "11px",
            fontFamily: "'DM Mono', monospace",
            padding: "3px 9px",
            borderRadius: "8px",
          }}>Fit: {prospect.fit_score}/10</span>
        </div>
      </div>

      {expanded && (
        <div style={{ marginTop: "14px", borderTop: "1px solid rgba(255,255,255,0.07)", paddingTop: "14px" }}>
          <div style={{ marginBottom: "10px" }}>
            <div style={{ color: "#666", fontSize: "10px", fontFamily: "'DM Mono', monospace", marginBottom: "4px", textTransform: "uppercase", letterSpacing: "0.1em" }}>AI Opportunity</div>
            <div style={{ color: "#ddd", fontSize: "13px", fontFamily: "'Outfit', sans-serif", lineHeight: "1.6" }}>{prospect.ai_opportunity}</div>
          </div>
          <div style={{ marginBottom: "10px" }}>
            <div style={{ color: "#666", fontSize: "10px", fontFamily: "'DM Mono', monospace", marginBottom: "4px", textTransform: "uppercase", letterSpacing: "0.1em" }}>Opening Line</div>
            <div style={{
              color: "#b8ffdc",
              fontSize: "13px",
              fontFamily: "'Outfit', sans-serif",
              lineHeight: "1.6",
              fontStyle: "italic",
              background: "rgba(0,255,135,0.05)",
              padding: "10px 14px",
              borderRadius: "8px",
              borderLeft: "2px solid rgba(0,255,135,0.3)",
            }}>"{prospect.opening_line}"</div>
          </div>
          {prospect.linkedin_search && (
            <div>
              <div style={{ color: "#666", fontSize: "10px", fontFamily: "'DM Mono', monospace", marginBottom: "4px", textTransform: "uppercase", letterSpacing: "0.1em" }}>LinkedIn Search</div>
              <div style={{ color: "#5ba3f5", fontSize: "12px", fontFamily: "'DM Mono', monospace" }}>{prospect.linkedin_search}</div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default function App() {
  const [industries, setIndustries] = useState(["Marketing Agency", "Recruiting/Staffing"]);
  const [region, setRegion] = useState("United States");
  const [sizes, setSizes] = useState(["11-50 employees", "51-200 employees"]);
  const [pains, setPains] = useState(["Content creation bottlenecks", "Manual data entry / admin overhead"]);
  const [prospects, setProspects] = useState([]);
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [statusMsg, setStatusMsg] = useState("");
  const [week, setWeek] = useState("");
  const [error, setError] = useState("");

  const toggleItem = (list, setList, item) => {
    setList(prev => prev.includes(item) ? prev.filter(x => x !== item) : [...prev, item]);
  };

  const fetchBatch = async (batchNum, industryList, sizeList, regionVal, painList) => {
    const prompt = `You are a B2B sales prospecting expert. Generate exactly 25 fictional but realistic SMB prospects (batch ${batchNum} of 2) that would benefit from AI workflow automation.

Target criteria:
- Industries: ${industryList.join(", ")}
- Company sizes: ${sizeList.join(", ")}
- Region: ${regionVal}
- Pain points: ${painList.join(", ")}

IMPORTANT: Return ONLY a raw JSON object. No markdown, no backticks, no explanation. Start your response with { and end with }.

Use this exact format:
{"prospects":[{"company_name":"Acme Marketing Co","industry":"Marketing Agency","size":"18 employees","location":"Austin, TX","channel":"LinkedIn","fit_score":8,"ai_opportunity":"They manually write all client reports which takes 2 days per week — AI could automate this to minutes.","opening_line":"I noticed Acme runs monthly performance reports for 30+ clients — we've helped similar agencies cut that process from days to hours.","linkedin_search":"Marketing Director OR Agency Owner at marketing agency"},{"company_name":"...","industry":"...","size":"...","location":"...","channel":"Cold Call","fit_score":7,"ai_opportunity":"...","opening_line":"...","linkedin_search":"..."}]}

Generate all 25 entries. Keep opening_line under 200 characters. Keep ai_opportunity under 200 characters.`;

    const response = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "anthropic-dangerous-direct-browser-access": "true",
      },
      body: JSON.stringify({
        model: "claude-sonnet-4-20250514",
        max_tokens: 5000,
        messages: [{ role: "user", content: prompt }],
      }),
    });

    if (!response.ok) {
      const errBody = await response.text();
      throw new Error(`API error ${response.status}: ${errBody}`);
    }

    const data = await response.json();
    const text = data.content?.map(b => b.text || "").join("") || "";
    if (!text) throw new Error("Empty response from API");

    // Extract JSON object
    const start = text.indexOf("{");
    const end = text.lastIndexOf("}");
    if (start === -1 || end === -1) throw new Error(`No JSON object found in batch ${batchNum}`);

    const jsonStr = text.slice(start, end + 1);
    const parsed = JSON.parse(jsonStr);
    if (!Array.isArray(parsed.prospects) || parsed.prospects.length === 0) {
      throw new Error(`No prospects array in batch ${batchNum}`);
    }
    return parsed.prospects;
  };

  const generateProspects = useCallback(async () => {
    if (industries.length === 0) { setError("Pick at least one industry."); return; }
    setError("");
    setLoading(true);
    setProspects([]);
    setProgress(5);

    const now = new Date();
    setWeek(`Week of ${now.toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" })}`);

    try {
      setStatusMsg("Generating first 25 prospects...");
      const t1 = setInterval(() => setProgress(p => Math.min(p + 3, 45)), 400);
      const batch1 = await fetchBatch(1, industries, sizes, region, pains);
      clearInterval(t1);
      setProgress(50);
      setProspects(batch1);

      setStatusMsg("Generating next 25 prospects...");
      const t2 = setInterval(() => setProgress(p => Math.min(p + 3, 90)), 400);
      const batch2 = await fetchBatch(2, industries, sizes, region, pains);
      clearInterval(t2);
      setProgress(100);
      setProspects([...batch1, ...batch2]);
      setStatusMsg("");
    } catch (err) {
      setError(`Error: ${err.message}`);
      console.error("Prospect generation failed:", err);
    } finally {
      setLoading(false);
    }
  }, [industries, region, sizes, pains]);

  const exportCSV = () => {
    const headers = ["#", "Company", "Industry", "Size", "Location", "Channel", "Fit Score", "AI Opportunity", "Opening Line", "LinkedIn Search"];
    const rows = prospects.map((p, i) => [
      i + 1, `"${p.company_name}"`, `"${p.industry}"`, `"${p.size}"`, `"${p.location}"`, p.channel,
      p.fit_score, `"${(p.ai_opportunity||"").replace(/"/g,"'")}"`, `"${(p.opening_line||"").replace(/"/g,"'")}"`, `"${(p.linkedin_search||"").replace(/"/g,"'")}"`
    ]);
    const csv = [headers, ...rows].map(r => r.join(",")).join("\n");
    const blob = new Blob([csv], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `prospects-${week.replace(/[^a-z0-9]/gi, "-")}.csv`;
    a.click();
  };

  return (
    <div style={{ minHeight: "100vh", background: "#0a0a12", color: "#f0f0f0", fontFamily: "'Outfit', sans-serif" }}>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');
        * { box-sizing: border-box; margin: 0; padding: 0; }
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: #0a0a12; }
        ::-webkit-scrollbar-thumb { background: #2a2a3a; border-radius: 3px; }
        @keyframes fadeSlide {
          from { opacity: 0; transform: translateY(10px); }
          to { opacity: 1; transform: translateY(0); }
        }
        @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.4} }
      `}</style>

      {/* Header */}
      <div style={{
        borderBottom: "1px solid rgba(255,255,255,0.07)",
        padding: "20px 32px",
        display: "flex", alignItems: "center", justifyContent: "space-between",
        background: "rgba(255,255,255,0.02)",
        position: "sticky", top: 0, zIndex: 100,
      }}>
        <div style={{ display: "flex", alignItems: "center", gap: "14px" }}>
          <div style={{
            width: "36px", height: "36px", borderRadius: "10px",
            background: "linear-gradient(135deg, #00FF87, #00b8d4)",
            display: "flex", alignItems: "center", justifyContent: "center", fontSize: "18px",
          }}>⚡</div>
          <div>
            <div style={{ fontSize: "17px", fontWeight: 600, letterSpacing: "-0.01em" }}>ProspectAI</div>
            <div style={{ fontSize: "11px", color: "#555", fontFamily: "'DM Mono', monospace" }}>Weekly Lead Engine</div>
          </div>
        </div>
        {prospects.length > 0 && (
          <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
            <span style={{ color: "#555", fontSize: "12px", fontFamily: "'DM Mono', monospace" }}>{week} · {prospects.length} leads</span>
            <button onClick={exportCSV} style={{
              background: "rgba(0,255,135,0.1)", border: "1px solid rgba(0,255,135,0.3)",
              color: "#00FF87", padding: "8px 16px", borderRadius: "8px",
              fontFamily: "'DM Mono', monospace", fontSize: "12px", cursor: "pointer",
            }}>↓ Export CSV</button>
          </div>
        )}
      </div>

      <div style={{ display: "flex", minHeight: "calc(100vh - 73px)" }}>
        {/* Sidebar */}
        <div style={{
          width: "300px", flexShrink: 0,
          borderRight: "1px solid rgba(255,255,255,0.07)",
          padding: "24px 20px", overflowY: "auto",
          background: "rgba(255,255,255,0.01)",
        }}>
          {[
            { label: "Target Industries", items: INDUSTRIES, selected: industries, setSelected: setIndustries },
          ].map(({ label, items, selected, setSelected }) => (
            <div key={label} style={{ marginBottom: "24px" }}>
              <div style={{ fontSize: "11px", color: "#555", fontFamily: "'DM Mono', monospace", textTransform: "uppercase", letterSpacing: "0.1em", marginBottom: "10px" }}>{label}</div>
              <div style={{ display: "flex", flexWrap: "wrap", gap: "6px" }}>
                {items.map(i => <Tag key={i} label={i} selected={selected.includes(i)} onClick={() => toggleItem(selected, setSelected, i)} />)}
              </div>
            </div>
          ))}

          <div style={{ marginBottom: "24px" }}>
            <div style={{ fontSize: "11px", color: "#555", fontFamily: "'DM Mono', monospace", textTransform: "uppercase", letterSpacing: "0.1em", marginBottom: "10px" }}>Company Size</div>
            <div style={{ display: "flex", flexWrap: "wrap", gap: "6px" }}>
              {SIZE_OPTIONS.map(s => <Tag key={s.value} label={s.label} selected={sizes.includes(s.value)} onClick={() => toggleItem(sizes, setSizes, s.value)} />)}
            </div>
          </div>

          <div style={{ marginBottom: "24px" }}>
            <div style={{ fontSize: "11px", color: "#555", fontFamily: "'DM Mono', monospace", textTransform: "uppercase", letterSpacing: "0.1em", marginBottom: "10px" }}>Region</div>
            <div style={{ display: "flex", flexWrap: "wrap", gap: "6px" }}>
              {REGIONS.map(r => <Tag key={r} label={r} selected={region === r} onClick={() => setRegion(r)} />)}
            </div>
          </div>

          <div style={{ marginBottom: "28px" }}>
            <div style={{ fontSize: "11px", color: "#555", fontFamily: "'DM Mono', monospace", textTransform: "uppercase", letterSpacing: "0.1em", marginBottom: "10px" }}>Pain Points to Target</div>
            <div style={{ display: "flex", flexWrap: "wrap", gap: "6px" }}>
              {PAIN_POINTS.map(p => <Tag key={p} label={p} selected={pains.includes(p)} onClick={() => toggleItem(pains, setPains, p)} />)}
            </div>
          </div>

          {error && (
            <div style={{ color: "#ff6b6b", fontSize: "12px", fontFamily: "'DM Mono', monospace", marginBottom: "12px", padding: "10px", background: "rgba(255,107,107,0.08)", borderRadius: "8px", wordBreak: "break-word" }}>{error}</div>
          )}

          <button
            onClick={generateProspects}
            disabled={loading}
            style={{
              width: "100%", padding: "14px",
              background: loading ? "rgba(0,255,135,0.05)" : "linear-gradient(135deg, #00FF87, #00d4aa)",
              border: loading ? "1px solid rgba(0,255,135,0.2)" : "none",
              borderRadius: "10px",
              color: loading ? "#00FF87" : "#0a0a12",
              fontFamily: "'Outfit', sans-serif", fontWeight: 700, fontSize: "14px",
              cursor: loading ? "not-allowed" : "pointer", transition: "all 0.2s",
            }}
          >
            {loading ? "⚡ Generating..." : "⚡ Generate 50 Prospects"}
          </button>
        </div>

        {/* Main */}
        <div style={{ flex: 1, padding: "28px 28px", overflowY: "auto" }}>
          {loading && (
            <div style={{ textAlign: "center", paddingTop: "80px" }}>
              <div style={{ fontSize: "48px", marginBottom: "20px", animation: "pulse 1.4s ease-in-out infinite" }}>⚡</div>
              <div style={{ fontSize: "16px", color: "#ccc", marginBottom: "8px", fontWeight: 500 }}>{statusMsg || "Generating your prospects..."}</div>
              <div style={{ color: "#555", fontSize: "12px", fontFamily: "'DM Mono', monospace", marginBottom: "24px" }}>
                {progress < 50 ? "Batch 1/2 · Researching companies..." : "Batch 2/2 · Crafting opening lines..."}
              </div>
              <div style={{ width: "280px", margin: "0 auto", height: "4px", background: "rgba(255,255,255,0.08)", borderRadius: "2px", overflow: "hidden" }}>
                <div style={{ height: "100%", width: `${progress}%`, background: "linear-gradient(90deg, #00FF87, #00d4aa)", borderRadius: "2px", transition: "width 0.4s ease" }} />
              </div>
              <div style={{ color: "#444", fontSize: "11px", fontFamily: "'DM Mono', monospace", marginTop: "8px" }}>{progress}%</div>
              {prospects.length > 0 && (
                <div style={{ marginTop: "24px", color: "#555", fontSize: "12px", fontFamily: "'DM Mono', monospace" }}>
                  ✓ {prospects.length} prospects loaded so far...
                </div>
              )}
            </div>
          )}

          {!loading && prospects.length === 0 && (
            <div style={{ textAlign: "center", paddingTop: "100px" }}>
              <div style={{ fontSize: "56px", marginBottom: "20px", opacity: 0.2 }}>🎯</div>
              <div style={{ fontSize: "20px", fontWeight: 600, marginBottom: "8px", color: "#555" }}>No prospects yet</div>
              <div style={{ color: "#444", fontSize: "13px", fontFamily: "'DM Mono', monospace" }}>
                Configure your targeting on the left, then hit Generate.
              </div>
            </div>
          )}

          {prospects.length > 0 && (
            <div>
              <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: "20px" }}>
                <div>
                  <div style={{ fontSize: "20px", fontWeight: 700, marginBottom: "2px" }}>
                    {prospects.length} Prospects {loading ? <span style={{ color: "#555", fontSize: "14px" }}>(loading...)</span> : "Generated"}
                  </div>
                  <div style={{ fontSize: "12px", color: "#555", fontFamily: "'DM Mono', monospace" }}>Click any row to expand details + opening line</div>
                </div>
                <div style={{ display: "flex", gap: "16px", fontSize: "12px", fontFamily: "'DM Mono', monospace", color: "#555" }}>
                  <span>🔗 LinkedIn: {prospects.filter(p => p.channel === "LinkedIn").length}</span>
                  <span>📞 Cold Call: {prospects.filter(p => p.channel === "Cold Call").length}</span>
                  <span>⭐ Avg fit: {(prospects.reduce((a, p) => a + (p.fit_score || 0), 0) / prospects.length).toFixed(1)}/10</span>
                </div>
              </div>
              {prospects.map((p, i) => <ProspectCard key={i} prospect={p} index={i} />)}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
