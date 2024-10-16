// function toggleZoom(imgElement) {
//     const overlay = document.getElementById("background-overlay");

//     if (imgElement && imgElement.classList.contains("zoom-fullscreen")) {
//         // Zoom out
//         imgElement.classList.remove("zoom-fullscreen");
//         overlay.style.display = "none";

//         // Restore original width and height
//         if (imgElement.dataset.originalWidth) {
//             imgElement.style.width = imgElement.dataset.originalWidth;
//             delete imgElement.dataset.originalWidth;
//         }

//         if (imgElement.dataset.originalHeight) {
//             imgElement.style.height = imgElement.dataset.originalHeight;
//             delete imgElement.dataset.originalHeight;
//         }

//     } else {
//         // Zoom in
//         // Save original width and height
//         if (!imgElement.dataset.originalWidth) {
//             imgElement.dataset.originalWidth = imgElement.style.width;
//         }

//         if (!imgElement.dataset.originalHeight) {
//             imgElement.dataset.originalHeight = imgElement.style.height;
//         }

//         // Remove width and height to allow natural scaling
//         imgElement.style.width = '';
//         imgElement.style.height = '';

//         imgElement.classList.add("zoom-fullscreen");
//         overlay.style.display = "block";
//     }
// }

function toggleZoom(imgElement) {
    const overlay = document.getElementById("background-overlay");
    const currentClonedImg = overlay.querySelector('img');

    if (overlay.style.display === "flex" && currentClonedImg && currentClonedImg.src === imgElement.src) {
        // Nếu overlay đang hiển thị cùng ảnh này, thì đóng overlay
        overlay.style.display = "none";
        overlay.innerHTML = ''; // Xóa ảnh trong overlay
    } else {
        // Tạo bản sao của ảnh
        const clonedImg = imgElement.cloneNode(true);
        clonedImg.style.width = ''; // Để ảnh tự nhiên theo CSS
        clonedImg.style.height = '';
        clonedImg.classList.remove("selected-image", "selected-submit-image"); // Loại bỏ các lớp chọn

        // Thêm sự kiện để đóng overlay khi nhấp vào ảnh phóng to
        clonedImg.onclick = function () {
            toggleZoom(imgElement);
        };

        // Xóa nội dung hiện tại của overlay và thêm ảnh mới
        overlay.innerHTML = '';
        overlay.appendChild(clonedImg);

        // Hiển thị overlay
        overlay.style.display = "flex";
    }
}

