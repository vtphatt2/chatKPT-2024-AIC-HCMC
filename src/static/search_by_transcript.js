
function searchByTranscript() {
    const keywords = document.getElementById('keywords').value;
    const k = document.getElementById('k').value;
    const searchBtn = document.getElementById("searchBtn4"); 
    let value;
    if (k !== '' && !isNaN(k)) {
        value = parseInt(k, 10);
    } 
    else {
        value = 100;
    }

    searchBtn.disabled = true;
    searchBtn.style.cursor = "not-allowed";
    searchBtn.style.opacity = "0.6"; 

    fetch('/search_by_transcript', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
            keywords: keywords,
            k: value
        })
    })
    .then(response => response.json())
    .then(data => {
        const searchResultContainer = document.getElementById('search-result');
        searchResultContainer.innerHTML = ''; // Clear previous results

        const submissionList = data.submission_list;

        submissionList.forEach(([videoName, video_link, images, fps, transcript], groupIndex) => {
            const transcriptText = document.createElement('p');
            transcriptText.innerHTML = transcript;
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

        searchBtn.disabled = false;
        searchBtn.style.cursor = "pointer";
        searchBtn.style.opacity = "1";

    })
    .catch(error => {
        console.error('Error:', error);
        translatedFirstThisElement.innerText = "An error occurred during temporal search.";

        searchBtn.disabled = false;
        searchBtn.style.cursor = "pointer";
        searchBtn.style.opacity = "1";
    });
}