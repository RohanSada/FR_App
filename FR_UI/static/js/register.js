const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const context = canvas.getContext("2d");
const clickButton = document.getElementById("clickButton");
const backButton = document.getElementById("backButton");

function startCamera() {
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
            video.srcObject = stream;
        })
        .catch(error => {
            console.error("Error accessing camera:", error);
            alert("Unable to access camera.");
        });
}

function captureImage() {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    const imageData = canvas.toDataURL('image/png');

    fetch('/get_bbox', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ imageData }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert("Error: " + data.error);
        } else {
            const boundingBoxes = data.BoundingBoxes;
            displayCroppedImages(imageData, boundingBoxes);
        }
    })
    .catch(error => {
        console.error("Error processing image:", error);
        alert("Failed to send image to the server.");
    });
}

function displayCroppedImages(imageData, boundingBoxes) {
    const croppedContainer = document.getElementById("croppedContainer");
    croppedContainer.innerHTML = "";

    boundingBoxes.forEach(box => {
        const [startX, startY, endX, endY] = box;

        const width = endX - startX;
        const height = endY - startY;

        const croppedCanvas = document.createElement("canvas");
        const croppedContext = croppedCanvas.getContext("2d");

        croppedCanvas.width = width;
        croppedCanvas.height = height;

        const image = new Image();
        image.onload = () => {
            croppedContext.drawImage(
                image,
                startX, startY, width, height, 
                0, 0, width, height
            );
            const croppedImageURL = croppedCanvas.toDataURL("image/png");

            const container = document.createElement("div");
            container.classList.add("cropped-item");

            const imgElement = document.createElement("img");
            imgElement.src = croppedImageURL;
            imgElement.classList.add("cropped-img");

            const textBox = document.createElement("input");
            textBox.type = "text";
            textBox.placeholder = "Enter label";
            textBox.classList.add("label-input");

            const submitButton = document.createElement("button");
            submitButton.textContent = "Submit";
            submitButton.classList.add("submit-btn");

            submitButton.addEventListener("click", () => {
                const label = textBox.value;
                if (!label) {
                    alert("Please enter a label before submitting.");
                    return;
                }

                fetch('/register_face', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ label, croppedImageURL }),
                })
                .then(response => {
                    if (response.ok) {
                        alert("Face registered successfully!");
                    } else {
                        alert("Failed to register face.");
                    }
                })
                .catch(error => {
                    console.error("Error registering face:", error);
                    alert("An error occurred.");
                });
            });

            container.appendChild(imgElement);
            container.appendChild(textBox);
            container.appendChild(submitButton);

            croppedContainer.appendChild(container);
        };
        image.src = imageData; 
    });
}

function navigateBack() {
    window.history.back();
}

clickButton.addEventListener("click", captureImage);
backButton.addEventListener("click", navigateBack);

startCamera();