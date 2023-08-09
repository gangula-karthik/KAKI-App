document.addEventListener('DOMContentLoaded', function () {
    const deleteAccountBtn = document.getElementById('deleteAccountBtn');
    
    deleteAccountBtn.addEventListener('click', function () {
        // Perform a POST request to the Flask route for deleting the account
        fetch('/delete_account', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                // Optionally, you can send some data along with the request if needed
            })
        }).then(function (response) {
            // Handle the response from the server 
        }).catch(function (error) {
            // Handle errors 
            console.error('Error:', error);
        });
    });
});


document.addEventListener("DOMContentLoaded", function () {
    const deleteAccountBtn = document.getElementById("deleteAccountBtn");
    
    // Confirm before performing delete account action
    deleteAccountBtn.addEventListener("click", function () {
      const confirmDelete = confirm("Are you sure you want to delete your account?");
      if (confirmDelete) {
        // Perform the delete account action
        // You can add your AJAX request or redirect logic here
      }
    });
  
    // Confirm before performing logout action
    const logoutBtn = document.querySelector(".toggle-btn"); // Assuming the logout button has the "toggle-btn" class
    logoutBtn.addEventListener("click", function () {
      const confirmLogout = confirm("Are you sure you want to log out?");
      if (!confirmLogout) {
        event.preventDefault(); // Prevent the default action if the user cancels
      }
    });
  
    // No need for a confirmation alert for the "Update" button, as it's just submitting a form
  });