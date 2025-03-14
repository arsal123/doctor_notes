import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function TranscriptInput() {
  const [transcript, setTranscript] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await fetch("http://localhost:5000/process-transcript", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ transcript }),
      });
      const data = await response.json();
      navigate(`/review/${data.noteId}`);
    } catch (error) {
      console.error("Error processing transcript:", error);
    }
  };

  return (
    <div>
      <h2>Submit Consultation Transcript</h2>
      <form onSubmit={handleSubmit}>
        <textarea
          value={transcript}
          onChange={(e) => setTranscript(e.target.value)}
          rows={5}
          cols={50}
        />
        <button type="submit">Process Transcript</button>
      </form>
    </div>
  );
}
