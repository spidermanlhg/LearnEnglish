import React, { useState } from "react";
import { Button } from "antd";

const LoadingButton = ({ onClick, text }) => {

  const [loading, setLoading] = useState(false);

  const handleClick = () => {
    setLoading(true);
    onClick(() => setLoading(false)); // Pass setLoading function as a callback
  };

  return (
    <Button onClick={handleClick} loading={ loading}>
      {text}
    </Button>
  );
};

export default LoadingButton;