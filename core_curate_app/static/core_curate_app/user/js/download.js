
/**
 * AJAX call, download document
 * @param document
 */
download = function(e){
    let toFormat = $('#format').is(':checked')
    let downloadUrl
    if (e.data.document == "data") downloadUrl = downloadXmlUrl
    else downloadUrl = downloadXsdUrl
    window.location.href = downloadUrl + "?format=" + toFormat

};


$('.download-document-btn').on('click', {document: 'data'}, download);
$('.download-template-btn').on('click', {document: 'template'}, download);