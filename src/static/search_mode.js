// Get radio buttons and areas
const searchText = document.getElementById('searchText');
const temporalSearch = document.getElementById('temporalSearch');
const textAndSketch = document.getElementById('textAndSketch');

const textSearchArea = document.getElementById('textSearchArea');
const temporalSearchArea = document.getElementById('temporalSearchArea');
const textAndSketchArea = document.getElementById('textAndSketchArea');

// Function to toggle visibility based on selection
function toggleSearchArea() {
    textSearchArea.style.display = 'none';
    temporalSearchArea.style.display = 'none';
    textAndSketchArea.style.display = 'none';

    if (searchText.checked) {
        textSearchArea.style.display = 'block';
    } else if (temporalSearch.checked) {
        temporalSearchArea.style.display = 'flex';
    } else if (textAndSketch.checked) {
        textAndSketchArea.style.display = 'flex';
    }

    // Save the selected radio button to localStorage
    localStorage.setItem('selectedSearchMode', document.querySelector('input[name="searchMode"]:checked').id);
}

// Function to restore the selected radio button from localStorage
function restoreSearchMode() {
    const savedMode = localStorage.getItem('selectedSearchMode');
    if (savedMode) {
        document.getElementById(savedMode).checked = true;
        toggleSearchArea(); // Update the UI based on the saved selection
    }
}

// Add event listeners to radio buttons
searchText.addEventListener('change', toggleSearchArea);
temporalSearch.addEventListener('change', toggleSearchArea);
textAndSketch.addEventListener('change', toggleSearchArea);

// Restore the previous selection on page load
document.addEventListener('DOMContentLoaded', restoreSearchMode);


function clearText() {
    document.getElementById("searchTextArea").value = "";
    document.getElementById("text_first_this_area").value = "";
    document.getElementById("text_then_that_area").value = "";
}

function sendSearchText() {
    // Get the text from the textarea
    const searchText = document.getElementById("searchTextArea").value;

    // Send the data to the backend using fetch API
    fetch('/search_by_text', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ searchText: searchText }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);  // Log the response for debugging

        // Display the result in the <p> tag with id "searchResult"
        document.getElementById("translated_text_for_search_by_text").innerText = data.translated_text;  // Update the <p> content with the processed result
    })
    .catch((error) => {
        console.error('Error:', error);  // Log any errors
        document.getElementById("translated_text_for_search_by_text").innerText = "An error occurred while translating the search.";  // Display error message
    });
}

