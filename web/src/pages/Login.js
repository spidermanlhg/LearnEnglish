import React from "react";
import { Button, Select, Form, Input, message } from "antd";
import axios from "axios";
import { useNavigate  } from "react-router-dom";
import md5 from "js-md5";

const App = () => {

    const navigate = useNavigate();
  const onFinish =async  (values) => {
    try {
      // 对密码进行MD5加密
      const encryptedPassword = md5(values.password.toString());
    //   console.log(encryptedPassword);
      const loginData = {
        ...values,
        password: encryptedPassword
      };

      const res = await axios.post("/api/login", loginData);
      
      if (res.data.status === "ok" ){
          // 存储用户token
          localStorage.setItem('token', res.data.user_info.id);
          navigate("/admin");
      } else {
          // 显示错误信息
          message.error(res.data.error || "登录失败，请检查用户名和密码");
      }
    } catch (error) {
      console.error("Login error:", error);
      message.error("登录失败，请稍后再试");
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
