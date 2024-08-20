import React, { useEffect, useState } from "react";
import {
  Table,
  Button,
  Modal,
  Input,
  Upload,
  message,
  Grid ,
  Col, 
  Row
} from "antd";
import { UploadOutlined } from "@ant-design/icons";

import LoadingButton from "./LoadingButton";
import axios from './api';


const App = () => {
  const [isModalOpen, setIsModalOpen] = useState(false);  //是否打开上传弹窗
  const [bookName, setBookName] = useState("");  // 书籍名称
  const [booksList, setBooksList] = useState();  // 书籍列表
  const [loading, setLoading ] = useState(false)
  const [messageApi, contextHolder] = message.useMessage();  //分隔成功后的提示语
  const [lessonsList, setLessonsList] = useState();  //某个课程中lessons列表内容
  const [isListModalOpen,  setIsListModalOpen ] = useState(false)
  const [username, setUsername] = useState()


  

  const getUploadProps = (bookId) => ({
    name: "file",
    action: `/api/upload?bookid=${bookId}`,
    headers: {
      authorization: "authorization-text",
    },
    multiple: true,
    onChange(info) {
      if (info.file.status !== "uploading") {
        console.log(info.file, info.fileList);
      }
      if (info.file.status === "done") {
        message.success(`${info.file.name} file uploaded successfully`);
      } else if (info.file.status === "error") {
        message.error(`${info.file.name} file upload failed.`);
      }
    },
  });

  // 分隔音频文件
  const onClickSplit = (id, callback ) => {
    

    axios.get(`/api/split/${id}`).then(() => {
        callback();
        messageApi.open({
            type: "success",
            content: "批量分隔完成",
        });
    });
  };

// 分隔音频文件
const onClickSplitLesson = ( lessonid ) => {

    setLoading(true);

    axios.get(`/api/split/lesson/${lessonid}`).then(() => {
        setLoading(false);
        messageApi.open({
        type: "success",
        content: "批量分隔完成",
        });
    });
    };


  //查看lessons 列表
  const getLessonsList = ( id )=>{

    axios
    .get("/api/books/"+id )
    .then((r) => {
      setLessonsList(r.data );
      setIsListModalOpen(true)
    }).then( ()=> console.log( lessonsList )
    )
    .catch((error) => {
      console.error("Error fetching Lessons:", error);
    });

  }

  const columns = [
    {
      title: "ID",
      dataIndex: "id",
      key: "id",
    },
    {
      title: "书籍名称",
      dataIndex: "name",
      key: "name",
    },
    {
        title:"lessons数量",
        key:"total",
        render:(record)=>(
            <Button onClick={ () =>getLessonsList( record.id )   }  type="link" >{ record.total  }</Button>
        )
    },
    {
      title: "上传",
      //   dataIndex: "operation",
      key: "operation",
      render: (record) => (
        <Upload {...getUploadProps(record.id)}>
          <Button icon={<UploadOutlined />}>批量上传lessons</Button>
        </Upload>
      ),
    },
    {
      title: "分隔音频",
      key: "split",
      render: (record) => (
        <LoadingButton
        onClick={(callback) => onClickSplit(record.id, callback)}
          loading={loading}
          text="批量生成sentences"
        />
      ),
    },
  ];

  const fetchData = () => {

    axios.get("/api/cur_user").then( r => setUsername(  r.data.username ) )

    axios
      .get("/api/books")
      .then((r) => {
        setBooksList(r.data);
      })
      .catch((error) => {
        console.error("Error fetching books:", error);
      });
  };

  useEffect(() => fetchData(), []);

  const showModal = () => {
    setIsModalOpen(true);
  };


  const lessonsColumns = [
    {
        title: "ID",
        dataIndex: "id",
        key: "id",
      },
      {
        title: "课程名称",
        dataIndex: "name",
        key: "name",
      },
      {
        title: "是否分隔",
        dataIndex: "status",
        key: "status",
      },

      {
        title: "分隔音频",
        key: "split",
        render: (record) => (
            <LoadingButton
            onClick={(callback) => onClickSplit(record.id, callback)}
            loading={loading}
            text="生成sentences"
            />
          ),
      },
  ]


  const handleOk = (value) => {
    axios
      .post("/api/add_book", { book_name: bookName })
      .then((r) => {
        setIsModalOpen(false);
        setBookName("");
        fetchData();
      })
      .catch((error) => {
        console.error("Error creating book:", error);
        // 可以在这里处理错误，如提示用户创建失败等
      });
  };
  const handleCancel = () => {
    setIsModalOpen(false);

    setBookName("");
  };


  const handleCancelList = ()=>{
    setIsListModalOpen(false)
  }

  const logout = ()=>{
    axios.get( "/api/logout" ).then(  (r)=>{
        if (r.data.status === "ok"){
            window.location.href = '/login';
        }
    }  )
  }

  return (
    <div>

        <Row>
            <Col span={12}>
                <Button type="primary" onClick={showModal}>
                    新建
                </Button>
            </Col>
            <Col span={12} style={ { textAlign:"right" } } >
                {username}, 你好！  
                    <Button onClick={ logout } >退出登录</Button>
                {contextHolder}
            </Col>
        </Row>




      <Table columns={columns} dataSource={booksList} />

      <Modal title="课程列表"  open={isListModalOpen} footer={null} onCancel={  handleCancelList }  >
        <Table  columns={lessonsColumns} dataSource={lessonsList} />
      </Modal>

      <Modal
        title="新建书籍"
        open={isModalOpen}
        onOk={handleOk}
        onCancel={handleCancel}
      >
        <Input
          defaultValue={"请输入书籍名称"}
          value={bookName}
          onChange={(e) => setBookName(e.target.value)}
        />
      </Modal>
    </div>
  );
};
export default App;


