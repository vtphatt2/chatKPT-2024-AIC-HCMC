// Save the scroll position before leaving the page or navigating away
window.addEventListener('beforeunload', function () {
    localStorage.setItem('scrollPosition', window.scrollY);
});

// Restore the scroll position when the page is loaded
window.addEventListener('load', function () {
    restoreScrollPosition();
});

// Handle restoration after the DOM is fully loaded
document.addEventListener('DOMContentLoaded', function () {
    // restoreSearchMode();
    restoreSearchData();
    // restoreScrollPosition(); // Already called in 'load' event
});

// function restoreSearchMode() {
//     const savedMode = localStorage.getItem('selectedSearchMode');
//     console.log(`Restoring search mode: ${savedMode}`);
//     if (savedMode) {
//         const radioBtn = document.getElementById(savedMode);
//         if (radioBtn) {
//             radioBtn.checked = true;
//             toggleSearchArea();
//         } else {
//             console.warn(`Radio button with ID "${savedMode}" not found.`);
//             // Optionally, set a default mode
//             document.getElementById('searchText').checked = true;
//             toggleSearchArea();
//         }
//     } else {
//         // Default to 'searchText' if no mode is saved
//         document.getElementById('searchText').checked = true;
//         toggleSearchArea();
//     }
// }

function restoreSearchData() {
    const selectedMode = localStorage.getItem('selectedSearchMode');
    console.log(`Selected Mode for restoration: ${selectedMode}`);

    if (selectedMode === 'searchText') {
        const lastSearchJSON = localStorage.getItem('lastSearch');
        console.log(`Retrieved lastSearch: ${lastSearchJSON}`);
        if (lastSearchJSON) {
            const lastSearch = JSON.parse(lastSearchJSON);
            document.getElementById("translated_text_for_search_by_text").innerText = lastSearch.translated_text;
            document.getElementById('searchTextArea').value = lastSearch.searchText;

            // Restore search results
            restoreSearchResults(lastSearch.submission_list);
        }
    } else if (selectedMode === 'temporalSearch') {
        const lastTemporalSearchJSON = localStorage.getItem('lastTemporalSearch');
        console.log(`Retrieved lastTemporalSearch: ${lastTemporalSearchJSON}`);
        if (lastTemporalSearchJSON) {
            const lastTemporalSearch = JSON.parse(lastTemporalSearchJSON);
            document.getElementById("translated_text_for_temporal_search").innerText = 
                `Translated First This: ${lastTemporalSearch.translated_first_this}\n` +
                `Translated Then That: ${lastTemporalSearch.translated_then_that}`;
            document.getElementById('text_first_this_area').value = lastTemporalSearch.textFirstThis;
            document.getElementById('text_then_that_area').value = lastTemporalSearch.textThenThat;

            // Restore search results
            restoreSearchResults(lastTemporalSearch.submission_list);
        }
    }
    // Add similar blocks for other search modes like 'textAndSketch' if needed
}

function restoreSearchResults(submissionList) {
    const searchResultContainer = document.getElementById('search-result');
    searchResultContainer.innerHTML = ''; // Clear previous search result

    submissionList.forEach(([videoName, video_link, images, fps, transcript], groupIndex) => {
        const transcriptText = document.createElement('p');
        transcriptText.innerText = transcript;
        transcriptText.style.marginTop = '-5px';
        transcriptText.style.marginBottom = '-5px';
        transcriptText.style.fontSize = '12px';

        // Create a container for each video section
        const videoSection = document.createElement('div');
        videoSection.classList.add('video-section');

        // Create the video header (displayed on the left side)
        const videoHeader = document.createElement('div');
        videoHeader.classList.add('video-header');
        videoHeader.innerText = `Video: ${videoName}`;
        videoSection.appendChild(videoHeader);

        const videoLink = document.createElement('a');
        videoLink.href = `${video_link}&t=${Math.floor(images[0][1] / fps)}s`;  // Set the link to point to the video
        videoLink.innerText = "Watch full video";  // Text displayed for the link
        videoLink.target = "_blank";  // Open link in a new tab
        videoLink.style.textDecoration = "none";  // Remove underline
        videoLink.style.color = "blue";  // Set text color (you can change it to any color you prefer)
        videoLink.style.display = "block";  // Ensure the link appears beneath the video name
        videoHeader.appendChild(videoLink); 

        const discardButton = document.createElement('button');
        discardButton.innerText = "Discard";  // Nội dung của nút
        discardButton.style.marginTop = "10px";  // Thêm khoảng cách giữa link và nút
        discardButton.style.padding = "5px 10px";  // Tạo khoảng trống trong nút
        discardButton.style.border = "none";  // Loại bỏ viền nút (tuỳ chọn)
        discardButton.style.backgroundColor = "#ff4d4d";  // Màu nền đỏ
        discardButton.style.color = "white";  // Màu chữ trắng
        discardButton.style.cursor = "pointer";
        
        const discardedVideosElement = document.getElementById('discarded_videos');
        discardButton.addEventListener('click', () => {
            // Xóa video khỏi giao diện
            transcriptText.remove();  
            videoSection.remove();  
        
            // Thêm tên video vào danh sách các video bị loại bỏ
            let discardedVideos = discardedVideosElement.value.split(',').map(v => v.trim()).filter(Boolean); // Chuyển thành mảng và loại bỏ khoảng trắng
            if (!discardedVideos.includes(videoName)) {  // Kiểm tra nếu video chưa có trong danh sách
                discardedVideos.push(videoName);
                discardedVideosElement.value = discardedVideos.join(', ');  // Cập nhật giá trị với các tên video được phân cách bởi dấu phẩy
            }
        });
        videoHeader.appendChild(discardButton);

        // Create the scrollable container for images (displayed next to the header)
        const scrollContainer = document.createElement('div');
        scrollContainer.classList.add('scroll-container');

        // Loop through the images and add them to the scroll container
        images.forEach(([imagePath, frameId], index) => {
            const imageItem = document.createElement('div');
            imageItem.classList.add('image-item');

            const imgElement = document.createElement('img');
            const normalizedImagePath = imagePath.replace(/^[A-Za-z]:\\|^\//, '').replace(/\\/g, '/');
            imgElement.alt = `Frame ${frameId}`;
            imgElement.style.width = '300px';  // Set initial width
            imgElement.style.height = 'auto';   // Set initial height
            imgElement.onclick = function (event) {
                // Nếu đã có timer, không làm gì
                if (clickTimers.has(imgElement)) return;

                const timer = setTimeout(() => {
                    // Single-click action: toggle red border
                    if (imgElement.classList.contains('selected-image')) {
                        imgElement.classList.remove('selected-image');
                    } else {
                        imgElement.classList.add('selected-image');
                    }
                    clickTimers.delete(imgElement);
                }, 250); // Thời gian chờ để phân biệt single và double-click

                clickTimers.set(imgElement, timer);
            };

            // Double-click event for zooming the image
            imgElement.ondblclick = function () {
                // Nếu có timer đang chờ, hủy bỏ nó
                if (clickTimers.has(imgElement)) {
                    clearTimeout(clickTimers.get(imgElement));
                    clickTimers.delete(imgElement);
                }
                toggleZoom(imgElement);
            };

            // Right-click event for selecting only one image with a blue border
            imgElement.oncontextmenu = function (event) {
                event.preventDefault();
            
                // Bỏ chọn viền xanh từ tất cả các ảnh
                document.querySelectorAll('.selected-submit-image').forEach(img => {
                    img.classList.remove('selected-submit-image');
                });
            
                // Toggle viền xanh cho ảnh hiện tại
                if (imgElement.classList.contains('selected-submit-image')) {
                    imgElement.classList.remove('selected-submit-image');
                } else {
                    imgElement.classList.add('selected-submit-image');
                    // Tuỳ chọn: bỏ chọn viền đỏ nếu muốn
                    imgElement.classList.remove('selected-image');
                    
                    // Tự động điền video_name và frame_id
                    document.getElementById('video_name').value = videoName;  // videoName from the submission list
                    document.getElementById('frame_id').value = frameId;  // frameId of the image
                }
            };

            const caption = document.createElement('div');
            caption.classList.add('image-caption');
            caption.innerText = `Frame ID: ${frameId}`;

            imageItem.appendChild(imgElement);
            imageItem.appendChild(caption);
            scrollContainer.appendChild(imageItem);
        });

        videoSection.appendChild(scrollContainer);
        searchResultContainer.appendChild(transcriptText);
        searchResultContainer.appendChild(videoSection);
    });
}

function restoreScrollPosition() {
    const scrollPosition = localStorage.getItem('scrollPosition');
    if (scrollPosition) {
        window.scrollTo(0, parseInt(scrollPosition, 10));
    }
}

function clearSearchData() {
    localStorage.removeItem('lastSearch');
    localStorage.removeItem('lastTemporalSearch');
    const searchResultContainer = document.getElementById('search-result');
    searchResultContainer.innerHTML = '';
    const translatedTextElement1 = document.getElementById("translated_text_for_search_by_text");
    const translatedTextElement2 = document.getElementById("translated_text_for_temporal_search");
    if (translatedTextElement1) translatedTextElement1.innerText = "";
    if (translatedTextElement2) translatedTextElement2.innerText = "";
    const searchTextArea = document.getElementById('searchTextArea');
    const textFirstThisArea = document.getElementById('text_first_this_area');
    const textThenThatArea = document.getElementById('text_then_that_area');
    if (searchTextArea) searchTextArea.value = "";
    if (textFirstThisArea) textFirstThisArea.value = "";
    if (textThenThatArea) textThenThatArea.value = "";
}

// // Save the scroll position before leaving the page or navigating away
// window.addEventListener('beforeunload', function () {
//     localStorage.setItem('scrollPosition', window.scrollY);
// });

// // Restore the scroll position when the page is loaded
// window.addEventListener('load', function () {
//     const searchDataJSON = localStorage.getItem('lastSearch');
//     if (searchDataJSON) {
//         const searchData = JSON.parse(searchDataJSON);
//         const { searchText, translated_text, submission_list } = searchData;

//         // Cập nhật nội dung đã dịch
//         const translatedTextElement = document.getElementById("translated_text_for_search_by_text");
//         translatedTextElement.innerText = translated_text;

//         // Cập nhật textarea với searchText (nếu muốn)
//         const searchTextArea = document.getElementById('searchTextArea');
//         if (searchTextArea) {
//             searchTextArea.value = searchText;
//         }

//         // Hiển thị kết quả tìm kiếm
//         const searchResultContainer = document.getElementById('search-result');
//         searchResultContainer.innerHTML = ''; // Clear previous search result

//         submission_list.forEach(([videoName, images], groupIndex) => {
//             // Create a container for each video section
//             const videoSection = document.createElement('div');
//             videoSection.classList.add('video-section');

//             // Create the video header (displayed on the left side)
//             const videoHeader = document.createElement('div');
//             videoHeader.classList.add('video-header');
//             videoHeader.innerText = `Video: ${videoName}`;
//             videoSection.appendChild(videoHeader);

//             // Create the scrollable container for images (displayed next to the header)
//             const scrollContainer = document.createElement('div');
//             scrollContainer.classList.add('scroll-container');

//             // Loop through the images and add them to the scroll container
//             images.forEach(([imagePath, frameId], index) => {
//                 const imageItem = document.createElement('div');
//                 imageItem.classList.add('image-item');

//                 const imgElement = document.createElement('img');
//                 imgElement.src = `/image/${imagePath.substring(1)}`;  // Serve the image via the /image/<path>
//                 imgElement.alt = `Frame ${frameId}`;
//                 imgElement.style.width = '150px';  // Set initial width
//                 imgElement.style.height = 'auto';   // Set initial height
//                 imgElement.onclick = function () { toggleZoom(imgElement); };

//                 const caption = document.createElement('div');
//                 caption.classList.add('image-caption');
//                 caption.innerText = `Frame ID: ${frameId}`;

//                 imageItem.appendChild(imgElement);
//                 imageItem.appendChild(caption);
//                 scrollContainer.appendChild(imageItem);
//             });

//             videoSection.appendChild(scrollContainer);
//             searchResultContainer.appendChild(videoSection);
//         });
//     }
// });

// function clearSearchData() {
//     localStorage.removeItem('lastSearch');
//     const searchResultContainer = document.getElementById('search-result');
//     searchResultContainer.innerHTML = '';
//     const translatedTextElement = document.getElementById("translated_text_for_search_by_text");
//     translatedTextElement.innerText = "";
//     const searchTextArea = document.getElementById('searchTextArea');
//     if (searchTextArea) {
//         searchTextArea.value = "";
//     }
// }

// document.addEventListener('DOMContentLoaded', function () {
//     restoreSearchMode();
//     restoreSearchData();
//     restoreScrollPosition();
// });

// function restoreSearchMode() {
//     const savedMode = localStorage.getItem('selectedSearchMode');
//     if (savedMode) {
//         document.getElementById(savedMode).checked = true;
//         toggleSearchArea(); // Update the UI based on the saved selection
//     }
// }

// function restoreSearchData() {
//     const selectedMode = localStorage.getItem('selectedSearchMode');

//     if (selectedMode === 'searchText') {
//         const lastSearchJSON = localStorage.getItem('lastSearch');
//         if (lastSearchJSON) {
//             const lastSearch = JSON.parse(lastSearchJSON);
//             document.getElementById("translated_text_for_search_by_text").innerText = lastSearch.translated_text;
//             document.getElementById('searchTextArea').value = lastSearch.searchText;

//             // Restore search results
//             restoreSearchResults(lastSearch.submission_list);
//         }
//     } else if (selectedMode === 'temporalSearch') {
//         const lastTemporalSearchJSON = localStorage.getItem('lastTemporalSearch');
//         if (lastTemporalSearchJSON) {
//             const lastTemporalSearch = JSON.parse(lastTemporalSearchJSON);
//             document.getElementById("translated_text_for_temporal_search").innerText = 
//                 `Translated First This: ${lastTemporalSearch.translated_first_this}\n` +
//                 `Translated Then That: ${lastTemporalSearch.translated_then_that}`;
//             document.getElementById('text_first_this_area').value = lastTemporalSearch.textFirstThis;
//             document.getElementById('text_then_that_area').value = lastTemporalSearch.textThenThat;

//             // Restore search results
//             restoreSearchResults(lastTemporalSearch.submission_list);
//         }
//     }
//     // Add similar blocks for other search modes like 'textAndSketch' if needed
// }

// function restoreSearchResults(submissionList) {
//     const searchResultContainer = document.getElementById('search-result');
//     searchResultContainer.innerHTML = ''; // Clear previous search result

//     submissionList.forEach(([videoName, images], groupIndex) => {
//         // Create a container for each video section
//         const videoSection = document.createElement('div');
//         videoSection.classList.add('video-section');

//         // Create the video header (displayed on the left side)
//         const videoHeader = document.createElement('div');
//         videoHeader.classList.add('video-header');
//         videoHeader.innerText = `Video: ${videoName}`;
//         videoSection.appendChild(videoHeader);

//         // Create the scrollable container for images (displayed next to the header)
//         const scrollContainer = document.createElement('div');
//         scrollContainer.classList.add('scroll-container');

//         // Loop through the images and add them to the scroll container
//         images.forEach(([imagePath, frameId], index) => {
//             const imageItem = document.createElement('div');
//             imageItem.classList.add('image-item');

//             const imgElement = document.createElement('img');
//             imgElement.src = `/image/${imagePath.substring(1)}`;  // Serve the image via the /image/<path>
//             imgElement.alt = `Frame ${frameId}`;
//             imgElement.style.width = '150px';  // Set initial width
//             imgElement.style.height = 'auto';   // Set initial height
//             imgElement.onclick = function() { toggleZoom(imgElement); };

//             const caption = document.createElement('div');
//             caption.classList.add('image-caption');
//             caption.innerText = `Frame ID: ${frameId}`;

//             imageItem.appendChild(imgElement);
//             imageItem.appendChild(caption);
//             scrollContainer.appendChild(imageItem);
//         });

//         videoSection.appendChild(scrollContainer);
//         searchResultContainer.appendChild(videoSection);
//     });
// }

// function restoreScrollPosition() {
//     const scrollPosition = localStorage.getItem('scrollPosition');
//     if (scrollPosition) {
//         window.scrollTo(0, parseInt(scrollPosition, 10));
//     }
// }

// function clearSearchData() {
//     localStorage.removeItem('lastSearch');
//     localStorage.removeItem('lastTemporalSearch');
//     const searchResultContainer = document.getElementById('search-result');
//     searchResultContainer.innerHTML = '';
//     const translatedTextElement1 = document.getElementById("translated_text_for_search_by_text");
//     const translatedTextElement2 = document.getElementById("translated_text_for_temporal_search");
//     if (translatedTextElement1) translatedTextElement1.innerText = "";
//     if (translatedTextElement2) translatedTextElement2.innerText = "";
//     const searchTextArea = document.getElementById('searchTextArea');
//     const textFirstThisArea = document.getElementById('text_first_this_area');
//     const textThenThatArea = document.getElementById('text_then_that_area');
//     if (searchTextArea) searchTextArea.value = "";
//     if (textFirstThisArea) textFirstThisArea.value = "";
//     if (textThenThatArea) textThenThatArea.value = "";
// }