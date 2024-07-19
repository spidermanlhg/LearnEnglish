import React, { useState, useEffect, useRef } from "react";
import { Button, InputNumber, Select } from "antd";
import axios from "axios";
import { useParams } from "react-router-dom";

function Lessons() {
  // 获取url中的bookid
  const { bookid } = useParams();

  //  设置课程下拉列表的选项
  const [lessonList, setLessonList] = useState();

  //  设置某个课程所有句子列表
  const [sentenceList, setSentenceList] = useState();

  //  更换课程
  const [lessonid, setLessonid] = useState(0);

  //   更换句子
  const [sentenceSn, setSentenceSn] = useState(0);

  //句子的路径
  const [path, setPath] = useState();

  const audio = useRef();

  useEffect(() => {
    axios.get(`/api/books/${bookid}`).then((r) => {
      if (r.data !== "") {
        const lesson_list = r.data.map((item) => {
          return { value: item.id, label: item.name };
        });
        setLessonList(lesson_list);
      }
    });
  }, []);

  //  选择某课后，调取该课的句子列表
  const onChangeLesson = (value) => {
    axios.get(`/api/lessons/${value}`).then((r) => {
      console.log(r.data);

      setSentenceList(r.data);

      setLessonid(value);

      if (r.data.length > 0) {
        setSentenceSn(r.data[0].sn);
      }
    });
  };

  useEffect(() => {
    const obj = sentenceList?.find((item) => {
      return item.sn === sentenceSn;
    });

    if (obj && obj.name) {
      setPath(`/audio/${bookid}/${lessonid}/${obj.name}`);
    }
  }, [bookid, lessonid, sentenceSn, sentenceList]);

  return (
    <div>
      <div style={{ textAlign: "left" }}>
        选择第几课：
        <Select
          defaultValue={"请选择"}
          onChange={(value) => onChangeLesson(value)}
          options={lessonList}
          style={{ width: 120 }}
        />
      </div>

      <div style={{ textAlign: "left", marginTop: "10px" }}>
        选择第几句：
        <InputNumber
          min={0}
          max={100}
          onChange={setSentenceSn}
          value={sentenceSn}
        />
      </div>

      <div style={{ margin: "10px 0px" }}>
        <audio ref={audio} controls src={path} autoPlay></audio>
      </div>

      <div>{path}</div>

      <div>
        <Button onClick={() => audio.current.play()}>重复</Button>
        <Button onClick={() => setSentenceSn(sentenceSn + 1)}>下一句</Button>
        <Button onClick={() => setSentenceSn(sentenceSn - 1)}>上一句</Button>
      </div>
    </div>
  );
}

export default Lessons;
