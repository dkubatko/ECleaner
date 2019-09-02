import React, { useState } from 'react';

const headerStyle = {
  display: "flex",
  flexDirection: "row"
}

const Header = (props) => {
  const isLoggedIn = props.loggedIn;

  return (
    <div style={headerStyle}>
      <div id="logged-user" className="tab">
        { isLoggedIn ? "Welcome " + props.username : "Log in"}
      </div>
      <div id="tab-main" className="tab">
        Main
      </div>
      <div id="tab-about" className="tab">
        About
      </div>
    </div>
  )
};

export default Header;