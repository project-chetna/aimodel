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

    // Create a canvas to capture the image
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0);

    // Convert canvas to image
    preview.src = canvas.toDataURL('image/png');
    container.classList.add('active');
    preview.style.display = 'block';

    // Close camera after capture
    closeCamera(type);
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