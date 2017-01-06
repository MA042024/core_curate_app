var clearFieldsUrl = "{% url 'core_curate_clear_fields' %}";
var saveFormUrl = "{% url 'core_curate_save_form' %}";
var validateFormUrl = "{% url 'core_curate_validate_form' %}";
var cancelChangesUrl = "{% url 'core_curate_cancel_changes' %}";
var cancelFormUrl = "{% url 'core_curate_cancel_form' %}";
var downloadXSDUrl = "{% url 'core_curate_download_xsd' data.data_structure.id %}";
var downloadXMLUrl = "{% url 'core_curate_download_xml' data.data_structure.id %}";
var viewDataUrl = "{% url 'core_curate_view_data' data.data_structure.id %}";