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

function searchByText() {
    const searchText = document.getElementById('searchTextArea').value;
    const translatedTextElement = document.getElementById("translated_text_for_search_by_text");
    const loadingSpinner = document.getElementById("loadingSpinner");
    const searchBtn = document.getElementById("searchBtn1"); // Đảm bảo ID đúng với nút Search của bạn

    // Vô hiệu hóa nút Search
    searchBtn.disabled = true;
    searchBtn.style.cursor = "not-allowed";
    searchBtn.style.opacity = "0.6"; // Thay đổi độ mờ để thể hiện nút đã bị vô hiệu hóa

    // Hiển thị thông báo "Đang xử lý..." và spinner
    translatedTextElement.innerText = "Đợi chị xíu nhe mấy cưng...";
    if (loadingSpinner) {
        loadingSpinner.style.display = "inline-block"; // Hiển thị spinner nếu có
    }

    fetch('/search_by_text', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ searchText: searchText })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log('Success:', data);  // Log the response for debugging

        // Cập nhật phần tử với văn bản đã dịch
        translatedTextElement.innerText = data.translated_text; 
        if (loadingSpinner) {
            loadingSpinner.style.display = "none"; // Ẩn spinner
        }

        const searchResultContainer = document.getElementById('search-result');
        searchResultContainer.innerHTML = ''; // Clear previous search result

        // Get the submission_list from the response
        const submissionList = data.submission_list;

        // Lưu trữ dữ liệu tìm kiếm vào localStorage
        const searchData = {
            searchText: searchText,
            translated_text: data.translated_text,
            submission_list: submissionList
        };
        localStorage.setItem('lastSearch', JSON.stringify(searchData));

        // Loop through each [videoName, images] pair and dynamically create the scrollable image list
        submissionList.forEach(([videoName, images], groupIndex) => {
            // Create a container for each video section
            const videoSection = document.createElement('div');
            videoSection.classList.add('video-section');

            // Create the video header (displayed on the left side)
            const videoHeader = document.createElement('div');
            videoHeader.classList.add('video-header');
            videoHeader.innerText = `Video: ${videoName}`;
            videoSection.appendChild(videoHeader);

            // Create the scrollable container for images (displayed next to the header)
            const scrollContainer = document.createElement('div');
            scrollContainer.classList.add('scroll-container');

            // Loop through the images and add them to the scroll container
            images.forEach(([imagePath, frameId], index) => {
                const imageItem = document.createElement('div');
                imageItem.classList.add('image-item');

                const imgElement = document.createElement('img');
                imgElement.src = `/image/${imagePath.substring(1)}`;  // Serve the image via the /image/<path>
                imgElement.alt = `Frame ${frameId}`;
                imgElement.style.width = '150px';  // Set initial width
                imgElement.style.height = 'auto';   // Set initial height
                imgElement.onclick = function() { toggleZoom(imgElement); };

                const caption = document.createElement('div');
                caption.classList.add('image-caption');
                caption.innerText = `Frame ID: ${frameId}`;

                imageItem.appendChild(imgElement);
                imageItem.appendChild(caption);
                scrollContainer.appendChild(imageItem);
            });

            videoSection.appendChild(scrollContainer);
            searchResultContainer.appendChild(videoSection);
        });


        searchBtn.disabled = false;
        searchBtn.style.cursor = "pointer";
        searchBtn.style.opacity = "1"; 
    })
    .catch(error => {
        console.error('Error:', error);
        translatedTextElement.innerText = "Đã xảy ra lỗi trong quá trình dịch tìm kiếm."; 
        if (loadingSpinner) {
            loadingSpinner.style.display = "none"; 
        }

        searchBtn.disabled = false;
        searchBtn.style.cursor = "pointer";
        searchBtn.style.opacity = "1"; 
    });
}



