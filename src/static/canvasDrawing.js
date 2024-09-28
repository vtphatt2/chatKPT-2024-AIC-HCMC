const canvas = document.getElementById('drawingCanvas');
const context = canvas.getContext('2d');
let isDrawing = false;

// Draw a bounding line around the canvas
function drawBoundingLine() {
    context.lineWidth = 2;  // Set the thickness of the bounding line
    context.strokeStyle = 'black';  // Set the color of the bounding line
    context.strokeRect(0, 0, canvas.width, canvas.height);  // Draw the bounding rectangle
}

// Initialize canvas with white background and bounding line
function initializeCanvas() {
    // Fill the canvas with white color
    context.fillStyle = 'white';  // Set the background color
    context.fillRect(0, 0, canvas.width, canvas.height);  // Fill the canvas
    drawBoundingLine();  // Draw the bounding line
}

initializeCanvas();

// Start drawing when the mouse is pressed down
canvas.addEventListener('mousedown', (event) => {
    isDrawing = true;
    context.beginPath();
    context.moveTo(event.offsetX, event.offsetY);
});

// Draw as the mouse moves
canvas.addEventListener('mousemove', (event) => {
    if (isDrawing) {
        context.lineTo(event.offsetX, event.offsetY);
        context.stroke();
    }
});

// Stop drawing when the mouse is released or leaves the canvas
canvas.addEventListener('mouseup', () => {
    isDrawing = false;
});

canvas.addEventListener('mouseleave', () => {
    isDrawing = false;
});

function clearCanvas() {
    // Clear the entire canvas
    context.clearRect(0, 0, canvas.width, canvas.height);

    // Redraw the white background and bounding line
    initializeCanvas();
}
