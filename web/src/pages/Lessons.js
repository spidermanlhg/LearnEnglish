import React, { useState, useEffect, useRef } from "react";
import { Button, InputNumber } from "antd";
import { Toast } from "antd-mobile";
import axios from "axios";
import { useParams } from "react-router-dom";
import '../assets/styles/style.css'
import LessonSelect from '../components/LessonSelect'
import CustomNavBar from '../components/NavBar'

function Lessons() {
    const { bookid } = useParams(); // 获取url中的bookid
    const [bookName, setBookName] = useState(''); // 页面标题 book name
    const [sentenceList, setSentenceList] = useState(); //  某个课程所有句子列表

    const [lessonid, setLessonid] = useState(0); //  修改课程下拉菜单，更换课程

    const [sentenceIndex, setSentenceIndex] = useState(0); //   修改句子输入框， 更换句子

    const [path, setPath] = useState(); //句子音频文件的路径
    const [showSubtitle, setShowSubtitle] = useState(true); // 控制字幕显示/隐藏

    let total = sentenceList?.length 

    const useAudio = useRef();



    //更换课程
    const changeLesson = async (value) => {
        
        const { data } = await axios.get(`/api/lessons/${value}`);
        if (data.length) {
            setSentenceList(data); //把获取到的句子列表设置到sentence list中。
            setLessonid(value); // 在第几课下拉菜单中选中句子
            setSentenceIndex(data[0].sn); //句子在本课中的排序
        }
        
    };


    // 更换句子
    const changeSentence = (type, value) => {
        switch (type) {
            case "previous":   //上一句
                if (sentenceIndex === 1) {
                    Toast.show({
                        content: "已经是第一句了",
                    });
                } else {
                    console.log(sentenceIndex)
                    setSentenceIndex(sentenceIndex - 1);
                }
                break;
            case "next":   //下一句
                if (sentenceIndex === total ) {
                    Toast.show({
                        content: "已经是最后一句了",
                    });
                } else {
                    setSentenceIndex(sentenceIndex + 1);
                }
                break;
            case "input":   //输入数字切换句子
                if (value >= 1 && value <= total ) {
                    setSentenceIndex(value);
                }
                console.log(value)
                break;
            default:
                return; // 如果类型不匹配，函数退出
        }
    };

    const [currentText, setCurrentText] = useState(''); // 当前播放句子的文本

    // 获取书籍名称
    useEffect(() => {
        const fetchBookName = async () => {
            try {
                const { data } = await axios.get(`/api/books/${bookid}`);
                if (data && data[0]) {
                    setBookName(data[0].book_name);
                }
            } catch (error) {
                console.error('获取书籍名称失败:', error);
            }
        };
        fetchBookName();
    }, [bookid]);

    useEffect(() => {
        const obj = sentenceList?.find( item => item.sn === sentenceIndex);

        if (obj && obj.name) {
            const path = `/audio/${bookid}/${lessonid}/${obj.name}`; // 设置句子的音频文件路径
            setPath(path);
            setCurrentText(obj.text || ''); // 设置当前句子的文本
        }
    }, [bookid, lessonid, sentenceIndex, sentenceList]);



    return (
        <div>
            <CustomNavBar title={bookName} />
            
            <div style={{ textAlign: "left" }}>

                选择第几课：
                <LessonSelect
                    bookid = {bookid}
                    changeLesson = { (value) => changeLesson(value) }
                />

            </div>

            <div style={{ textAlign: "left", marginTop: "10px" }}>
                选择第几句：
                <InputNumber
                    min={0}
                    max={100}
                    onChange={(value) => changeSentence("input", value)}
                    value={sentenceIndex}
                    disabled={ total ?  false : true  }
                />
                <span className="ml5" >共{ total }句</span>
            </div>

            <div style={{ margin: "10px 0px" }}>
                <audio ref={useAudio} controls src={path} autoPlay></audio>
            </div>

            <div style={{ margin: "10px 0px", fontSize: "16px", padding: "10px", backgroundColor: "#f5f5f5", borderRadius: "4px", display: showSubtitle ? "block" : "none" }}>
                {currentText || "暂无字幕" }
            </div>

            {/* <div>{path}</div> */}

            <div>
                <Button  onClick={() => useAudio.current.play()}>重复</Button>
                <Button  className="ml5 mr5" onClick={() => changeSentence("previous")}>上一句</Button>
                <Button onClick={() => changeSentence("next")}>下一句</Button>
                <Button onClick={() => setShowSubtitle(!showSubtitle)}>{showSubtitle ? "隐藏字幕" : "显示字幕"}</Button>

            </div>
        </div>
    );
}

export default Lessons;
