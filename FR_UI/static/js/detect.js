async function initializeCamera(videoElement) {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        videoElement.srcObject = stream;
    } catch (error) {
        console.error("Error accessing the camera:", error);
    }
}

async function sendFrameToBackend(videoElement) {
    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d');
    canvas.width = videoElement.videoWidth;
    canvas.height = videoElement.videoHeight;

    context.drawImage(videoElement, 0, 0, canvas.width, canvas.height);

    const imageData = canvas.toDataURL('image/jpeg');

    try {
        const response = await fetch('/detect_face', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ image: imageData })
        });

        const result = await response.json();

        if (!result.BoundingBoxes || result.BoundingBoxes.length === 0) {
            console.log('No detections, skipping to the next frame.');
            return null; 
        }

        const detections = result.BoundingBoxes.map((bbox, index) => ({
            name: result.Names[index],
            boundingBox: bbox
        }));

        return detections;

    } catch (error) {
        console.error("Error sending frame to backend:", error);
        return null; 
    }
}

function overlayDetection(videoElement, detections) {
    const canvasOverlay = document.getElementById('overlayCanvas');
    const context = canvasOverlay.getContext('2d');

    canvasOverlay.width = videoElement.videoWidth;
    canvasOverlay.height = videoElement.videoHeight;

    context.clearRect(0, 0, canvasOverlay.width, canvasOverlay.height);

    const scaleX = canvasOverlay.width / videoElement.videoWidth;
    const scaleY = canvasOverlay.height / videoElement.videoHeight;

    detections.forEach(detection => {
        const { name, boundingBox } = detection;
        const [startx, starty, endx, endy] = boundingBox;

        const scaledStartX = startx * scaleX;
        const scaledStartY = starty * scaleY;
        const scaledEndX = endx * scaleX;
        const scaledEndY = endy * scaleY;

        const width = scaledEndX - scaledStartX;
        const height = scaledEndY - scaledStartY;

        context.strokeStyle = 'red';
        context.lineWidth = 2;
        context.strokeRect(scaledStartX, scaledStartY, width, height);

        context.fillStyle = 'red';
        context.font = '16px Arial';
        context.fillText(name, scaledStartX, scaledStartY - 5);
    });
}

async function startDetection() {
    const videoElement = document.getElementById('videoFeed');
    await initializeCamera(videoElement);

    setInterval(async () => {
        const startTime = performance.now();
        const detections = await sendFrameToBackend(videoElement);

        if (detections) {
            overlayDetection(videoElement, detections);
        } else {
            console.log('Skipping this frame.');
        }
        const endTime = performance.now();
        const timeTaken = endTime - startTime;
        console.log(`Time to send and get the frame: ${timeTaken.toFixed(2)} ms`);
    }, 200);
}

function navigateBack() {
    window.history.back();
}

window.onload = startDetection;
backButton.addEventListener("click", navigateBack);