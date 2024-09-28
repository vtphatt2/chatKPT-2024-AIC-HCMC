document.getElementById('csvFiles').addEventListener('change', function() {
    var selectedFile = this.value;

    fetch('/get_csv_content', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ filename: selectedFile })
    })
    .then(response => response.json())
    .then(data => {
        if (data.content !== undefined) {
            // If the file has content, display it; otherwise, clear the textarea
            document.querySelector('textarea[name="csv_file_content"]').value = data.content || '';
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

// Save button functionality
document.getElementById('saveBtn').addEventListener('click', function() {
    var selectedFile = document.getElementById('csvFiles').value;
    var content = document.querySelector('textarea[name="csv_file_content"]').value;
    
    if (selectedFile === "None") {
        alert("Please select a file to save.");
        return;
    }

    fetch('/save_csv', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ filename: selectedFile, content: content })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    })
    .catch(error => {
        alert('Error saving file: ' + error);
        console.error('Error:', error);
    });
});

// Delete button functionality
document.getElementById('deleteBtn').addEventListener('click', function() {
    var selectedFile = document.getElementById('csvFiles').value;

    if (selectedFile === "None") {
        alert("Please select a file to delete.");
        return;
    }

    if (confirm("Are you sure you want to delete this file?")) {
        fetch('/delete_csv', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ filename: selectedFile })
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                alert(data.message);
                // Optionally, remove the deleted file from the dropdown
                var option = document.querySelector(`#csvFiles option[value="${selectedFile}"]`);
                if (option) option.remove();
                document.querySelector('textarea[name="csv_file_content"]').value = ''; // Clear textarea
            } else {
                alert(data.error);
            }
        })
        .catch(error => {
            alert('Error deleting file: ' + error);
            console.error('Error:', error);
        });
    }
});

// Create new file functionality
document.getElementById('createBtn').addEventListener('click', function() {
    var newFileName = document.querySelector('input[name="new_file_name"]').value.trim();

    // Check if the filename is not empty and ends with .csv
    if (newFileName === "") {
        alert("Please enter a filename.");
        return;
    }

    if (!newFileName.endsWith('.csv')) {
        alert("Filename must end with .csv");
        return;
    }

    fetch('/create_csv', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ filename: newFileName })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert(data.message);
            // Optionally, add the new file to the dropdown menu
            var newOption = document.createElement('option');
            newOption.value = newFileName;
            newOption.textContent = newFileName;
            document.getElementById('csvFiles').appendChild(newOption);
        } else if (data.error) {
            alert(data.error);
        }
    })
    .catch(error => {
        alert('Error creating file: ' + error);
        console.error('Error:', error);
    });
});
