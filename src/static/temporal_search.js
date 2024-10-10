// static/temporal_search.js

function performTemporalSearch() {
    const textFirstThis = document.getElementById('text_first_this_area').value;
    const textThenThat = document.getElementById('text_then_that_area').value;
    const translatedFirstThisElement = document.getElementById("translated_text_for_temporal_search");
    const discardedVideos = document.getElementById('discarded_videos').value;
    const newFileName = document.getElementById('new_file_name').value;
    const keywords = document.getElementById('keywords').value;
    const k = document.getElementById('k').value;
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

    // Show loading state if needed
    translatedFirstThisElement.innerText = "Processing temporal search...";

    fetch('/temporal_search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
            textFirstThis: textFirstThis, 
            textThenThat: textThenThat,
            discardedVideos: discardedVideos,
            newFileName: newFileName,
            keywords: keywords,
            k: value
        })
    })
    .then(response => response.json())
    .then(data => {
        // Update translated text
        translatedFirstThisElement.innerText = `Translated First This: ${data.translated_first_this}\nTranslated Then That: ${data.translated_then_that}`;

        // Display search results (similar to searchByText)
        const searchResultContainer = document.getElementById('search-result');
        searchResultContainer.innerHTML = ''; // Clear previous results

        const submissionList = data.submission_list;

        submissionList.forEach(([videoName, video_link, images, fps], groupIndex) => {
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
                imgElement.src = `/image/${imagePath.substring(1)}`;  // Serve the image via the /image/<path>
                imgElement.alt = `Frame ${frameId}`;
                imgElement.style.width = '300px';  // Set initial width
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
    });
}

// Attach this function to the temporal search button
document.getElementById('searchBtn2').addEventListener('click', performTemporalSearch);
