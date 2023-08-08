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
