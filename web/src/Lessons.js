import React, { useState, useEffect, useRef } from "react";
import { Button, InputNumber, Select } from "antd";
import { Toast } from "antd-mobile";
import axios from "axios";
import { useParams } from "react-router-dom";
import { config } from "antd-mobile/es/components/toast/methods";

function Lessons() {
  // 获取url中的bookid
  const { bookid } = useParams();

  // 页面标题 book name
  const [bookName, setBookName] = useState(); 

  //  课程下拉列表的选项
  const [lessonList, setLessonList] = useState();

  //  某个课程所有句子列表
  const [sentenceList, setSentenceList] = useState();

  //  修改课程下拉菜单，更换课程
  const [lessonid, setLessonid] = useState(0);

  //   修改句子输入框， 更换句子
  const [sentenceSn, setSentenceSn] = useState(0);

  // 课程中句子总数
  const [total, setTotal] = useState(0);

  //句子的路径
  const [path, setPath] = useState();

  const audio = useRef();

  useEffect(() => {
    axios.get(`/api/books/${bookid}`).then((r) => {
      if (r.data !== "") {
        const lesson_list = r.data.lessons.map((item) => {
          return { value: item.id, label: item.name };
        });
        setLessonList(lesson_list);

        setBookName(r.data.book_name)

        console.log(bookName  )
      }
    });
  }, []);

  //  选择某课后，获取本课的所有句子
  const onChangeLesson = (value) => {
    axios.get(`/api/lessons/${value}`).then((r) => {
      console.log(r.data);

      setSentenceList(r.data);

      setLessonid(value);

      if (r.data.length > 0 ) {

        setSentenceSn(r.data[0].sn);

        setTotal(r.data.length);
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

  const preSentence = () => {
    if (sentenceSn === 1) {
      Toast.show({
        content: "已经是第一句了",
      });
    } else {
      setSentenceSn(sentenceSn - 1);
    }
  };

  const nextSentence = () => {

    if (sentenceSn === total ) {
        Toast.show({
          content: "已经是最后一句了",
        });
      } else {
        setSentenceSn(sentenceSn + 1);
      }

  };

  const handleInputChange = (value) => {
    if (value >= 1 && value <= total) {
      setSentenceSn(value);
    }
  };

  return (
    <div>
      <h1>{bookName}</h1>
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
          onChange={handleInputChange}
          value={sentenceSn}
        />{" "}
        共{total}句
      </div>

      <div style={{ margin: "10px 0px" }}>
        <audio ref={audio} controls src={path} autoPlay></audio>
      </div>

      <div>{path}</div>

      <div>
        <Button onClick={() => audio.current.play()}>重复</Button>
        <Button onClick={nextSentence}>下一句</Button>
        <Button onClick={preSentence}>上一句</Button>
      </div>
    </div>
  );
}

export default Lessons;
