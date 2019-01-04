function TabulateRecords(data) {


    let table = $('.js-table');
    (table.find('table')).remove();

    let content = '<table class="table table"> <thead class="results-headers">';

    content += '<th scope="col"> Study ID</th>';

    content += '<th scope="col"> Modality </th>';
    content += '<th scope="col"> Image </th>';

    content += '<th scope="col"> Patient\'s Birth Date</th>';
    content += '<th scope="col"> Patient\'s Name</th>';
    content += '<th scope="col">  Patient\'s Sex</th>';
    content += '<th scope="col"> SOP Class UID </th>';
    content += '<th scope="col"> Frame of Reference UID </th>';

    content += '<tbody>';

    let i;
    for (i = 0; i < data['tags'].length; i++) {


        let rec = data['tags'][i];
        let image_url = rec['image_url'];
        let filename = `static/images/${image_url}`;
        let img = `<img src='${filename}' alt="" height='500' width='500' />`;


        content += '<tr>';
        content += '<td>' + rec['Study ID'] + '</td>';
        content += '<td>' + rec['Modality'] + '</td>';
        content += '<td>' + img + '</td>';

        content += '<td>' + rec['Patient\'s Birth Date'] + '</td>';
        content += '<td>' + rec['Patient\'s Name'] + '</td>';
        content += '<td>' + rec['Patient\'s Sex'] + '</td>';
        content += '<td>' + rec['SOP Class UID'] + '</td>';
        content += '<td>' + rec['Frame of Reference UID'] + '</td>';
        content += '</tr>';

        console.log(rec);
    }

    content += '</tbody>';
    content += '</thead></table>';


    $(table).append($(content));

}


