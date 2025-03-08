let streams = {
    reference: null,
    verify: null
};

async function toggleCamera(type) {
    const container = document.getElementById(`${type}CameraContainer`);
    const video = document.getElementById(`${type}Video`);

    if (container.classList.contains('active')) {
        closeCamera(type);
    } else {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ video: true });
            streams[type] = stream;
            video.srcObject = stream;
            container.classList.add('active');
        } catch (err) {
            console.error('Error accessing camera:', err);
            alert('Unable to access camera. Please make sure you have granted camera permissions.');
        }
    }
}

function closeCamera(type) {
    const container = document.getElementById(`${type}CameraContainer`);
    const video = document.getElementById(`${type}Video`);

    if (streams[type]) {
        streams[type].getTracks().forEach(track => track.stop());
        streams[type] = null;
    }
    video.srcObject = null;
    container.classList.remove('active');
}

function captureImage(type) {
    const video = document.getElementById(`${type}Video`);
    const preview = document.getElementById(`${type}Preview`);
    const container = preview.parentElement;
    const fileInput = document.getElementById(`${type}Image`); // File input element

    // Create a canvas to capture the image
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0);

    // Convert canvas to Blob and create a File object
    canvas.toBlob((blob) => {
        if (!blob) {
            alert("Error capturing image.");
            return;
        }

        // Create a file from the blob
        const file = new File([blob], `${type}_capture.png`, { type: "image/png" });

        // Create a new DataTransfer object to simulate file selection in the input field
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(file);
        fileInput.files = dataTransfer.files; // Assign file to input

        // Set preview image
        const objectURL = URL.createObjectURL(file);
        preview.src = objectURL;
        preview.style.display = 'block';
        container.classList.add('active');

        // Close camera after capture
        closeCamera(type);
    }, "image/png");
}

function removeImage(type) {
    // Clear the file input
    const fileInput = document.getElementById(`${type}Image`);
    fileInput.value = '';

    // Clear the preview
    const preview = document.getElementById(`${type}Preview`);
    preview.src = '';

    // Hide the preview container
    const previewContainer = preview.parentElement;
    previewContainer.classList.remove('active');
    preview.style.display = 'none';
}