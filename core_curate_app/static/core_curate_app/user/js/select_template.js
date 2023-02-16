$(document).ready(function(){
    loadTemplateSelectionControllers();
    initBanner();
});


/**
 * Load controllers for template selection
 */
loadTemplateSelectionControllers = function()
{
    $('.btn.set-template').on('click', setCurrentTemplate);
}


initBanner = function()
{
    $("[data-hide]").on("click", function(){
        $(this).closest("." + $(this).attr("data-hide")).hide(200);
    });
}

/**
 * Set the current template
 * @returns {Boolean}
 */
setCurrentTemplate = function()
{
    var templateID = $(this).parent().parent().children(':first').attr('templateID');
    $('.btn.set-template').off('click');
    set_current_template(templateID);
    return false;
}

/**
 * AJAX call, sets the current template
 * @param templateFilename name of the selected template
 * @param templateID id of the selected template
 */
set_current_template = function(templateID){
    $('#template_selection').load(document.URL +  ' #template_selection', function() {
        loadTemplateSelectionControllers();
    });
    load_start_form(templateID);
    displayTemplateSelectedDialog();
}

/**
 * Show a dialog when a template is selected
 */
displayTemplateSelectedDialog = function()
{
    $("#select-template-modal").modal("show");
    // before create a new listener delete all the previous listeners
    $('#btn-display-data').off('click');
    $('#btn-display-data').on('click', function(){
        // start regular form processing
        displayTemplateProcess($("#btn-display-data > i"));

    });
}


/**
 * AJAX call, loads the start curate form
 */
load_start_form = function(templateID){
    $.ajax({
        url : startCurate,
        type : "GET",
        dataType: "json",
        data : {
            'template_id': templateID
        },
        success: function(data){
            $("#banner_errors").hide()
            $("#form_start_content").html(data.template);
            initSaveButton();
            syncRadioButtons();
        },
        error:function(data){
            if (data.responseText != ""){
                $("#form_start_errors").html(data.responseText);
                $("#banner_errors").show(500)
                return (false);
            }else{
                return (true);
            }
        },
    });
}

displayTemplateProcess = function (iconSelector)
{
    if (validateStartCurate()){
       var icon = iconSelector.attr("class");

       showSpinner(iconSelector)

       var formData = new FormData($( "#form_select_template" )[0]);
       $.ajax({
            url: startCurate,
            type: 'POST',
            data: formData,
            cache: false,
            contentType: false,
            processData: false,
            success: function(data){
                window.location = data;
            },
            error: function(data){
                // get old button icon
                hideSpinner(iconSelector, icon)
                // FIXME: temp fix for safari support
                $( "#id_file" ).prop('disabled', false);
                // FIXME: temp fix for chrome support (click twice on start raise an error)
                $( "#btn-display-data" ).prop('disabled', false);
                if (data.responseText != ""){
                    $("#form_start_errors").html(data.responseText);
                    $("#banner_errors").show(500);
                }
                // uncheck direct upload checkbox
                $("#id_direct_upload").prop("checked", false);
                $("#id_text_editor").prop("checked", false);
            },
       })

   }
}

/**
 * Validate fields of the start curate form
 */
validateStartCurate = function(){
    var errors = "";

	$("#banner_errors").hide()
	// check if an option has been selected
	selected_option = $( "#form_start_content" ).find("input:radio[name='curate_form']:checked").val()
	if (selected_option == undefined){
		errors = "No option selected. Please check one radio button."
		$("#form_start_errors").html(errors);
		$("#banner_errors").show(500)
		return (false);
	}else{
		if (selected_option == "new"){
			if ($( "#id_document_name" ).val().trim() == ""){
				errors = "You selected the option 'Create a new document'. Please provide a name for the document."
			}
		}else if (selected_option == "open"){
			if ($( "#id_forms" ).val() == ""){
				errors = "You selected the option 'Open a Form'. Please select a form from the list."
			}
		}else if (selected_option == "upload"){
			if ($( "#id_file" ).val() == ""){
				errors = "You selected the option 'Upload a File'. Please select an XML file."
			}
		}
	}
	if (errors != ""){
		$("#form_start_errors").html(errors);
		$("#banner_errors").show(500)
		$("#id_text_editor").prop("checked", false);
		return (false);
	}else{
	    // FIXME: temp fix for safari support
	    if (selected_option != "upload"){
            $( "#id_file" ).prop('disabled', true);
        }
        // FIXME: temp fix for chrome support (click twice on start raise an error)
        $( "#btn-display-data" ).prop('disabled', true);
		return (true)
	}
}

syncRadioButtons =function()
{
	// auto set radio buttons value according to what option the user is choosing
	$("#id_document_name").on("click", function(){
	    $("input:radio[name=curate_form][value='new']").prop("checked", true),
	    $("#btn-save-data").attr('hidden', true)
	});
	$("#id_forms").on("change", function(){
	    $("input:radio[name=curate_form][value='open']").prop("checked", true),
	    $("#btn-save-data").attr('hidden', true)
    });
	$("#id_file").on("change", function(){
	    $("input:radio[name=curate_form][value='upload']").prop("checked", true);
	    $("#btn-save-data").attr('hidden', false)
	});
	$("#curate_form_new").on("change", function(){$("#btn-save-data").attr('hidden', true)});
	$("#curate_form_open").on("change", function(){$("#btn-save-data").attr('hidden', true)});
	$("#curate_form_upload").on("change", function(){$("#btn-save-data").attr('hidden', false)});
}

/**
* Initialize the save data button
*/
initSaveButton = function(){
    $("#id_direct_upload").prop("checked", false);
    $("#id_text_editor").prop("checked", false);
    $("#btn-save-data").on("click", function(){
        // check hidden direct upload checkbox
        $("#id_direct_upload").prop("checked", true);
        // start regular form processing
        displayTemplateProcess($("#btn-save-data > i"));
    });
    $("#btn-open-data").on("click", function(){
        // check hidden text editor checkbox
        $("#id_text_editor").prop("checked", true);
        // start regular form processing
        displayTemplateProcess($("#btn-open-data > i"));
    });
}