function update_bc() {
    payload = {};
    payload['part'] = $('#part').val()
    payload['dimension'] = $('#dimension').val()
    payload['nresults'] = $('#nresults').val()

    $.get('/component', payload, function(data) {
        $('#bar-chart').html(data);
    });
}

$(document).ready(function(){
    update_bc()
});
