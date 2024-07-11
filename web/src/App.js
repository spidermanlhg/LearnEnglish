import React, { useState, useEffect } from "react";
import { Routes, Route } from "react-router-dom";

import LessonCat from "./LessonCat";
import LessonDeatail from "./LessonDeatail";
import MangeLesson from "./MangeLesson";
import Book from "./Book";

import axios from "axios";

function App() {
  const [data, setData] = useState();

  useEffect(() => {
    axios.get("/api/getLessons").then((r) => setData( r.data ) );
  }, []);

  return (
    <div className="App">
      <h1>{data?.name}</h1>
      <Routes>
        <Route path="/cat" element={<LessonCat />} />
        <Route path="/lesson" element={<LessonDeatail />} />
        <Route path="/mange" element={<MangeLesson />}></Route>
        <Route path="/book" element={<Book />}></Route>
      </Routes>
      {/* <LessonDeatail></LessonDeatail> */}
    </div>
  );
}

export default App;
