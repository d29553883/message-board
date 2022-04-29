let board = document.querySelector("#board");
console.log(board);

function render(message, imageURL) {
  // render 留言
  let messageText = document.createTextNode(message);
  board.appendChild(messageText);
  let image = document.createElement("img");
  image.setAttribute("src", imageURL);
  image.setAttribute("class", "common-style");
  let hr = document.createElement("hr");
  board.appendChild(image);
  board.appendChild(hr);
}

window.addEventListener("load", () => {
  // 網頁載入時 render 畫面
  fetch("/api/board", {
    method: "GET",
  })
    .then((res) => res.json())
    .then((data) => {
      console.log(data.data);
      data.data.forEach((data) => render(data.message, data.image));
    });
});

let messageData = new FormData();
let image = "";
let file = document.getElementById("selectFile");
console.log(messageData);
file.addEventListener("change", (e) => {
  image = e.target.files[0];
  console.log(file.files);
  console.log(e.target);
  console.log(image);
});

document.getElementById("postBtn").addEventListener("click", function () {
  let message = document.getElementById("comment").value;
  if (message !== "" || image !== "") {
    alert("成功送出");
    console.log("圖檔名稱", image);
    messageData.append("message", message);
    messageData.append("file", image);
    // 帶資料給後端
    fetch("/api/board", {
      method: "POST",
      body: messageData,
    })
      .then((res) => res.json())
      .then((data) => {
        // console.log(`${data.ok}`);
        document.getElementById("comment").value = "";
        document.getElementById("selectFile").value = "";
        window.location.reload();
      })
      .catch((err) => console.log("出錯了...", err));
  } else {
    alert("請輸入留言或圖片");
  }
});
