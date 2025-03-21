import React from 'react';
import { NavBar } from 'antd-mobile';
import { useNavigate } from 'react-router-dom';
import './NavBar.css';

const CustomNavBar = ({ title }) => {
    const navigate = useNavigate();

    return (
        <NavBar
            onBack={() => navigate('/books')}
            className="custom-navbar"
        >
            {title}
        </NavBar>
    );
};

export default CustomNavBar;