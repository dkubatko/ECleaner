import React, { useState } from 'react';

export function HomePage(props) {
  const [cleaned, setCleaned] = useState(false);

  const onCleanEmail = () => {
    fetch("/clean")
      .then(res => res.json())
      .then((result) => {
        console.log(result);
      })
  }
  return (
    <button onClick={onCleanEmail}>{ cleaned ? "Cleaned!" : "Let's do it!"}</button>
  );
}

export default HomePage;
