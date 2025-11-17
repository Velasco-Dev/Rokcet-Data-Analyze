// This file contains JavaScript code for the dashboard, handling interactions and dynamic behaviors.

document.addEventListener('DOMContentLoaded', function() {
    // Function to open the upload modal
    const openUploadModal = () => {
        const uploadModal = document.getElementById('uploadModal');
        const modal = new bootstrap.Modal(uploadModal);
        modal.show();
    };

    // Attach event listener to the upload button
    const uploadButton = document.querySelector('.btn-success');
    if (uploadButton) {
        uploadButton.addEventListener('click', openUploadModal);
    }

    // Optional: Handle form submission via AJAX
    const uploadForm = document.getElementById('uploadForm');
    if (uploadForm) {
        uploadForm.addEventListener('submit', function(event) {
            event.preventDefault(); // Prevent default form submission

            const formData = new FormData(uploadForm);
            fetch(uploadForm.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': getCookie('csrftoken') // Include CSRF token
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Handle successful upload (e.g., update the dashboard)
                    location.reload(); // Reload the page to see the new file
                } else {
                    // Handle errors (e.g., display error messages)
                    alert(data.error || 'Error uploading file.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while uploading the file.');
            });
        });
    }

    // Function to get CSRF token from cookies
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Check if this cookie string begins with the name we want
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});