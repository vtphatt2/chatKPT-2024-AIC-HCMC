function submitToSystem() {
    const submitType = document.querySelector('input[name="submit_type"]:checked').value;

    // Get the values of the textareas
    const videoName = document.getElementById('video_name').value.trim();
    const frameId = document.getElementById('frame_id').value.trim();
    const answer = document.getElementById('answer').value.trim();

    // Get the <p> tag to update the announcement
    const announcement = document.getElementById('submit_annoucement');

    // Check if video_name and frame_id are empty
    if (!videoName) {
        alert("Please enter the video name.");  // Use alert dialog
        return;
    }

    if (!frameId) {
        alert("Please enter the frame ID.");  // Use alert dialog
        return;
    }

    // If "QA Submit" is selected, check if answer is filled
    if (submitType === "QA Submit" && !answer) {
        alert("Please enter the answer for QA Submit.");  // Use alert dialog
        return;
    }

    // Perform the fetch request to get session ID, evaluation ID, and fps
    fetch('/submit_to_system', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ video_name: videoName })
    })
    .then(response => response.json())
    .then(result => {
        const sessionId = result.session_id;
        const evaluationId = result.evaluation_id;
        const fps = result.fps;

        // Convert frame_id to milliseconds (frame_id / fps)
        const timeMs = Math.round(frameId / fps * 1000);

        // Prepare the confirmation message
        const confirmationMessage = (
            submitType + " Confirmation:\n" +
            "Session ID: " + sessionId + "\n" +
            "Evaluation ID: " + evaluationId + "\n" +
            "Video Name: " + videoName + "\n" +
            "Time in milliseconds: " + timeMs + "\n\n" +
            "Do you want to proceed?"
        );

        // Ask the user to confirm
        if (!confirm(confirmationMessage)) {
            // If user cancels, stop the function
            return;
        }

        // Call the appropriate function based on the submission type
        if (submitType === "QA Submit") {
            submitQA(sessionId, evaluationId, videoName, timeMs, answer, announcement);
        } else if (submitType === "KIS Submit") {
            submitKIS(sessionId, evaluationId, videoName, timeMs, announcement);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        announcement.textContent = 'Error: Unable to retrieve session data.';
    });
}

// Function to handle QA Submit
function submitQA(sessionId, evaluationId, videoName, timeMs, answer, announcement) {
    const answerQA = `${answer}-${videoName}-${timeMs}`;

    // Prepare the body for QA Submit
    const body = {
        "answerSets": [{
            "answers": [
                {
                    "text": answerQA
                }
            ]
        }]
    };

    // Perform the POST request for QA Submit
    fetch(`https://eventretrieval.one/api/v2/submit/${evaluationId}?session=${sessionId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(body)
    })
    .then(response => {
        // Check if the response is OK (status code 2xx)
        if (!response.ok) {
            return response.json().then(errData => {
                // Handle failed submission (e.g., duplicate submission)
                throw new Error(`QA Submit failed: ${errData.description}`);
            });
        }
        return response.json();  // Parse the response as JSON
    })
    .then(data => {
        // Check for success in the response
        console.log('Response Data:', data);
        if (data.status && data.submission === "CORRECT") {
            announcement.textContent = 'QA Submit successful: ' + data.description;
        } else {
            throw new Error('QA Submit failed: ' + (data.description || 'Unknown error'));
        }
    })
    .catch(error => {
        console.error('Error:', error);
        announcement.textContent = 'Error: ' + error.message;
    });
}


// Function to handle KIS Submit
function submitKIS(sessionId, evaluationId, videoName, timeMs, announcement) {
    // Prepare the body for KIS Submit
    const body = {
        "answerSets": [{
            "answers": [
                {
                    "mediaItemName": videoName,
                    "start": timeMs,
                    "end": timeMs
                }
            ]
        }]
    };

    // Perform the POST request for KIS Submit
    fetch(`https://eventretrieval.one/api/v2/submit/${evaluationId}?session=${sessionId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(body)  // Ensure the body is correctly formatted as JSON
    })
    .then(response => {
        // Check if the response is OK (status code 2xx)
        if (!response.ok) {
            // Parse the error response to get the description from the server
            return response.json().then(errData => {
                throw new Error(`KIS Submit failed: ${errData.description}`);
            });
        }
        return response.json();  // Parse the response as JSON
    })
    .then(data => {
        // Check for success in the response
        console.log('Response Data:', data);
        if (data.status && data.submission === "CORRECT") {
            announcement.textContent = 'KIS Submit successful: ' + data.description;
        } else {
            throw new Error('KIS Submit failed: ' + (data.description || 'Unknown error'));
        }
    })
    .catch(error => {
        // Log the error and display it in the announcement
        console.error('Error:', error);
        announcement.textContent = 'Error: ' + error.message;
    });
}


