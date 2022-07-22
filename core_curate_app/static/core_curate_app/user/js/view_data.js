/**
 * Load controllers for view data
 */
$(document).ready(function() {
    $('.btn.save-to-repo').on('click', saveToRepository);
});

/**
 * AJAX, to start form save
 */
var saveToRepository = function()
{
   var objectID = $("#curate_data_structure_id").html();
   var icon = $(".btn.save-to-repo > i").attr("class");
   // Show loading spinner
   showSpinner($(".btn.save-to-repo > i"))

   $.ajax({
        url : saveDataUrl,
        type: 'POST',
        data: {
          'id': objectID
        },
        dataType: 'json',
        success : function(data) {
            window.location = curateIndexUrl;
        },
        error: function(data){
            XMLDataSavedError(data.responseText);

        }
   }).always(function() {
        // get old button icon
        hideSpinner.attr($(".btn.save-to-repo > i"),icon);
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