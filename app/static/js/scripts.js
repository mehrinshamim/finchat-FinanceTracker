function showRenameForm(categoryId) {
    var form = document.getElementById('rename-form-' + categoryId);
    form.style.display = form.style.display === 'none' ? 'block' : 'none';
}
