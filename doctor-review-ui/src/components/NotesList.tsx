import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import axios from "axios";

interface Note {
  id: number;
  title: string;
  summary: string;
  status: string;
}

export default function NotesList() {
  const [notes, setNotes] = useState<Note[]>([]);

  useEffect(() => {
    axios.get("http://127.0.0.1:5000/notes/")
      .then(response => setNotes(response.data))
      .catch(error => console.error("Error fetching notes:", error));
  }, []);

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold">Doctor Review Notes</h2>
      <button>
        <Link to="/submit">Submit New Transcript</Link>
      </button>
      <ul className="mt-4">
        {notes.map(note => (
          <li key={note.id} className="p-4 border-b">
            <Link to={`/review/${note.id}`} className="text-blue-500 hover:underline">
              <h3 className="text-lg font-semibold">{note.title}</h3>
            </Link>
            <p className="text-gray-600">{note.summary}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}
