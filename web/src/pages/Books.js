import React, { useEffect, useState } from "react";
import axios from "axios";
import { List } from "antd-mobile";
import { useNavigate } from "react-router-dom";
function Book() {

    const navigate = useNavigate();

    const [data, setData] = useState();


    //   通过books接口获取全部书籍列表
    const getBooks = async () => {
        const res = await axios.get("/api/books");
        setData(res.data);
    };


    useEffect(() => {
        getBooks();
    }, []);


    return (
        <>
            <List header="书籍列表">
                {data?.map((item) => (
                    <List.Item onClick={id => navigate(`/books/${item.id}`)}>
                        {item.name}{" "}
                    </List.Item>
                ))}
            </List>
        </>
    );
}

export default Book;
