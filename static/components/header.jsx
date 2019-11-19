import React, { useState } from 'react';
import '../style/main.scss';

const headerStyle = {
  display: "flex",
  flexDirection: "row"
}

const Header = (props) => {
  const isLoggedIn = props.loggedIn;

  return (
    <div className="header">
      <div id="logged-user" className="tab">
        <p className="tab-text">
          { isLoggedIn ? "Welcome " + props.username : "Log in"}
        </p>
      </div>
      <div id="tab-main" className="tab">
        <p className="tab-text">Main</p>
      </div>
      <div id="tab-about" className="tab">
        <p className="tab-text">About</p>
      </div>
    </div>
  )
};

export default Header;