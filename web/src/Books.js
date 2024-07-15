import React, { useEffect, useState } from "react";
import axios from "axios";
import { List } from "antd-mobile";

function Book() {
  const [data, setData] = useState();

  useEffect(() => {
    const getBooks = () => {
      axios.get("/api/books").then((r) => setData(r.data));
    };
    getBooks();
  }, []);

  const clickHandler = (id) => {
    console.log(id);

    window.location.href = `books/${id}`;
  };

  return (
    <>
      <List header="书籍列表">
        {data?.map((item) => (
          <List.Item onClick={(id) => clickHandler(item.id)}>
            {" "}
            {item.name}{" "}
          </List.Item>
        ))}
      </List>
    </>
  );
}

export default Book;
