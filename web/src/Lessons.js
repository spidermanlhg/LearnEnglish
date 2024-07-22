import React, { useState, useEffect, useRef } from "react";
import { Button, InputNumber, Select } from "antd";
import { Toast } from "antd-mobile";
import axios from "axios";
import { useParams } from "react-router-dom";

function Lessons() {
  const { bookid } = useParams(); // 获取url中的bookid

  const [bookName, setBookName] = useState(); // 页面标题 book name

  const [lessonList, setLessonList] = useState(); //  课程下拉列表的选项

  const [sentenceList, setSentenceList] = useState(); //  某个课程所有句子列表

  const [lessonid, setLessonid] = useState(0); //  修改课程下拉菜单，更换课程

  const [sentenceIndex, setSentenceIndex] = useState(0); //   修改句子输入框， 更换句子

  const [total, setTotal] = useState(0); // 课程中句子总数

  const [path, setPath] = useState(); //句子音频文件的路径

  const useAudio = useRef();


//通过bookid 获取 课程内容。
  const fetchBookData = async () => {
    try {
      const { data } = await axios.get(`/api/books/${bookid}`);

      if (data ) {
        const lessons = data.lessons.map(item => ({ value: item.id, label: item.name }));
        setLessonList(lessons);
        setBookName(data.book_name);
      }
    } catch (error) {
      console.error('Error fetching book data:', error);
    }
  };


//选择某课后，获取本课的所有句子
const fetchLessonSentences = async (value) => {
    try {
      const { data } = await axios.get(`/api/lessons/${value}`);
      if (data.length) {
        setSentenceList(data);  //把获取到的句子列表设置到sentence list中。
        setLessonid(value);  // 在第几课下拉菜单中选中句子
        setSentenceIndex(data[0].sn);  //句子在本课中的排序
        setTotal(data.length);  //句子总数
      }
    } catch (error) {
      console.error('Error fetching sentences:', error);
    }
  };


  useEffect(() => {
    fetchBookData()
  }, []);


  useEffect(() => {
    const obj = sentenceList?.find (item => item.sn === sentenceIndex );

    if (obj && obj.name) {
      const path = `/audio/${bookid}/${lessonid}/${obj.name}`;  // 设置句子的音频文件路径
      setPath(path) 
    }
  }, [bookid, lessonid, sentenceIndex, sentenceList]);



  // 更换句子
const changeSentence = (type, value) => {
  
    switch (type) {
        
      case 'previous':
        if (sentenceIndex === 1) {
            Toast.show({
              content: "已经是第一句了",
            });
          } else {
              setSentenceIndex(sentenceIndex - 1);
          }
        break;
      case 'next':
        if (sentenceIndex === total) {
            Toast.show({
              content: "已经是最后一句了",
            });
          } else {
              setSentenceIndex(sentenceIndex + 1);
          }
        break;

      case 'change':
        if (value >= 1 && value <= total) {
            setSentenceIndex(value);
        }

        break;
      default:
        return; // 如果类型不匹配，函数退出
    }
  

  };


  return (
    <div>
      <h1>{bookName}</h1>
      <div style={{ textAlign: "left" }}>
        选择第几课：
        <Select
          defaultValue={"请选择"}
          onChange={(value) => fetchLessonSentences(value)}
          options={lessonList}
          style={{ width: 120 }}
        />
      </div>

      <div style={{ textAlign: "left", marginTop: "10px" }}>
        选择第几句：
        <InputNumber
          min={0}
          max={100}
          onChange={ value=> changeSentence( "input", value ) }
          value={sentenceIndex}
        />{" "}
        共{total}句
      </div>

      <div style={{ margin: "10px 0px" }}>
        <audio ref={useAudio} controls src={path} autoPlay></audio>
      </div>

      <div>{path}</div>

      <div>
        <Button onClick={ () => useAudio.current.play()}>重复</Button>
        <Button onClick={ ()=> changeSentence("next")}>下一句</Button>
        <Button onClick={ ()=>  changeSentence("pre")}>上一句</Button>
      </div>
    </div>
  );
}

export default Lessons;
