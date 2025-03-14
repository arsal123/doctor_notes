import { useState } from "react";
import axios from "axios";
import { Routes, Route, useNavigate } from "react-router-dom";
import ReviewPage from "./ReviewPage";
import FinalReviewPage from "./FinalReviewPage";
import Header from "./components/header/Header"; // Import the Header component
import "./App.css"; // Import styles

export default function App() {
  const [transcript, setTranscript] = useState(`Doctor: Good morning! How are you feeling today?
  Patient: Good morning, doctor. I’ve been feeling really tired lately, and I often wake up feeling completely exhausted.
  
  Doctor: I see. Have you been experiencing any stress or anxiety recently?
  Patient: Yes, actually. My job has been really demanding, and I’ve been feeling overwhelmed. Sometimes I feel anxious for no reason.
  
  Doctor: That’s understandable. Have you had any headaches or dizziness?
  Patient: Yes, I get frequent headaches, especially in the mornings. Also, I feel lightheaded sometimes.
  
  Doctor: I see. What about your diet? Are you eating well?
  Patient: Honestly, not really. I’ve been eating a lot of fast food and skipping meals. I’ve also lost weight recently.
  
  Doctor: That could be affecting your energy levels. Have you been exercising?
  Patient: Not much. I used to, but I just don’t have the motivation anymore.
  
  Doctor: I’d like to check your medical history. Have you had any chronic conditions or past health issues?
  Patient: I had anemia a few years ago, and my doctor said I had low vitamin D levels.
  
  Doctor: That’s important to know. I’ll request your medical records to check if there’s any pattern. Also, I’d like to run some blood tests.
  
  Patient: That sounds good. Should I be worried?
  
  Doctor: Not necessarily. But based on your symptoms, I’d recommend talking to a nutrition specialist to improve your diet, and maybe consulting a mental health expert to manage stress better.
  
  Patient: I appreciate that. I’ll follow up with those specialists.
  
  Doctor: Great! In the meantime, try to maintain a balanced diet, drink plenty of water, and get some light exercise. I’ll follow up with your test results soon.`);
  
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async () => {
    if (!transcript.trim()) {
      alert("Please enter a transcript before submitting.");
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post("http://127.0.0.1:5000/process-transcript", { transcript });

      navigate("/review", {
        state: {
          transcript,
          transcriptionSummary: response.data.transcription_summary,
          analysisSummary: response.data.analysis_summary, // Pass full structured data
        },
      });

    } catch (error) {
      console.error("Error processing transcript:", error);
      alert("❌ Failed to generate notes. Please try again.");
    }
    setLoading(false);
  };

  return (
    <>
      <Header /> {/* Fixed header at the top */}
      <Routes>
        <Route
            path="/"
            element={
              <div className="call-ended-container">
                {/* LEFT SIDE - IMAGE */}
                <div className="call-ended-left"></div>

                {/* RIGHT SIDE - CALL SUMMARY */}
                <div className="call-ended-right">
                  <h1>Call Ended</h1>
                  <h2>AI-Powered Medical Review</h2>

                  <textarea
                    className="textarea-input"
                    placeholder="📝 Enter doctor-patient transcript here..."
                    value={transcript}
                    onChange={(e) => setTranscript(e.target.value)}
                  ></textarea>

                  <button className="submit-button" onClick={handleSubmit} disabled={loading}>
                    {loading ? "Processing..." : "Generate Notes"}
                  </button>
                </div>
              </div>
                }
          />

          {/* Review Page */}
        <Route path="/review" element={<ReviewPage />} />
        <Route path="/final-review" element={<FinalReviewPage />} />

      </Routes>
    </>
  );
}
