import React, { useState, useEffect } from "react";
import axios from "axios";

const App = () => {
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [image, setImage] = useState(null);
  const [images, setImages] = useState([]);
  const BASE_URL = "http://127.0.0.1:5000/";
  const IMAGES_URL = "http://127.0.0.1:5000/display";
  const DISPLAY_URL = "http://127.0.0.1:5000/static/upload/";
  useEffect(() => {
    axios(IMAGES_URL).then((result) => setImages(result.data));
  }, []);

  const handleTitle = (e) => {
    e.preventDefault();
    setTitle(e.target.value);
  };

  const handleContent = (e) => {
    e.preventDefault();
    setContent(e.target.value);
  };

  const handleImage = (e) => {
    e.preventDefault();
    console.log(e.target.files);
    setImage(e.target.files[0]);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log(title, content, image);

    const form_data = new FormData();
    form_data.append("image", image, image.name);
    form_data.append("title", title);
    form_data.append("content", content);

    axios
      .post(BASE_URL, form_data, {
        headers: {
          "content-type": "multipart/form-data",
        },
      })
      .then((res) => {
        console.log(res.data);
      })
      .catch((err) => console.log(err));

    setTitle("");
    setImage(null);
    setContent("");
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <p>
          title:
          <input
            type="text"
            placeholder="Title"
            id="title"
            value={title}
            onChange={handleTitle}
            required
          ></input>
        </p>
        <p>
          content:
          <input
            type="text"
            placeholder="Content"
            id="content"
            value={content}
            onChange={handleContent}
            required
          ></input>
        </p>
        <p>
          <input
            type="file"
            id="image"
            accept="image/png,image/jpeg"
            onChange={handleImage}
            required
          ></input>
        </p>
        <button type="submit">Post</button>
      </form>
      {images.length > 0 &&
        images.map((img, i) => (
          <div key={i}>
            <h1>{img.title}</h1>
            <img src={`${DISPLAY_URL}${img.image}`} alt={img.title}></img>
          </div>
        ))}
    </div>
  );
};

export default App;
