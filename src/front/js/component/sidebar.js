import React from "react";

const Sidebar = () => {
  return (
    <div className="sidebar">
      <ul className="nav flex-column">
        <li className="nav-item">
          <a className="nav-link active" href="/">
            Dashboard
          </a>
        </li>
        <li className="nav-item">
          <a className="nav-link" href="/products">
            Products
          </a>
        </li>
        <li className="nav-item">
          <a className="nav-link" href="/orders">
            Orders
          </a>
        </li>
        <li className="nav-item">
          <a className="nav-link" href="/analytics">
            Analytics
          </a>
        </li>
        <li className="nav-item">
          <a className="nav-link" href="/settings">
            Settings
          </a>
        </li>
      </ul>
    </div>
  );
};

export default Sidebar;
