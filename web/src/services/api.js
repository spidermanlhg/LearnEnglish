// api.js
import axios from "axios";
import { useNavigate } from "react-router-dom";

const instance = axios.create({
  baseURL: "/",
});


instance.interceptors.response.use(

  (response) => response,

  (error) => {
    if (error.response && error.response.status === 401) {
      const navigate = useNavigate();
      navigate("/login");
    }
    return Promise.reject(error);
  }
);

export default instance;
