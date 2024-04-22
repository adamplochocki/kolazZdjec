let images = [];
let collageType = "horizontal";
let borderSize = 0;

document.querySelector("#horizontal").onclick = (e) => {
  clearRadios();
  e.target.checked = true;
};
document.querySelector("#vertical").onclick = (e) => {
  clearRadios();
  e.target.checked = true;
};

document.querySelector("#box").onclick = (e) => {
  clearRadios();
  e.target.checked = true;
};

const clearRadios = () => {
  Array.from(document.querySelectorAll("[type=radio]")).forEach((radio) => {
    radio.checked = false;
  });
};

document.querySelector("#border").oninput = (e) => {
  const value = e.target.value;

  if (value.length > 3 || value.length == 0) return;
  else if (/[0-9]*/.exec(e.target.value)[0].length != e.target.value.length) {
    e.target.value = borderSize.toString();
  } else {
    borderSize = parseInt(value);
  }
};

function handleFiles(files) {
  for (const file of files) {
    const fileReader = new FileReader();

    fileReader.onload = function (event) {
      const base64 = event.target.result;

      const img = {
        data: file,
        url: base64,
      };

      makePicture(base64, file.name);
      images.push(img);
    };

    fileReader.readAsDataURL(file);
  }
}

function makePicture(url, name) {
  const imgElement = document.createElement("div");

  imgElement.className = "picture";

  imgElement.innerHTML = `
  <img src="${url}">
  <p>${name}</p>
  <span title="Click to remove">+</span>
  `;

  imgElement.querySelector("span").onclick = (e) => {
    images = images.filter((v, i) => {
      if (v.data.name != name) {
        return v;
      }
    });

    e.target.parentElement.remove();
  };

  document.querySelector("#pictures #upload-area")
    ? document.querySelector("#pictures #upload-area").remove()
    : null;

  document.querySelector("#pictures").appendChild(imgElement);
}

async function process() {
  let fd = new FormData();

  for (let i = 0; i < images.length; i++) {
    fd.append("file" + i + 1, images[i].data);
  }

  fd.append("border", borderSize);
  fd.append("color", document.querySelector("#color").value);

  collageType = document.querySelector("input:checked").id;

  const resp = await fetch(`/collage/${collageType}`, {
    method: "POST",
    body: fd,
  });

  const blob = await resp.blob();

  return URL.createObjectURL(blob);
}
