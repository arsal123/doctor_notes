import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";

export default function ReviewEditor() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [note, setNote] = useState("");

  useEffect(() => {
    fetch(`http://localhost:5000/notes/${id}`)
      .then((res) => res.json())
      .then((data) => setNote(data.note))
      .catch((error) => console.error("Error fetching note:", error));
  }, [id]);

  const handleApprove = async () => {
    try {
      await fetch(`http://localhost:5000/approve-note/${id}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ note }),
      });
      alert("Note approved!");
      navigate("/");
    } catch (error) {
      console.error("Error approving note:", error);
    }
  };

  return (
    <div>
      <h2>Review Note</h2>
      <textarea value={note} onChange={(e) => setNote(e.target.value)} rows={10} cols={50} />
      <button onClick={handleApprove}>Approve</button>
    </div>
  );
}
