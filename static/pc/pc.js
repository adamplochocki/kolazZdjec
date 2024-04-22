const dropZone = document.querySelector("#upload-area");

document.querySelector("#upload").onclick = async () => {
  if (images.length == 0) return;

  clearZone();
  const url = await process();
  displayCollage(url);
};

dropZone.onclick = () => {
  const inp = document.createElement("input");
  inp.type = "file";
  inp.multiple = true;
  inp.accept = "image/*";

  inp.onchange = (e) => {
    e.preventDefault();

    dropZone.classList.remove("highlight");
    handleFiles(e.target.files);
  };

  inp.click();
};

["dragenter", "dragover", "dragleave"].forEach((eventName) => {
  dropZone.addEventListener(
    eventName,
    (e) => {
      e.preventDefault();
    },
    false
  );
});

dropZone.ondragover = (e) => {
  e.target.querySelector("h1").textContent = "Drop files to upload";
  dropZone.classList.add("highlight");
};

dropZone.ondragleave = (e) => {
  e.target.querySelector("h1").textContent = "Click to add pictures";
  dropZone.classList.remove("highlight");
};

dropZone.ondrop = (e) => {
  e.target.querySelector("h1").textContent = "Click to add pictures";
  dropZone.classList.remove("highlight");

  e.preventDefault();
  handleFiles(e.dataTransfer.files);
};

function displayCollage(url) {
  dropZone.innerHTML = `
      <img id="collage" src="${url}">
    `;
}

function clearZone() {
  dropZone.classList.add("full");
  dropZone.classList.remove("highlight");
  dropZone.onclick = null;
  dropZone.ondragover = null;
  dropZone.ondragleave = null;
  dropZone.ondrop = null;
}
