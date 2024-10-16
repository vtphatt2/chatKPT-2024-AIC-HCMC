
function performTASKformerSearch() {
    const textSearch = document.getElementById('text_task_former').value;
    const sketchCanvas = document.getElementById('drawingCanvas');
    const sketch = sketchCanvas.toDataURL('image/png');
    const translatedText = document.getElementById("translated_text_TASKformer");
    const discardedVideos = document.getElementById('discarded_videos').value;
    const keywords = document.getElementById('keywords').value;
    const k = document.getElementById('k').value;
    const searchBtn = document.getElementById("searchBtn3"); 
    let value;
    if (k !== '' && !isNaN(k)) {
        value = parseInt(k, 10);
    } 
    else if (keywords !== '') {
        value = 500;
    }
    else {
        value = 100;
    }

    searchBtn.disabled = true;
    searchBtn.style.cursor = "not-allowed";
    searchBtn.style.opacity = "0.6"; 

    // Show loading state if needed
    translatedText.innerText = "Processing search by text and sketch...";

    fetch('/search_text_and_sketch', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
            textSearch: textSearch,
            sketch: sketch,
            translatedText: translatedText,
            discardedVideos: discardedVideos,
            keywords: keywords,
            k: value
        })
    })
    .then(response => response.json())
    .then(data => {
        // Update translated text
        translatedText.innerText = `Translated: ${data.translated_text}`;

        // Display search results (similar to searchByText)
        const searchResultContainer = document.getElementById('search-result');
        searchResultContainer.innerHTML = ''; // Clear previous results

        const submissionList = data.submission_list;

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

            // Create the scrollable container for images (displayed next to the header)
            const scrollContainer = document.createElement('div');
            scrollContainer.classList.add('scroll-container');

            // Loop through the images and add them to the scroll container
            images.forEach(([imagePath, frameId], index) => {
                const imageItem = document.createElement('div');
                imageItem.classList.add('image-item');

                const imgElement = document.createElement('img');
                const normalizedImagePath = imagePath.replace(/^[A-Za-z]:\\|^\//, '').replace(/\\/g, '/');
                imgElement.src = `/image/${normalizedImagePath}`; 
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

        searchBtn.disabled = false;
        searchBtn.style.cursor = "pointer";
        searchBtn.style.opacity = "1";

        // Save temporal search data to localStorage
        const temporalSearchData = {
            textFirstThis: textFirstThis,
            textThenThat: textThenThat,
            translated_first_this: data.translated_first_this,
            translated_then_that: data.translated_then_that,
            submission_list: submissionList
        };
        localStorage.setItem('lastTemporalSearch', JSON.stringify(temporalSearchData));
    })
    .catch(error => {
        console.error('Error:', error);
        translatedFirstThisElement.innerText = "An error occurred during temporal search.";

        searchBtn.disabled = false;
        searchBtn.style.cursor = "pointer";
        searchBtn.style.opacity = "1";
    });
}

// Attach this function to the temporal search button
document.getElementById('searchBtn2').addEventListener('click', performTemporalSearch);
