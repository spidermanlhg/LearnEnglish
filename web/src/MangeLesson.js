import React, { useEffect, useState } from "react";
import { Space, Table, Tag, Button, Modal, Input, Upload, message } from "antd";
import { UploadOutlined } from "@ant-design/icons";
import axios from "axios";

const App = () => {


    const [isModalOpen, setIsModalOpen] = useState(false);
    const [bookName, setBookName] = useState("");
    const [booksList, setBooksList] = useState();

    
  const getUploadProps = (bookId)  => ({
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

  const onClickSplit =( id )=>{
    axios.get( `/api/split/${id}`   )
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
      //   dataIndex: "operation",
        key: "split",
        render: (record) => (

            <Button  onClick={ () => onClickSplit( record.id )  } >批量生成sentences</Button>
        ),
      },
    
  ];



  const fetchData = () => {
    axios
      .get("/api/books")
      .then((r) => {
        console.log(r);
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
  const handleOk = (value) => {
    axios
      .post("/api/add_book", { book_name: bookName })
      .then((r) => {
        console.log("Book created successfully:", r.data);
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

  return (
    <div>
      <Button type="primary" onClick={showModal}>
        新建
      </Button>

      <Table columns={columns} dataSource={booksList} />

      <Modal
        title="Basic Modal"
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
