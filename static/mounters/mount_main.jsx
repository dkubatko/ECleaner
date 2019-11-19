import React, { useState } from 'react';
import ReactDOM from 'react-dom';

import Header from '../components/header.jsx';
import HomePage from '../components/home.jsx';

const headerContainer = document.getElementById('header');
const mainContainer = document.getElementById('main-content');

const header = <Header loggedIn={true} username="User1437"/>;
const homePage = <HomePage value="x1c6 and counting?"></HomePage>;

ReactDOM.render(homePage, mainContainer)
ReactDOM.render(header, headerContainer)