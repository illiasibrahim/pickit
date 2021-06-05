

$(document).ready(function(){
    $("#search-input").on("keyup", function() {
      var value = $(this).val().toLowerCase();
      $("#data-table tbody tr").filter(function() {
        $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
      });
    });

    // category page delete modal
    $('.delete-cat-item').click(function(){
        $('#delete-cat-modal').show();
    });
    $('#cancel-delete-cat').click(function(){
        $('#delete-cat-modal').hide()
    });

    // brand page delete modal
    $('.delete-brand-item').click(function(){
      $('.delete-brand-modal').show();
    });
    $('#cancel-delete-brand').click(function(){
        $('.delete-brand-modal').hide()
    });

    // product page delete modal
    $('.delete-product-item').click(function(){
      $('.delete-product-modal').show();
    });
    $('#cancel-delete-product').click(function(){
        $('.delete-product-modal').hide()
    });

    // banner page delete modal
    $('.delete-banner-item').click(function(){
      $('.delete-banner-modal').show();
    });
    $('#cancel-delete-banner').click(function(){
        $('.delete-banner-modal').hide()
    });

    // poster page delete modal
    $('.delete-poster-item').click(function(){
      $('.delete-poster-modal').show();
    });
    $('#cancel-delete-poster').click(function(){
        $('.delete-poster-modal').hide()
    });
});