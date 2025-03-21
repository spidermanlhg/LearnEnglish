import { useState, useEffect } from "react";
import {  Select } from "antd";
import axios from "axios";



const LessonSelect = ( {bookid , changeLesson } )=> {

    const [lessonList, setLessonList] = useState(); //  课程下拉列表的选项

    //通过bookid 获取 课程内容。
    const fetchBookData = async () => {
       
        const { data } = await axios.get(`/api/books/${bookid}`)

        // console.log( data )

        if (data) {
            const lessons = data.map( item => ({
                value: item.id,
                label: item.name,
            }));
            setLessonList(lessons);
        //     // setBookName(data[0].book_name);  //接口返回的bookname放在里每一个lesson中，随便取一条数据中的book_name都可以。
        }

        
    };

    useEffect( ()=>{ fetchBookData() }, [] )


    return (
        <Select
            defaultValue={"请选择"}
            onChange={value => changeLesson(value)}
            options={lessonList}
            style={{ width: 120 }}
        />
    )


}

export default LessonSelect;