function showRenameForm(categoryId) {
    var form = document.getElementById('rename-form-' + categoryId);
    form.style.display = form.style.display === 'none' ? 'block' : 'none';
}

function showUpdateForm(transactionId) {
    var form = document.getElementById('update-form-' + transactionId);
    form.style.display = 'block';
}
  
function hideUpdateForm(transactionId) {
    var form = document.getElementById('update-form-' + transactionId);
    form.style.display = 'none';
}

// Add event listeners to update buttons
const updateButtons = document.querySelectorAll('button[onclick^="showUpdateForm"]');
updateButtons.forEach(function(button) {
  button.addEventListener('click', function() {
    const transactionId = button.getAttribute('onclick').match(/'([^']+)'/)[1];
    showUpdateForm(transactionId);
  });
});

// Add event listeners to cancel buttons
const cancelButtons = document.querySelectorAll('button[onclick^="hideUpdateForm"]');
cancelButtons.forEach(function(button) {
  button.addEventListener('click', function() {
    const transactionId = button.getAttribute('onclick').match(/'([^']+)'/)[1];
    hideUpdateForm(transactionId);
  });
});