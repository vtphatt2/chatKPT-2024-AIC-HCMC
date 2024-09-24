const canvas = document.getElementById('drawingCanvas');
const context = canvas.getContext('2d');
let isDrawing = false;

// Draw a bounding line around the canvas
function drawBoundingLine() {
    context.lineWidth = 2;  // Set the thickness of the bounding line
    context.strokeStyle = 'black';  // Set the color of the bounding line
    context.strokeRect(0, 0, canvas.width, canvas.height);  // Draw the bounding rectangle
}

// Initialize canvas with bounding line
drawBoundingLine();

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

    // Redraw the bounding line
    drawBoundingLine();
}
