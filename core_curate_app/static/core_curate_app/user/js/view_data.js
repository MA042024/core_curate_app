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
   let objectID = $("#curate_data_structure_id").html();
   let $saveToRepoButton = $(".btn.save-to-repo > i");
   let icon = $saveToRepoButton.attr("class");
   // Show loading spinner
   showSpinner($saveToRepoButton)

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
        hideSpinner($saveToRepoButton, icon);
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

/**
 * AJAX call, download document
 * @param document
 */
download = function(document){
    let toFormat = $('#format').is(':checked')

    // Download form/template
    if (document === "form")
        window.location = downloadDocumentUrl+"?pretty_print="+toFormat
    else
        window.location = downloadTemplateUrl+"?pretty_print="+toFormat
};

$(document).on('click', '.download-document-btn', e=>download("form"));
$(document).on('click', '.download-template-btn', e=>download("template"));