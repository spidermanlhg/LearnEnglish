import React, { useState, useEffect, useRef } from "react";
import { Button, InputNumber, Select } from "antd";
import axios from "axios";
import { useParams } from "react-router-dom";

function Lessons() {
    // 获取url中的bookid
  const { bookid } = useParams();

//  设置课程菜单的选项
  const [lessonOptions, setLessonOptions] = useState();

//  设置某个课程所有句子列表
  const [sentenceList, setSentenceList] = useState();

//  更换课程
  const [lesson, setLesson] = useState(0);

//   更换句子
  const [sentence, setSentence] = useState(0);

  //句子的路径
  const [path,setPath] = useState();


  const audio = useRef();

  useEffect(() => {
    axios.get(`/api/books/${bookid}`).then((r) => {
      if (r.data !== "") {
        const lesson_list = r.data.map((item) => {
          return { value: item.id, label: item.name };
        });
        setLessonOptions(lesson_list);
      }
    });
  }, []);

  //  选择某课后，调取该课的句子列表
  const onChangeLesson = (value) => {
    axios.get(`/api/lessons/${value}`).then((r) => {
      console.log(r);


      setSentenceList( r.data )

      setLesson( value );

      setPath(  `/data/${bookid}/${value}/${r.data[ sentence ].name}`  )



    });
  };


    useEffect(() => {
        setPath(  `/data/${bookid}/${lesson}/${sentence}`  )
    }, [sentence]);

  return (
    <div>
      <div style={{ textAlign: "left" }}>
        选择第几课：
        <Select
          defaultValue={"请选择 "}
          onChange={(value) => onChangeLesson(value)}
          options={lessonOptions}
          style={{ width: 120 }}
        />
      </div>

      {/* <div style={{ textAlign: "left", marginTop: "10px" }}>
        选择第几句：
        <InputNumber
          min={0}
          max={100}
          onChange={setSentence}
          value={sentence}
        />
      </div> */}

      <div style={{ margin: "10px 0px" }}>
        <audio ref={audio} controls src={sentence} autoPlay></audio>
      </div>

      <div>{path}</div>

      {
        sentenceList.map( item=> <div> {item.name} </div> )
      }

      <div>
        <Button onClick={() => audio.current.play()}>重复</Button>
        <Button onClick={() => setSentence(sentence + 1)}>下一句</Button>
        <Button onClick={() => setSentence(sentence - 1)}>上一句</Button>
      </div>
    </div>
  );
}

export default Lessons;
