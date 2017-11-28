$(function() {
  $(document).ready(function() {
    $('input[type="checkbox"]').click(function(){
       if( $(this).is(':checked') ) {
            $('#change_id').show();
       } else {
            $('#change_id').hide();
       }
    });
  });
});

