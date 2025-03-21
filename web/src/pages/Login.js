import React from "react";
import { Button, Select, Form, Input } from "antd";
import axios from "axios";
import { useNavigate  } from "react-router-dom";

const App = () => {

    const navigate = useNavigate();
  const onFinish =async  (values) => {

    const res = await axios.post("/api/login", values);
    
    if (res.data.status === "ok" ){
        // 存储用户token
        localStorage.setItem('token', res.data.user_info.id);
        navigate("/admin");
    }


  };
  const onFinishFailed = (errorInfo) => {
    console.log("Failed:", errorInfo);
  };

  const handleChange = (value) => {
    console.log(`selected ${value}`);
  };

  return (
    <div>
      <Form
        name="basic"
        labelCol={{
          span: 8,
        }}
        wrapperCol={{
          span: 16,
        }}
        style={{
          maxWidth: 600,
        }}
        initialValues={{
            "role":"2"
          
        }}
        onFinish={onFinish}
        onFinishFailed={onFinishFailed}
        autoComplete="off"
      >
        <Form.Item
          label="role"
          name="role"
          rules={[
            {
              required: true,
            },
          ]}
        >
          <Select
            defaultValue="2"
            onChange={handleChange}
            options={[
              {
                value: "1",
                label: "普通用户",
              },
              {
                value: "2",
                label: "管理员",
              },
            ]}
          />
        </Form.Item>

        <Form.Item
          label="Username"
          name="username"
          rules={[
            {
              required: true,
              message: "Please input your username!",
            },
          ]}
        >
          <Input />
        </Form.Item>

        <Form.Item
          label="Password"
          name="password"
          rules={[
            {
              required: true,
              message: "Please input your password!",
            },
          ]}
        >
          <Input.Password />
        </Form.Item>

        <Form.Item
          wrapperCol={{
            offset: 8,
            span: 16,
          }}
        >
          <Button type="primary" htmlType="submit">
            Submit
          </Button>
        </Form.Item>
      </Form>
    </div>
  );
};

export default App;
