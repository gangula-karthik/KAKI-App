document.addEventListener('DOMContentLoaded', function () {
    const editBtns = document.querySelectorAll('.edit-btn');
    const deleteBtns = document.querySelectorAll('.delete-btn');

    editBtns.forEach(btn => {
      btn.addEventListener('click', function () {
        const cardBody = this.closest('.card-body');
        const userFields = cardBody.querySelectorAll('.about p[data-field]');

        if (this.classList.contains('confirm-btn')) {
          // If the button is in "Confirm" mode, update the user data
          const userId = this.dataset.userId;
          const userData = {};

          userFields.forEach(field => {
            const fieldName = field.getAttribute('data-field');
            const input = field.querySelector('input');
            const value = input.value.trim();
            if (value) {
              userData[fieldName] = value;
              field.innerHTML = fieldName.charAt(0).toUpperCase() + fieldName.slice(1) + ': ' + value;
            } else {
              // Remove placeholder field from user data if input is empty
              delete userData[fieldName];
              field.innerHTML = fieldName.charAt(0).toUpperCase() + fieldName.slice(1) + ': ';
            }
          });

          // Perform a POST request to update the user data in the database
          fetch('/update_user', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              user_id: userId,
              user_data: userData
            })
          }).then(function (response) {
            // Handle the response from the server (if needed)
            console.log('User data updated successfully');
            // Optionally, you can reload the page or show a success message
            window.location.reload();
          }).catch(function (error) {
            // Handle errors (if any)
            console.error('Error:', error);
          });

          // Switch back to "Update Profile" mode
          this.textContent = 'Update Profile';
          this.classList.remove('btn-success');
          this.classList.add('btn-primary');
          this.classList.remove('confirm-btn');

          // Exit edit mode and hide input fields
          cardBody.classList.remove('edit-mode');
          userFields.forEach(field => {
            const input = field.querySelector('input');
            input.style.display = 'none';
          });
        } else {
          // If the button is in "Update Profile" mode, make fields editable
          cardBody.classList.add('edit-mode');
          userFields.forEach(field => {
            const value = field.textContent.trim().split(': ')[1];
            const input = document.createElement('input');
            input.value = value;
            input.setAttribute('placeholder', field.textContent.split(': ')[1]);
            field.innerHTML = field.textContent.split(': ')[0] + ': ';
            field.appendChild(input);
          });

          this.textContent = 'Confirm';
          this.classList.remove('btn-primary');
          this.classList.add('btn-success');
          this.classList.add('confirm-btn');
        }
      });
    });

    deleteBtns.forEach(btn => {
      btn.addEventListener('click', function () {
        const userId = this.dataset.userId;

        // Perform a POST request to delete the user data from the database
        fetch('/delete_user', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            user_id: userId
          })
        }).then(function (response) {
          // Handle the response from the server (if needed)
          console.log('User data deleted successfully');
          // Optionally, you can reload the page or show a success message
          window.location.reload();
        }).catch(function (error) {
          // Handle errors (if any)
          console.error('Error:', error);
        });
      });
    });
  });