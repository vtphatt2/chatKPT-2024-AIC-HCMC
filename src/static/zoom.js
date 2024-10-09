function toggleZoom(imgElement) {
    const overlay = document.getElementById("background-overlay");

    if (imgElement && imgElement.classList.contains("zoom-fullscreen")) {
        // Zoom out
        imgElement.classList.remove("zoom-fullscreen");
        overlay.style.display = "none";

        // Restore original width and height
        if (imgElement.dataset.originalWidth) {
            imgElement.style.width = imgElement.dataset.originalWidth;
            delete imgElement.dataset.originalWidth;
        }

        if (imgElement.dataset.originalHeight) {
            imgElement.style.height = imgElement.dataset.originalHeight;
            delete imgElement.dataset.originalHeight;
        }

    } else {
        // Zoom in
        // Save original width and height
        if (!imgElement.dataset.originalWidth) {
            imgElement.dataset.originalWidth = imgElement.style.width;
        }

        if (!imgElement.dataset.originalHeight) {
            imgElement.dataset.originalHeight = imgElement.style.height;
        }

        // Remove width and height to allow natural scaling
        imgElement.style.width = '';
        imgElement.style.height = '';

        imgElement.classList.add("zoom-fullscreen");
        overlay.style.display = "block";
    }
}
