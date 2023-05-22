const dropArea1 = document.querySelector("#drag-area-1");
const dragText1 = document.querySelector(".header-1");
const button1 = document.querySelector(".browse_button-1");
const input1 = document.querySelector(".input-1");

const dropArea2 = document.querySelector("#drag-area-2");
const dragText2 = document.querySelector(".header-2");
const button2 = document.querySelector(".browse_button-2");
const input2 = document.querySelector(".input-2");

const cancel_icon = document.querySelector(".btn-cancel");

const button3 = document.querySelector("#browse_button-3");
const input3 = document.querySelector(".input-3");

const button1_copy = document.querySelector("#browse_button-1-1");
const button2_copy = document.querySelector("#browse_button-2-2");

const start_processing_button = document.getElementById('start-processing');

let file1; //DML file
let file2; //pdf file
let file3; //validation file


//1st step
button1.addEventListener("click", function (event) {
  event.preventDefault();
  input1.click();
});

input1.addEventListener("change", function (event) {
  event.preventDefault();
  console.log("input 1");
  file1 = this.files[0];
  dropArea1.classList.add("active");
  showFile1();
});

//If user Drag File Over DropArea
dropArea1.addEventListener("dragover", (event) => {
  event.preventDefault(); //preventing from default behaviour
  dropArea1.classList.add("active");
  dragText1.textContent = "Release to Upload File";
});

//If user leave dragged File from DropArea
dropArea1.addEventListener("dragleave", () => {
  dropArea1.classList.remove("active");
  dragText1.textContent = "Drag & Drop to Upload File";
});

//If user drop File on DropArea
dropArea1.addEventListener("drop", (event) => {
  event.preventDefault(); //preventing from default behaviour
  //getting user select file and [0] this means if user select multiple files then we'll select only the first one
  file1 = event.dataTransfer.files[0];
  showFile1(); //calling function
});

//2nd step
button2.addEventListener("click", function (event) {
  event.preventDefault();
  input2.click();
});

input2.addEventListener("change", function (event) {
  event.preventDefault();
  console.log("input 2");
  file2 = this.files[0];
  dropArea2.classList.add("active");
  showFile2();
});

dropArea2.addEventListener("dragover", (event) => {
  event.preventDefault(); //preventing from default behaviour
  dropArea2.classList.add("active");
  dragText2.textContent = "Release to Upload File";
});

//If user leave dragged File from DropArea
dropArea2.addEventListener("dragleave", () => {
  dropArea2.classList.remove("active");
  dragText2.textContent = "Drag & Drop to Upload File";
});

//If user drop File on DropArea
dropArea2.addEventListener("drop", (event) => {
  event.preventDefault(); //preventing from default behaviour
  //getting user select file and [0] this means if user select multiple files then we'll select only the first one
  file2 = event.dataTransfer.files[0];
  showFile2(); //calling function
});


function fileSize(bytes) {
  const units = ["B", "KB", "MB", "GB", "TB"];
  let size = bytes;
  let unitIndex = 0;

  while (size >= 1024) {
    size /= 1024;
    unitIndex++;
  }

  const formattedSize = size.toFixed(2) + " " + units[unitIndex];
  return formattedSize;
}

function saveFile1() {
  if (file1){
      const formData = new FormData();
    formData.append('file', file1)
    console.log("Inside the pythonSend function")
    try{
      fetch('/DML_file', {
        method: 'POST', // *GET, POST, PUT, DELETE, etc.
        body: formData, // body data type must match "Content-Type" header
      });
    } catch (error) {
      console.error(error);
    }
  }
}

function saveFile2() {
  if(file2){
    const formData = new FormData();
    formData.append('file', file2)
    try{
      fetch('/NON_DML_file', {
        method: 'POST', // *GET, POST, PUT, DELETE, etc.
        body: formData, // body data type must match "Content-Type" header
      });
    } catch (error) {
      console.error(error);
    }
  }
}

function downloadDML(button) {
  const formData = new FormData();

  // Get the name of the file from the table row
  var text = button.parentNode.parentNode.cells[1].textContent;
  var fileName = text.split(' ')[0];
  console.log(fileName);

  // Construct the URL for the file download
  var url = "/download_DML/" + encodeURIComponent(fileName);

  // Navigate to the file download URL
  window.location.href = url;
}

function downloadNONDML(button){
  const formData = new FormData();

  // Get the name of the file from the table row
  var text = button.parentNode.parentNode.cells[1].textContent;
  var fileName = text.split('.pdf')[0];
  console.log(fileName);

  // Construct the URL for the file download
  var url = "/download_NONDML/" + encodeURIComponent(fileName+'.pdf');

  // Navigate to the file download URL
  window.location.href = url;
}

//display File 1
function showFile1() {
  const date = new Date();
  const dateString = `${date.getMonth() + 1}/${date.getDate()}/${date.getFullYear()}<br>${date.getHours()}:${date.getMinutes()}:${date.getSeconds()}`;
  let validExtensions_file1 = ["text/csv", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"];
  if (validExtensions_file1.includes(file1.type)) {
    let fileReader = new FileReader(); //creating new FileReader object
    fileReader.onload = () => {
      let fileDiv = `<div class="btn-cancel" >
                            <a href="reroute" class="btn_cancel_upload"><i class="fa fa-times-circle" aria-hidden="true"></i></a>
                          </div>
                          <div class="icon-text">
                            <div class="icon">
                              <i class="fas fa-file-excel"></i>
                            </div>
                            <div>${file1.name}</br>${fileSize(file1.size)}
                            </div>
                          </div>`;
      dropArea1.innerHTML = fileDiv;
      document.getElementById("file1-name").innerHTML = `${file1.name} </br> ${fileSize(file1.size)}`;
      document.getElementById("date1").innerHTML = dateString;
    }
    fileReader.readAsDataURL(file1);
  } else {
    alert("This is not an DML File!");
    dropArea1.classList.remove("active");
    dragText1.textContent = "Drag & Drop to Upload File";
  }
}

//display File 2 
function showFile2() {
  const date = new Date();
  const dateString = `${date.getMonth() + 1}/${date.getDate()}/${date.getFullYear()}<br>${date.getHours()}:${date.getMinutes()}:${date.getSeconds()}`;
  let validExtensions_file2 = ["application/pdf"];
  if (validExtensions_file2.includes(file2.type)) {
    let fileReader = new FileReader(); //creating new FileReader object
    fileReader.onload = () => {
      let fileDiv = `<div class="btn-cancel" >
                            <a href="reroute" class="btn_cancel_upload"><i class="fa fa-times-circle" aria-hidden="true"></i></a>
                          </div>
                          <div class="icon-text">
                            <div class="icon">
                              <i class="fas fa-file-excel"></i>
                            </div>
                            <div>${file2.name}</br>${fileSize(file2.size)}
                            </div>
                          </div>`;
      dropArea2.innerHTML = fileDiv;
      document.getElementById("file2-name").innerHTML = `${file2.name} </br> ${fileSize(file2.size)}`;
      document.getElementById("date2").innerHTML = dateString;
    }
    fileReader.readAsDataURL(file2);
  } else {
    alert("This is not an PDF File!");
    dropArea2.classList.remove("active");
    dragText2.textContent = "Drag & Drop to Upload File";
  }
}

// button3.addEventListener("click", function (event) {
//   event.preventDefault();
//   input3.click();
// });

// input3.addEventListener("change", function (event) {
//   event.preventDefault();
//   file3 = this.files[0];
//   Replacefile(file3);
// });

button1_copy.addEventListener("click", function (event) {
  event.preventDefault();
  input1.click();
});

button2_copy.addEventListener("click", function (event) {
  event.preventDefault();
  input2.click();
});

// //THIRD VALIDATEION FILE
// const file3_original = new File([], "Callsign vs Aircraft type.xlsx");
// const reader = new FileReader();
// reader.onloadend = function () {
//   const lastModifiedDate = new Date(file3_original.lastModified);
//   const fileDate = `${lastModifiedDate.getMonth() + 1}/${lastModifiedDate.getDate()}/${lastModifiedDate.getFullYear()}<br>${lastModifiedDate.getHours()}:${lastModifiedDate.getMinutes()}:${lastModifiedDate.getSeconds()}`;
//   const fileSizeFormatted = fileSize(file3_original.size);
//   // document.getElementById('file3-name').innerHTML = `${file3_original.name} <br> ${fileSizeFormatted}`;
//   document.getElementById('date3').innerHTML = fileDate;
// }
// reader.readAsDataURL(file3_original);

// function Replacefile(file3) {
//   const reader = new FileReader();
//   reader.onloadend = function () {
//     const lastModifiedDate = new Date(file3.lastModified);
//     const fileDate = `${lastModifiedDate.getMonth() + 1}/${lastModifiedDate.getDate()}/${lastModifiedDate.getFullYear()}<br>${lastModifiedDate.getHours()}:${lastModifiedDate.getMinutes()}:${lastModifiedDate.getSeconds()}`;
//     const fileSizeFormatted = fileSize(file3.size);
//     document.getElementById('file3-name').innerHTML = `${file3.name} <br> ${fileSizeFormatted}`;
//     document.getElementById('date3').innerHTML = fileDate;
//   }
//   reader.readAsDataURL(file3);
// }

//Navigation part
const navigateToFormStep = (stepNumber) => {

  /* Hide all form steps.*/
  document.querySelectorAll(".form-step").forEach((formStepElement) => {
    formStepElement.classList.add("d-none");
  });

  /* Mark all form steps as unfinished.*/
  document.querySelectorAll(".form-stepper-list").forEach((formStepHeader) => {
    formStepHeader.classList.add("form-stepper-unfinished");
    formStepHeader.classList.remove("form-stepper-active", "form-stepper-completed");
  });

  /* Show the current form step (as passed to the function).*/
  document.querySelector("#step-" + stepNumber).classList.remove("d-none");

  /* Select the form step circle (progress bar).*/
  const formStepCircle = document.querySelector('li[step="' + stepNumber + '"]');

  /* Mark the current form step as active.*/
  formStepCircle.classList.remove("form-stepper-unfinished", "form-stepper-completed");
  formStepCircle.classList.add("form-stepper-active");

  // Loop through each form step circles.

  for (let index = 0; index < stepNumber; index++) {

    const formStepCircle = document.querySelector('li[step="' + index + '"]');
    if (formStepCircle) {
      formStepCircle.classList.remove("form-stepper-unfinished", "form-stepper-active");
      formStepCircle.classList.add("form-stepper-completed");
    }
  }
};

document.querySelectorAll(".btn-navigate-form-step").forEach((formNavigationBtn) => {
  formNavigationBtn.addEventListener("click", () => {
    const stepNumber = parseInt(formNavigationBtn.getAttribute("step_number"));
    navigateToFormStep(stepNumber);
  });
});

function validateFiles(event){

  if(!file1 || !file2)
  {
    alert('No files were uploaded. Please upload both files before proceeding.');
    event.preventDefault();
    location.reload();
  }
};

start_processing_button.addEventListener('click', function (event) {
  // Validate files before redirecting
  validateFiles(event);
});

