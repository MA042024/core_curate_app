
/**
 * Display the switching to form editor confirmation popup.
 */
var switchToFormEditorModal = function() {
    $("#switch-to-form-editor").modal("show");
}

/**
 * Switch the current to form editor.
 */
var switchEditor = function() {
    $.ajax({
        url: saveFormUrl,
        type: 'POST',
        data: { 'id': documentID, 'form_string': getContent()},
        dataType: 'json',
        success: function(data) {
            window.location = switchToFormUrl.replace("curate_data_structure_id", documentID);
        },
        error: function(dataXHR) {
            $.notify(dataXHR.responseJSON.error, "danger");
            if( "details" in dataXHR.responseJSON){
                jqError.html('<i class="fas fa-exclamation-triangle"></i> '+ dataXHR.responseJSON.details);
                jqError.show();
            }
        }
    }).always(function(data) {
        $("#switch-to-form-editor").modal("hide");
    });
}

$(document).on('click', '.btn.switch-to-form-editor', switchToFormEditorModal);
$(document).on('click', '.save-and-switch-to-form-editor',switchEditor);
