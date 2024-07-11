import React, { useState, useEffect, useRef } from "react";
import { Button, InputNumber, Select } from "antd";
import axios from "axios";


function LessonDeatail() {
  const [contents, setContents] = useState();

  const [lesson, setLesson] = useState(1);

  const [sentence, setSentence] = useState(1);

  const [path, setPath] = useState();

  const audio = useRef();

  useEffect(() => {

    axios.get("/api/getLessons").then((r) => {

        setContents(r.data.lessons)

        setLesson( r.data.lessons[0].value )
        
    });

  }, []);

  useEffect(() => {

    setPath( `/api/sentence/${lesson}/${sentence}` )

  }, [ lesson, sentence ]);



  return (
    <div>
      <div style={{ textAlign: "left" }}>
        选择第几课：
        <Select
          value={ lesson }
          onChange={ setLesson }
          options={contents  }
          style={{ width: 120 }}
        />
      </div>
      <div style={{ textAlign: "left", marginTop: "10px" }}>
        选择第几句：
        <InputNumber
          min={0}
          max={100}
          onChange={setSentence}
          value={sentence}
        />
      </div>

      <div style={{ margin: "10px 0px" }}>
        <audio ref={audio} controls src={path} autoPlay ></audio>
      </div>

      <div>{path}</div>

      <div>
        <Button onClick={() => audio.current.play() }>重复</Button>
        <Button onClick={() =>  setSentence( sentence+1 ) }>下一句</Button>
        <Button onClick={() => setSentence( sentence-1 ) }>上一句</Button>
      </div>
    </div>
  );
}

export default LessonDeatail;
