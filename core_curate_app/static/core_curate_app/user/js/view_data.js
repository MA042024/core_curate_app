/**
 * Load controllers for view data
 */
$(document).ready(function() {
    $('.btn.save-to-repo').on('click', saveToRepository);
});


/**
 * Save Form to repository
 */
var saveToRepository = function()
{
    $("#save-modal").modal("show");
    $("#btn-save").on("click", saveToRepositoryProcess);
};

/**
 * AJAX, to start form save
 */
var saveToRepositoryProcess = function()
{
   var objectID = $("#curate_data_structure_id").html();
   $.ajax({
        url : saveDataUrl,
        type: 'POST',
        data: {
          'id': objectID
        },
        dataType: 'json',
        success : function(data) {
            console.log("test");
            $("#save-modal").modal("hide");
            XMLDataSavedSuccess();
        },
        error: function(data){
            $("#save-modal").modal("hide");
            XMLDataSavedError(data.responseText);
        }
    });
};

/**
 * Saved XML data to DB success message
 */
var XMLDataSavedSuccess = function()
{
    var $saved_success_modal = $("#save-success-modal");
    $saved_success_modal.modal("show");
    $saved_success_modal.on("hidden.bs.modal", function () {
        window.location = curateIndexUrl;
    });
};

/**
 * Saved XML data to DB error message.
 * @param errors
 */
var XMLDataSavedError = function(errors)
{
    var $saved_error_modal = $("#save-error-modal");
    $("#saveErrorMessage").html(errors);
    $saved_error_modal.modal("show");
};