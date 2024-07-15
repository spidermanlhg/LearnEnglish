import React, { useState, useEffect } from "react";
import { Routes, Route } from "react-router-dom";
import Books from "./Books";
import Lessons from "./Lessons";
import axios from "axios";

function App() {

  return (
    <div className="App">
      
      <Routes>
        <Route path="/" element={<Books />}></Route>
        <Route path="/books/:bookid" element={<Lessons />} />
        {/* <Route path="/mange" element={<MangeLesson />}></Route> */}
        
      </Routes>
    </div>
  );
}

export default App;
