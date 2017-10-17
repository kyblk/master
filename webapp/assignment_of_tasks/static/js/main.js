$(function() {
    $('#change_id').hide();
    $('#id_change_state').change(function(){
        if($('#id_change_state').val() == "Y") {
            $('#change_id').show();
        } else {
            $('#change_id').hide();
        }
    });
});