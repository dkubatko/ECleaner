import React, { useState } from 'react';

export function HomePage(props) {
  const [loggedIn, setLoggedIn] = useState(true);
  // const loggedIn = true;
  return (
    <div>
      You are { loggedIn ? 'logged in' : 'not logged in'}<br/>
      Value passed: {props.value}
    </div>
  );
}

export default HomePage;
