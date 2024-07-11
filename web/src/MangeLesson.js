
import './App.css';
import { UploadOutlined } from '@ant-design/icons';
import { Button, Input, message, Upload, Form, Space } from 'antd';
import axios from 'axios';
import { useRef, useState } from 'react';

const  URL = "http://127.0.0.1:5000";




const MangeLesson = () => {

    const catId = useRef()

    const [file, setFile] = useState([]);

    const [uploading, setUploading] = useState(false);

    const [action, setAction] = useState('/api/upload/')

    const [path, setPath] = useState()

    const changeCat = (e) => {

        setAction('api/upload/' + e.target.value)
    }

    const props = {

        beforeUpload:(file)=>{
            setFile(file)
            return false
        }

    };

    const creatFolder=( values )=>{

        axios.post(  URL+ "/api/create", values  )


    }

    const changePath = (v) =>{

        setPath(v.target.value)

    }
    
    const [messageApi, contextHolder] = message.useMessage();


    const handleUpload=()=>{


        const formData = new FormData()
        formData.append('file', file)

        axios.post( URL+ '/api/upload/'+path , formData).then(res => {

            // console.log( res['data'] )
            
            if (res['data']){
                messageApi.open({
                    type: 'success',
                    content: '上传成功',
                  });
            }else{
                messageApi.open({
                    type: 'error',
                    content: '上传失败',
                });
            }

            
        })
    }



    return (
        <div style={{ textAlign: "left" }} >

            {contextHolder}

            <div>
                上传音频：
                <Input style={{width:"100px"}} placeholder='填写上传的路径'  onChange={ changePath } />
                <Upload {...props}>
                    <Button icon={<UploadOutlined />}>选择音频</Button>
                </Upload>

                <Button onClick={handleUpload}>上传</Button>
            </div>



            <div style={{ margin: "10px 0" }} >
                <Form>
                    填写音频路径：
                    <Space.Compact >
                        <Input />
                        <Button type="primary">提交</Button>
                    </Space.Compact>
                </Form>

            </div>
        </div>
    )
};


export default MangeLesson;

