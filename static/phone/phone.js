var result_url;

document.querySelector("#upload-area").onclick = () => {
  const inp = document.createElement("input");
  inp.type = "file";
  inp.multiple = true;
  inp.accept = "image/*";

  inp.onchange = (e) => {
    e.preventDefault();

    handleFiles(e.target.files);
  };

  inp.click();
};

document.querySelector("#upload").onclick = async () => {
  if (images.length == 0) return;

  const url = await process();
  result_url = url;
  displayCollage(url);
};

function displayCollage(url, orient) {
  document.querySelector("#result").innerHTML = `<img src=${url} id="collage">`;

  if (document.querySelector("#download")) return;

  const downButton = document.createElement("button");
  downButton.id = "download";
  downButton.textContent = "Download";

  downButton.onclick = () => {
    var downloadLink = document.createElement("a");
    downloadLink.href = result_url;
    downloadLink.download = "collage.png";

    downloadLink.click();
  };

  document.querySelector("#buttons").prepend(downButton);
}
