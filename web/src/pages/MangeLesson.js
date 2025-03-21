import React, { useEffect, useState } from "react";
import { Table, Button, Modal, Input, Upload, message, Col, Row, Checkbox } from "antd";
import { UploadOutlined } from "@ant-design/icons";
import { useSearchParams } from "react-router-dom";

import LoadingButton from "../components/LoadingButton";
import axios from "../services/api";

const App = () => {
  const [isModalOpen, setIsModalOpen] = useState(false); //是否打开上传弹窗
  const [bookName, setBookName] = useState(""); // 书籍名称
  const [booksList, setBooksList] = useState(); // 书籍列表
  const [loading, setLoading] = useState(false);
  const [messageApi, contextHolder] = message.useMessage(); //分隔成功后的提示语
  const [lessonsList, setLessonsList] = useState(); //某个课程中lessons列表内容
  const [isListModalOpen, setIsListModalOpen] = useState(false);
  const [username, setUsername] = useState();
  const [searchParams, setSearchParams] = useSearchParams();
  const [currentPage, setCurrentPage] = useState(1);
  const [isDeleteBookModalOpen, setIsDeleteBookModalOpen] = useState(false);
  const [selectedBookId, setSelectedBookId] = useState(null);
  const [deleteLoading, setDeleteLoading] = useState(false);

  const handleDeleteBook = () => {
    setDeleteLoading(true);
    axios.delete(`/api/admin/delete_book/${selectedBookId}`)
      .then(() => {
        setIsDeleteBookModalOpen(false);
        setSelectedBookId(null);
        fetchData();
        message.success('删除成功');
      })
      .catch(error => {
        console.error('Error deleting book:', error);
        if (error.response && error.response.status === 400 && error.response.data.message) {
          setIsDeleteBookModalOpen(false);
          setSelectedBookId(null);
          Modal.error({
            title: '无法删除书籍',
            content: '请先删除全部课程后，再删除书籍'
          });
        } else {
          message.error('删除失败');
        }
      })
      .finally(() => {
        setDeleteLoading(false);
      });
  };

  const getUploadProps = (bookId) => ({
    name: "file",
    action: `/api/admin/upload?bookid=${bookId}`,
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
        fetchData(); // 刷新数据
      } else if (info.file.status === "error") {
        message.error(`${info.file.name} file upload failed.`);
      }
    },
  });

  // 分隔音频文件
  const onClickSplit = (id, callback) => {
    axios.get(`/api/admin/split/${id}`).then(() => {
      callback();
      messageApi.open({
        type: "success",
        content: "批量分隔完成",
      });
    });
  };

  // 分隔音频文件
  const onClickSplitLesson = (lessonid, callback) => {
    setLoading(true);

    axios.get(`/api/admin/split/lesson/${lessonid}`).then(() => {
      setLoading(false);
      callback && callback();
      messageApi.open({
        type: "success",
        content: "批量分隔完成",
      });
      // 重新获取课程列表以更新状态
      if (lessonsList && lessonsList[0]) {
        getLessonsList(lessonsList[0].book_id);
      }
    });
  };

  //查看lessons 列表
  const getLessonsList = (id) => {
    axios
      .get("/api/books/" + id)
      .then((r) => {
        setLessonsList(r.data);
        setIsListModalOpen(true);
        // 重置全选状态和已选中的课程列表
        setSelectAll(false);
        setSelectedLessons([]);
      })
      .catch((error) => {
        console.error("Error fetching Lessons:", error);
      });
  };

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
      title: "lessons数量",
      key: "total",
      render: (record) => (
        <Button onClick={() => getLessonsList(record.id)} type="link">
          {record.total || 0}
        </Button>
      ),
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
    {
      title: "操作",
      key: "action",
      render: (record) => (
        <Button
          type="link"
          danger
          onClick={() => {
            setSelectedBookId(record.id);
            setIsDeleteBookModalOpen(true);
          }}
        >
          删除
        </Button>
      ),
    },
  ];

  const fetchData = () => {
    axios.get("/api/cur_user").then((r) => setUsername(r.data.username));

    axios
      .get("/api/books")
      .then((r) => {
        setBooksList(r.data);
      })
      .catch((error) => {
        console.error("Error fetching books:", error);
      });
  };

  useEffect(() => {
    // 从URL参数中获取页码
    const page = parseInt(searchParams.get("page")) || 1;
    setCurrentPage(page);
    fetchData();
  }, []);

  const showModal = () => {
    setIsModalOpen(true);
  };

  const [selectedLessons, setSelectedLessons] = useState([]);
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
  const [selectAll, setSelectAll] = useState(false);
  
  const handleDeleteConfirm = () => {
    axios.post('/api/admin/delete_lessons', { lesson_ids: selectedLessons })
      .then(() => {
        setIsDeleteModalOpen(false);
        setSelectedLessons([]);
        setSelectAll(false);
        getLessonsList(lessonsList[0].book_id);
        message.success('删除成功');
      })
      .catch(error => {
        console.error('Error deleting lessons:', error);
        message.error('删除失败');
      });
  };

  const handleSelectAll = () => {
    if (!selectAll) {
      const allLessonIds = lessonsList.map(lesson => lesson.id);
      setSelectedLessons(allLessonIds);
    } else {
      setSelectedLessons([]);
    }
    setSelectAll(!selectAll);
  };
  
  const lessonsColumns = [
    {
      title: '选择',
      dataIndex: 'select',
      key: 'select',
      render: (_, record) => (
        <Checkbox
          checked={selectedLessons.includes(record.id)}
          onChange={e => {
            if (e.target.checked) {
              setSelectedLessons([...selectedLessons, record.id]);
            } else {
              setSelectedLessons(selectedLessons.filter(id => id !== record.id));
              setSelectAll(false);
            }
          }}
        />
      )
    },
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
      render: (status) => status ? "是" : "否"
    },

    {
      title: "分隔音频",
      key: "split",
      render: (record) => (
        <LoadingButton
          onClick={(callback) => onClickSplitLesson(record.id, callback)}
          loading={loading}
          text="生成sentences"
        />
      ),
    },
  ];

  const handleOk = (value) => {
    axios
      .post("/api/admin/add_book", { book_name: bookName })
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

  const handleCancelList = () => {
    setIsListModalOpen(false);
    fetchData();
  };

  const logout = () => {
    axios.get("/api/logout").then((r) => {
      if (r.data.status === "ok") {
        window.location.href = "/login";
      }
    });
  };

  return (
    <div>
      <Row>
        <Col span={12}>
          <Button type="primary" onClick={showModal}>
            新建
          </Button>
        </Col>
        <Col span={12} style={{ textAlign: "right" }}>
          {username}, 你好！
          <Button onClick={logout}>退出登录</Button>
          {contextHolder}
        </Col>
      </Row>

      <Table 
        columns={columns} 
        dataSource={booksList}
        pagination={{
          current: currentPage,
          onChange: (page) => {
            setCurrentPage(page);
            setSearchParams({ page: page.toString() });
          }
        }}
      />

      <Modal
        title="课程列表"
        open={isListModalOpen}
        footer={null}
        onCancel={handleCancelList}
      >
        <div style={{ marginBottom: 16 }}>
          
          <Button
            onClick={handleSelectAll}
          >
            {selectAll ? '取消全选' : '全选'}
          </Button>

          <Button 
            type="primary" 
            danger 
            disabled={selectedLessons.length === 0}
            onClick={() => setIsDeleteModalOpen(true)}
            style={{ marginLeft: 10 }}
          >
            批量删除
          </Button>


        </div>
        <Table columns={lessonsColumns} dataSource={lessonsList} />
      </Modal>

      <Modal
        title="确认删除"
        open={isDeleteModalOpen}
        onOk={handleDeleteConfirm}
        onCancel={() => setIsDeleteModalOpen(false)}
      >
        <p>确定要删除选中的{selectedLessons.length}个课程吗？</p>
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

      <Modal
        title="确认删除"
        open={isDeleteBookModalOpen}
        onOk={handleDeleteBook}
        onCancel={() => {
          setIsDeleteBookModalOpen(false);
          setSelectedBookId(null);
        }}
        confirmLoading={deleteLoading}
      >
        <p>确定要删除这本书吗？删除后将无法恢复。</p>
      </Modal>
    </div>
  );
};
export default App;
