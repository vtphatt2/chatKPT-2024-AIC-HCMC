function findSimilarImages() {
    const searchBtn = document.getElementById("findSimilarBtn"); // Đảm bảo ID đúng với nút Search của bạn
    const discardedVideos = document.getElementById('discarded_videos').value;
    const selectedImages = document.querySelectorAll('.selected-image');
    const k = document.getElementById('k_for_search_similar_images').value;
    let value;
    if (k == '') {
        value = 100
    }
    else {
        value = parseInt(k, 10);
    }

    // Vô hiệu hóa nút Search
    // searchBtn.disabled = true;
    // searchBtn.style.cursor = "not-allowed";
    // searchBtn.style.opacity = "0.6"; // Thay đổi độ mờ để thể hiện nút đã bị vô hiệu hóa

    const selectedImagesList = [];

    selectedImages.forEach(img => {
        const video = img.src;  // Assuming video info is stored in 'data-video'
        const frameId = img.alt.replace('Frame ', ''); // Extract frameId from the 'alt' attribute
        
        // Add video and frameId info to the submission list
        selectedImagesList.push({
            video_name: video,
            frame_id: frameId
        });
    });

    fetch('/find_similar_images', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            selectedImagesList: selectedImagesList,
            k: value
        })
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
        // translatedTextElement.innerText = data.translated_text; 
        // if (loadingSpinner) {
        //     loadingSpinner.style.display = "none"; // Ẩn spinner
        // }

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
                imgElement.onclick = function() { 
                    toggleZoom(imgElement); 
                };
                imgElement.ondblclick = function() {                
                    if (imgElement.classList.contains('selected-image')) {
                        // Nếu đã được chọn, thì bỏ chọn (xóa viền đỏ)
                        imgElement.classList.remove('selected-image');
                        imgElement.style.border = 'none';  // Xóa viền đỏ khi ảnh bị bỏ chọn
                    } else {
                        // Nếu chưa được chọn, thì chọn ảnh (thêm viền đỏ)
                        imgElement.classList.add('selected-image');
                        imgElement.style.border = '2px solid red';  // Thêm viền đỏ khi ảnh được chọn
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
        translatedTextElement.innerText = "An error occurred while translating the text."; 
        if (loadingSpinner) {
            loadingSpinner.style.display = "none"; 
        }

        searchBtn.disabled = false;
        searchBtn.style.cursor = "pointer";
        searchBtn.style.opacity = "1"; 
    });
}