import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import Books from "../pages/Books";
import Lessons from "../pages/Lessons";
import MangeLesson from '../pages/MangeLesson'
import Login from '../pages/Login'

const PrivateRoute = ({ element }) => {
  const isAuthenticated = localStorage.getItem('token');
  return isAuthenticated ? element : <Navigate to="/login" replace />;
};

function App() {

  return (
    <div className="App">
      
      <Routes>
        <Route path="/" element={<Books />}></Route>
        <Route path="/books" element={<Books />} /> {/* 添加这一行 */}
        <Route path="/books/:bookid" element={<Lessons />} />
        <Route path="/login" element={<Login />}></Route>
        <Route path="/admin" element={<PrivateRoute element={<MangeLesson />} />}></Route>
        
      </Routes>
    </div>
  );
}

export default App;
