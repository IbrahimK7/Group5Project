// editprofile.js - Handles AJAX profile updates without page reload

document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();  // Prevent page reload

            const formData = new FormData(this);
            try {
                const response = await fetch('/api/update-profile', {
                    method: 'POST',
                    body: formData
                });

                const result = await response.json();

                if (result.success) {
                    // Update the current profile display
                    const newUsername = formData.get('username') || 'Not set';
                    const newBio = formData.get('bio') || 'Not set';
                    const profileCard = document.querySelector('.card-body');
                    if (profileCard) {
                        profileCard.innerHTML = `
                            <p><strong>Username:</strong> ${newUsername}</p>
                            <p><strong>Bio:</strong> ${newBio}</p>
                        `;
                    }

                    // Show success message
                    alert(result.message);
                } else {
                    alert('Error updating profile');
                }
            } catch (error) {
                alert('Network error: ' + error.message);
            }
        });
    }
});