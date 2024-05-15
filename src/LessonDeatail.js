import React, { useState, useEffect,useRef} from "react";
import { Button, InputNumber, Select, message  } from "antd";

import axios from 'axios';
import { useAsyncError } from "react-router-dom";
// import { Button, message, Upload } from 'antd';



const getPath = (l, s ) => {

    s = String(s).padStart(3, '0') + ".mp3"
    return  `/uploads/${l}/${s}` 
  
}

function LessonDeatail(){


    const [lesson, setLesson] = useState(1)

    const [sentence, setSentence] = useState(1)

    const [path, setPath] = useState( getPath(1,1) )

    const [messageApi, contextHolder] = message.useMessage();


    // 目录
    const contents=   [
            {
            value: 1,
            label: 'SPRING',
        },
        {
            value: 2,
            label: 'THE STORY',
        },
        {
            value: 3,
            label: 'A LOST BUTTON',
        },
        {
            value: 4,
            label: 'A SWIM',
        },
        {
            value: 5,
            label: 'THE LETTER',
        }
    ]   

    const audio = useRef()

    const changeLesson=(v)=>{
        setLesson(v); 
        changePath( v, 1  )
    }

    const changeSentence=(v)=>{
        setSentence( v )

        changePath( lesson, v  )
    }


    useEffect( ()=>{
        
        try{
            audio.current.play()
        }catch{
            messageApi.open({
                type: 'error',
                content: 'This is an error message',
              });
        }
            

    }, [ path ] )


    const changePath = (l, s )=>{

        setSentence( s )
        setPath( getPath(l, s ) )

    }


    return(
        <div  >
            
            <div style={{ textAlign:"left" }} > 
                选择第几课：<Select defaultValue="SPRING" onChange={changeLesson}  options={contents}   style={{width: 120}}/>
                
            </div>
            <div style={{ textAlign:"left", marginTop:"10px" }} >
                选择第几句：<InputNumber min={0} max={100}    onChange={ changeSentence } value={sentence}  />
            </div>


            <div style={{margin:"10px 0px"}}  ><audio ref={audio}  controls src={ path }  ></audio></div>

            <div>{ path }</div>

            <div>
            <Button onClick={ ()=>  audio.current.play() }>重复</Button>
                <Button onClick={ ()=> changePath( lesson, sentence+1 )  }>下一句</Button>
                <Button onClick={ ()=> changePath( lesson, sentence-1 )  }>上一句</Button>
            </div>
        </div>
    )
}


export default LessonDeatail