
import './App.css';
import Home from './UI Components/orders_page';
import React, { useState, useEffect } from 'react';
import syncreonlogo from './Images/logo.png'



function App() {
  const [headerClass, setHeaderClass] = useState('');

  useEffect(() => {
    window.addEventListener('scroll', handleScroll);

    return () => {
      window.removeEventListener('scroll', handleScroll);
    };
  }, []);

  const handleScroll = () => {
    const scrollPosition = window.pageYOffset;

    if (scrollPosition > 100) {
      setHeaderClass('scrolled');
    } else {
      setHeaderClass('');
    }
  };

  return (
    <>
      <div className={`Header ${headerClass}`}>
      <img src={syncreonlogo} alt="Logo" />
        {/* <h1>Syncreon Technical Challenge</h1> */}
      </div>
      <div className="App">
        <Home />
      </div>
    </>
  );
}
export default App;
