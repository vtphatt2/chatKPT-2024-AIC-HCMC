// Save the scroll position before leaving the page or navigating away
window.addEventListener('beforeunload', function () {
    localStorage.setItem('scrollPosition', window.scrollY);
});

// Restore the scroll position when the page is loaded
window.addEventListener('load', function () {
    const searchDataJSON = localStorage.getItem('lastSearch');
    if (searchDataJSON) {
        const searchData = JSON.parse(searchDataJSON);
        const { searchText, translated_text, submission_list } = searchData;

        // Cập nhật nội dung đã dịch
        const translatedTextElement = document.getElementById("translated_text_for_search_by_text");
        translatedTextElement.innerText = translated_text;

        // Cập nhật textarea với searchText (nếu muốn)
        const searchTextArea = document.getElementById('searchTextArea');
        if (searchTextArea) {
            searchTextArea.value = searchText;
        }

        // Hiển thị kết quả tìm kiếm
        const searchResultContainer = document.getElementById('search-result');
        searchResultContainer.innerHTML = ''; // Clear previous search result

        submission_list.forEach(([videoName, images], groupIndex) => {
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
                imgElement.onclick = function () { toggleZoom(imgElement); };

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
    }
});

function clearSearchData() {
    localStorage.removeItem('lastSearch');
    const searchResultContainer = document.getElementById('search-result');
    searchResultContainer.innerHTML = '';
    const translatedTextElement = document.getElementById("translated_text_for_search_by_text");
    translatedTextElement.innerText = "";
    const searchTextArea = document.getElementById('searchTextArea');
    if (searchTextArea) {
        searchTextArea.value = "";
    }
}