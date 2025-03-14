import { useLocation, useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import "./reviewpage.css";
import ChatBot from "react-simple-chatbot";
import { ThemeProvider } from "styled-components";
import axios from "axios";
import ReactMarkdown from "react-markdown"; // ✅ Added Markdown support

// 🔹 Toggle Dummy Data ON/OFF
const useDummyData = true; // Set to false to use API data from app.tsx

export default function ReviewPage() {
  const location = useLocation();
  const navigate = useNavigate();

  // 🔹 Get API Data from `app.tsx` (or default to empty object)
  const apiData = location.state || {};

  // 🔹 Dummy Data (Used when `useDummyData = true`)
  const dummyData = {
    transcript: "Patient complains of persistent headache and fatigue.",
    transcriptionSummary: "### Summary\n**Patient reports frequent headaches and fatigue.** Suggested hydration & sleep improvement.",
    analysisSummary: [
      {
        nlp_type: "nlp_general",
        analysis_result: {
          possible_conditions: ["Migraine", "Tension-type headache", "Chronic fatigue syndrome"],
          recommended_tests: ["Complete blood count (CBC)", "Thyroid function tests"],
          referral_suggestions: ["Neurologist", "Sleep specialist"],
          treatment_guidelines: ["Use over-the-counter analgesics", "Ensure adequate hydration"],
        },
      },
      {
        nlp_type: "nlp_mental",
        analysis_result: {
          possible_conditions: ["Anxiety", "Depression", "Chronic stress"],
          lifestyle_recommendations: ["Mindfulness meditation", "Cognitive-behavioral therapy (CBT)"],
          referral_suggestions: ["Psychologist", "Therapist"],
          treatment_guidelines: ["Therapy sessions", "Medication if needed"],
        },
      },
      {
        nlp_type: "nlp_nutrition",
        analysis_result: {
          lifestyle_recommendations: ["Increase protein intake", "Ensure vitamin B12 levels"],
          risk_factors: ["Dietary deficiencies", "Dehydration"],
        },
      },
    ],
  };

  // 🔹 Use API Data if Available, Otherwise Use Dummy Data
  const transcript = useDummyData ? dummyData.transcript : apiData.transcript || "";
  const transcriptionSummary = useDummyData ? dummyData.transcriptionSummary : apiData.transcriptionSummary || "";
  const analysisSummary = useDummyData ? dummyData.analysisSummary : apiData.analysisSummary || [];

  const [doctorNotes, setDoctorNotes] = useState("");
  const [showTranscript, setShowTranscript] = useState(false);
  const [selectedAgent, setSelectedAgent] = useState<string>("");
  const [expandedSections, setExpandedSections] = useState<Record<string, boolean>>({
    general: false,
    mental: false,
    nutrition: false,
  });

  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

  const handleApprove = () => {
    navigate("/final-review", {
      state: {
        transcript,
        doctorNotes,
      },
    });
  };

  const toggleSection = (section: string) => {
    setExpandedSections((prev) => ({
      ...prev,
      [section]: !prev[section],
    }));
  };

  // ✅ Function to Render Analysis Summary Sections Dynamically
  const renderAnalysisSection = (title: string, type: string) => {
    const sectionData = analysisSummary?.filter((entry: any) => entry.nlp_type === type) || [];

    if (!sectionData.length) return null; // ✅ Prevents rendering empty sections

    return (
      <div className="expandable-section">
        <button className="expandable-header" onClick={() => toggleSection(type)}>
          {title + " AI generated"}
        </button>

        {expandedSections[type] && (
          <div className="analysis-grid">
            {sectionData.map((entry: any, index: number) =>
              Object.entries(entry.analysis_result || {}).map(([label, values], subIndex) => (
                <div className="analysis-card" key={`${index}-${subIndex}`}>
                  <div className="card-label">{label.replace(/_/g, " ")}</div>
                  <div className="card-content">
                    {Array.isArray(values) ? values.map((item, i) => <div key={i}>{item}</div>) : <p>{values || "N/A"}</p>}
                  </div>
                </div>
              ))
            )}
          </div>
        )}
      </div>
    );
  };

  // ✅ Chatbot Theme
  const theme = {
    background: "#f5f8fb",
    headerBgColor: "#007bff",
    headerFontColor: "#fff",
    headerFontSize: "18px",
    botBubbleColor: "#007bff",
    botFontColor: "#fff",
    userBubbleColor: "#f1f1f1",
    userFontColor: "#4a4a4a",
  };

  // ✅ Chatbot Steps
  const steps = [
    {
      id: "1",
      message: "Hello! Which AI Agent would you like to ask?",
      trigger: "agentSelection",
    },
    {
      id: "agentSelection",
      options: [
        { value: "mental", label: "🧠 Mental Health Agent", trigger: "continueChat" },
        { value: "general", label: "🏥 General Medicine Agent", trigger: "continueChat" },
        { value: "nutrition", label: "🥗 Nutrition Agent", trigger: "continueChat" },
      ],
    },
    {
      id: "continueChat",
      message: "Ask your question below.",
      trigger: "userInput",
    },
    {
      id: "userInput",
      user: true,
      trigger: "fetchAIResponse",
    },
    {
      id: "fetchAIResponse",
      component: <AIResponse />,
      asMessage: true,
      trigger: "userInput",
    },
  ];

  // ✅ AI Response Component - Uses Dummy Responses for Mental Health Agent
  function AIResponse(props: any) {
    const [aiMessage, setAiMessage] = useState<string>("🤖 Thinking...");

    useEffect(() => {
      if (!props.previousStep?.message) {
        setAiMessage("No question received.");
        return;
      }

      const userMessage = props.previousStep?.message;
      axios
        .post("http://127.0.0.1:5000/chat-agent", {
          message: userMessage,
          agent_type: selectedAgent,
        })
        .then((response) => {
          setAiMessage(response.data.reply || "🤖 No response from AI.");
        })
        .catch(() => {
          setAiMessage("Error fetching response from AI.");
        });
    }, [props.previousStep?.message]);

    return <div>{aiMessage}</div>;
  }

  return (
    <div className="review-container">
      <h1 className="review-title">Medical Summary & Insights</h1>

      {/* ✅ AI-Generated Notes with Markdown Support */}
      <div className="notes-section">
  <h3>AI-Generated Notes</h3>
  {transcriptionSummary ? (
    <div 
      className="notes-editor markdown-textarea" 
      contentEditable={false} // ✅ Prevents editing
      suppressContentEditableWarning={true} // ✅ Suppresses React warning
    >
      <ReactMarkdown>{transcriptionSummary}</ReactMarkdown>
    </div>
  ) : (
    <p className="no-data">No notes available.</p>
  )}
</div>

      {/* ✅ Analysis Summary Sections */}
      {renderAnalysisSection("General Medicine", "nlp_general")}
      {renderAnalysisSection("Mental Health", "nlp_mental")}
      {renderAnalysisSection("Nutrition", "nlp_nutrition")}

      {/* ✅ Collapsible Transcript */}
      <div className="collapsible-section">
        <button className="toggle-btn" onClick={() => setShowTranscript(!showTranscript)}>
          {showTranscript ? "Hide Transcript" : "Show Transcript"}
        </button>
        {showTranscript && <pre className="transcript-text">{transcript}</pre>}
      </div>

      {/* ✅ Doctor's Final Notes */}
      <div className="doctor-notes-section">
        <h3>✍️ Doctor’s Final Review & Notes</h3>
        <textarea className="doctor-notes" placeholder="Enter your notes..." value={doctorNotes} onChange={(e) => setDoctorNotes(e.target.value)} />
      </div>

      {/* ✅ Floating Chatbot */}
      <ThemeProvider theme={theme}>
        <ChatBot steps={steps} floating={true} />
      </ThemeProvider>

      {/* ✅ Submit Button */}
      <button className="approve-button" onClick={handleApprove}>
        Submit
      </button>
    </div>
  );
}
