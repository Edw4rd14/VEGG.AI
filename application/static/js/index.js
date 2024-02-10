/*
==================================================
ST1516 DEVOPS AND AUTOMATION FOR AI CA2 ASSIGNMENT 
NAME: EDWARD TAN YUAN CHONG
CLASS: DAAA/FT/2B/04
ADM NO: 2214407
==================================================
FILENAME: index.js
==================================================
*/

// ===================
// CLASSIFIER REDIRECT
// ===================

document.getElementById('tc-button').addEventListener('click', () => {
    const element = document.getElementById('classifier-title');
    const headerOffset = 100;
    const elementPosition = element.getBoundingClientRect().top + window.scrollY;
    const offsetPosition = elementPosition - headerOffset;
    window.scrollTo({
        top: offsetPosition,
        behavior: 'smooth'
    });
});

// ============
// IMAGE UPLOAD
// ============

// CONSTANTS
const dropArea = document.getElementById('drop-area');
const imageFile = document.getElementById('image-file');
const imgView = document.getElementById('img-view');
const originalImgView = imgView.innerHTML;
const fileName = document.getElementById('file-name');
const predict_button = document.getElementById('predict');
var result = document.getElementById('result');
const clear_button = document.getElementById('clear-form');

// HANDLE FILE
let base64ImageData;
const handleFile = (file) => {
    const reader = new FileReader();
    reader.onloadend = (e) => {
        if (file.type !== 'image/jpeg' && file.type !== 'image/png') {
            result.textContent = `INVALID FILE TYPE. PLEASE TRY AGAIN.`;
            result.style.border = '2px solid red';
            result.style.backgroundColor = '#ee6666';
            result.style.display = 'block';
            return;
        }
        const imgLink = e.target.result;
        imgView.style.backgroundImage = `url(${imgLink})`;
        imgView.textContent = '';
        imgView.style.backgroundColor = 'white';
        fileName.textContent = `FILE NAME: ${file.name}`;
        base64ImageData = imgLink;
        result.style.display = 'none';
        sessionStorage.setItem('fileName',file.name)
    };
    reader.readAsDataURL(file);
};
// PREVENT DEFAULT ACTIONS
const preventDefaults = (e) => {
    e.preventDefault();
    e.stopPropagation();
};
// HANDLE DRAG AND DROPS
const handleDrop = (e) => {
    preventDefaults(e);
    const files = e.dataTransfer.files || e.target.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
};
// EVENT LISTENERS 
dropArea.addEventListener('dragover', preventDefaults);
dropArea.addEventListener('drop', handleDrop);
imageFile.addEventListener('change', () => handleFile(imageFile.files[0]));

// ======================
// PAGE REFRESH REDIRECTS
// ======================

// FUNCTION TO MAKE SUBMIT BUTTON SCROLL TO FORM UPON REFRESH
function rememberRedirectTarget(target) {
    // Store the ID of the form which I want the website to redirect to upon refresh
    sessionStorage.setItem('redirectTarget', target);
}
// REDIRECT
window.onload = function() {
    // REDIRECT ID ELEMENT
    const redirectTarget = sessionStorage.getItem('redirectTarget');
    // IF REDIRECT TARGET EXISTS
    if (redirectTarget) {
        // TARGET ELEMENT
        const targetElement = document.getElementById(redirectTarget);
        // IF TARGET ELEMENT EXISTS
        if (targetElement) {
            // SCROLL TO VIEW
            targetElement.scrollIntoView();
            window.scrollBy(0, -100);
            // RESET REDIRECT ID
            sessionStorage.removeItem('redirectTarget');
        }
    }
};

// ===================
// IMAGE SIZE CHECKBOX
// ===================

// GET SELECTED IMAGE SIZE
var image_size = 128 // DEFAULT
// CHECKBOX ELEMENT
var checkbox = document.getElementById('img-size-checkbox');
// CHECK STORED CHECKBOX STATE
var storedState = sessionStorage.getItem('checkboxState');
// SET INITIAL STATE
var isChecked = storedState == 'true';
checkbox.checked = isChecked;
// HANDLE CHECKBOX CHANGE
function handleCheckboxChange() {
    // CHECK CURRENT STATE
    isChecked = checkbox.checked;
    if (isChecked) {
        image_size = 31;
    } else {
        image_size = 128;
    }
    // SAVE STATE TO SESSIONSTORAGE
    sessionStorage.setItem('checkboxState', isChecked);
}
// ADD EVENT LISTENER TO HANDLE CHECKBOX CHANGE
checkbox.addEventListener('change', handleCheckboxChange);
// SET INITIAL STATE
handleCheckboxChange();

// ==========
// PREDICTION
// ==========
// WHEN PREDICT BUTTON IS PRESSED
predict_button.addEventListener('click',(e)=>{
    result.textContent = `PREDICTING...`;
    result.style.border = 'none';
    result.style.backgroundColor = 'transparent';
    result.style.display = 'block';
    $.ajax({
        type: 'POST',
        url: `/predict`,
        data: JSON.stringify({
            'image':base64ImageData, 
            'image_size': image_size.toString(),
            'file_name': sessionStorage.getItem('fileName').toString()
        }
        ),
        contentType: 'application/json',
        success: (response)=>{
            result.textContent = `Prediction Result: ${response}`;
            result.style.border = '2px solid #034607';
            result.style.backgroundColor = '#67a97e';
        },
        error: (error)=>{
            result.textContent = `${error.responseJSON.error_message}`;
            result.style.border = '2px solid red';
            result.style.backgroundColor = '#ee6666';
        }
    });
    e.preventDefault();
});
// CLEAR FORM
clear_button.addEventListener('click',(e)=>{
    e.preventDefault();
    result.style.display='none';
    fileName.textContent = '';
    imgView.innerHTML = originalImgView;
    imgView.style.backgroundImage = ``;
    imgView.style.backgroundColor = '#c7ebc3';
    sessionStorage.removeItem('fileName')
})

// =============
// HISTORY TABLE
// =============

document.getElementById("search-input").addEventListener("keyup", function() {
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById("search-input");
    filter = input.value.toUpperCase();
    table = document.getElementById("history-table");
    tr = table.getElementsByTagName("tr");

    for (i = 1; i < tr.length; i++) {
        var displayRow = false; // Flag to determine if the row should be displayed
        td = tr[i].getElementsByTagName("td");

        // Loop through all td elements in the current row
        for (j = 0; j < td.length; j++) {
            txtValue = td[j].textContent || td[j].innerText;
            // Check if the text in the current td element contains the search filter
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                displayRow = true; // Set the flag to true if any td element matches
                break; // Exit the loop once a match is found in any column
            }
        }

        // Display or hide the row based on the displayRow flag
        if (displayRow) {
            tr[i].style.display = "";
        } else {
            tr[i].style.display = "none";
        }
    }
});