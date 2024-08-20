import React from "react";
import { Routes, Route } from "react-router-dom";
import Books from "./Books";
import Lessons from "./Lessons";
import MangeLesson from './MangeLesson'
import Login from './Login'

function App() {

  return (
    <div className="App">
      
      <Routes>
        <Route path="/" element={<Books />}></Route>
        <Route path="/books/:bookid" element={<Lessons />} />
        <Route path="/login" element={<Login />}></Route>
        <Route path="/admin" element={<MangeLesson />}></Route>
        
      </Routes>
    </div>
  );
}

export default App;
