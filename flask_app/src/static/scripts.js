function update_chart() {
    payload = {};
    payload['part'] = $('#part').val()
    payload['dimension'] = $('#dimension').val()
    payload['nresults'] = $('#nresults').val()

    $.get('/bar-chart', payload, function(data) {
        $('#bar-chart').html(data);
    });
}

$(document).ready(function(){
    update_chart()
});
