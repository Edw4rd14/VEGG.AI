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
const randomImageBtn = document.getElementById('random-image-button');

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
// GET RANDOM IMAGE AND SET
const setRandomImage = () => {
    $.ajax({
        url: '/random-prediction-image',
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            sessionStorage.setItem('fileName', data.filename);
            base64ImageData = `data:image/jpeg;base64,${data.base64_image}`;
            imgView.style.backgroundImage = `url(data:image/jpeg;base64,${data.base64_image})`;
            imgView.textContent = '';
            imgView.style.backgroundColor = 'white';
            fileName.textContent = `FILE NAME: ${data.filename}`;
            result.style.display = 'none';
        },
        error: function (error) {
            console.error('Error fetching random image:', error);
        }
    });
}
// EVENT LISTENERS 
dropArea.addEventListener('dragover', preventDefaults);
dropArea.addEventListener('drop', handleDrop);
imageFile.addEventListener('change', () => handleFile(imageFile.files[0]));
randomImageBtn.addEventListener('click', setRandomImage);


// ======================
// PAGE REFRESH REDIRECTS
// ======================

// FUNCTION TO MAKE SUBMIT BUTTON SCROLL TO FORM UPON REFRESH
const rememberRedirectTarget = (target) => {
    // Store the ID of the form which I want the website to redirect to upon refresh
    sessionStorage.setItem('redirectTarget', target);
}
// REDIRECT
window.onload = () => {
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
const handleCheckboxChange = () => {
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
            'image_size': image_size,
            'file_name': sessionStorage.getItem('fileName')
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

// SEARCH TABLE
document.getElementById("search-input").addEventListener("keyup", () => {
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById("search-input");
    filter = input.value.toUpperCase();
    table = document.getElementById("history-table");
    tr = table.getElementsByTagName("tr");
    for (i = 1; i < tr.length; i++) {
        var displayRow = false; 
        td = tr[i].getElementsByTagName("td");
        for (j = 0; j < td.length; j++) {
            txtValue = td[j].textContent || td[j].innerText;
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                displayRow = true;
                break; 
            }
        }
        if (displayRow) {
            tr[i].style.display = "";
        } else {
            tr[i].style.display = "none";
        }
    }
});

// SORT COLUMNS (ID AND TIMESTAMP) [REFFERRED TO https://www.youtube.com/watch?v=8SL_hM1a0yo]
const sortTableByColumn = (table, column, asc = true) => {
    const dirModifier = asc ? 1: -1;
    const tBody = table.tBodies[0];
    const rows = Array.from(tBody.querySelectorAll('tr'));
    // Sort each row
    const sortedRows = rows.sort((a,b)=>{
        const aColText = a.querySelector(`td:nth-child(${column+1})`).textContent.trim();
        const bColText = b.querySelector(`td:nth-child(${column+1})`).textContent.trim();
        return aColText > bColText ? (1 * dirModifier) : (-1 * dirModifier)
    })
    // Remove all existing TR from the table
    while (tBody.firstChild) {
        tBody.removeChild(tBody.firstChild);
    }
    // Re-add sorted rows
    tBody.append(...sortedRows);
    // Remember how current column was sorted
    table.querySelectorAll('th').forEach(th=> th.classList.remove('th-sort-asc', 'th-sort-desc'));
    table.querySelector(`th:nth-child(${column+1})`).classList.toggle("th-sort-asc", asc);
    table.querySelector(`th:nth-child(${column+1})`).classList.toggle("th-sort-desc", !asc);
}
document.querySelectorAll('.table-sortable th').forEach(headerCell => {
    headerCell.addEventListener('click', ()=> {
        const tableElement = headerCell.parentElement.parentElement.parentElement;
        const headerIndex = Array.prototype.indexOf.call(headerCell.parentElement.children, headerCell);
        if (headerIndex === 0 || headerIndex === 5) {
            const currentIsAscending = headerCell.classList.contains("th-sort-asc");
            sortTableByColumn(tableElement, headerIndex, !currentIsAscending);
        }
    })
});

// FILTER TABLE
const filterTable = () => {
    // Get elements required
    var selects = document.getElementsByTagName("select");
    var table = document.getElementById("history-table");
    var rows = table.getElementsByTagName("tr");
    // Loop through all table rows, starting from the second row (skipping the header row)
    for (var i = 1; i < rows.length; i++) {
        var row = rows[i];
        var cells = row.getElementsByTagName("td");
        var shouldDisplay = true;
        // Loop through all select elements and apply filtering
        for (var j = 0; j < selects.length; j++) {
            var filter = selects[j].value.toUpperCase();
            var columnIndex = selects[j].getAttribute("data-column");
            // If the select element has a valid column index
            if (columnIndex !== null) {
                var cell = cells[columnIndex];
                // If the cell exists and its text content does not match the filter
                if (cell && cell.textContent.toUpperCase().indexOf(filter) === -1 && filter !== "") {
                    shouldDisplay = false;
                    break; // No need to check further, move to the next row
                }
            }
        }
        // Display or hide the row based on the filter results
        if (shouldDisplay) {
            row.style.display = "";
        } else {
            row.style.display = "none";
        }
    }
};