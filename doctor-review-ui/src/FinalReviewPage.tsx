import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Lottie from "lottie-react";
import checkAnimation from "./checkmark.json";
import "./reviewpage.css";

export default function ReviewPage() {
  const navigate = useNavigate();

  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

  return (
    <div className="review-container">
      {/* ✅ Lottie Checkmark Animation */}
      <div 
        style={{ 
          display: "flex", 
          justifyContent: "center", 
          alignItems: "center", 
          width: "100%", 
          height: "150px",
        }}
      >
        <Lottie 
          animationData={checkAnimation} 
          style={{ 
            width: "100px", 
            height: "100px", 
            display: "block", 
            margin: "0 auto" 
          }} 
        />
      </div>
      {/* ✅ Success Message */}
      <h1 className="review-title">Review Complete</h1>
      <p className="review-subtext">Your notes have been saved successfully.</p>
    </div>
  );
}
