import React, { useState } from 'react';
import ReactDOM from 'react-dom';

import Header from '../components/header.jsx';
import HomePage from '../components/home.jsx';

const headerContainer = document.getElementById('header');
const mainContainer = document.getElementById('main-content');

const header = <Header loggedIn={false}/>;
const homePage = <HomePage value="Please work!"></HomePage>;

ReactDOM.render(homePage, mainContainer)
ReactDOM.render(header, headerContainer)