import React from "react";
import "./Header.css"; // Import styles

const Header: React.FC = () => {
  return (
    <header className="header">
      <div className="logo-container">
        <img src="https://www.teladochealth.com/content/dam/tdh-www/us/en/images/logos/TDH_Logo_Full_Color_RGB.svg" alt="Medical Logo" className="logo" />
        <span className="logo-text">Consult Genie</span>
      </div>
      <nav className="nav-links">
        <a href="/">Home</a>
        <a href="#">About</a>
        <a href="#">Services</a>
        <a href="#">Contact</a>
      </nav>
    </header>
  );
};

export default Header;
