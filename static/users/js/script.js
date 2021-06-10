

$(document).ready(function() {

	//////////////////////// Prevent closing from click inside dropdown
    $(document).on('click', '.dropdown-menu', function (e) {
      e.stopPropagation();
    });


    $('.js-check :radio').change(function () {
        var check_attr_name = $(this).attr('name');
        if ($(this).is(':checked')) {
            $('input[name='+ check_attr_name +']').closest('.js-check').removeClass('active');
            $(this).closest('.js-check').addClass('active');
           // item.find('.radio').find('span').text('Add');

        } else {
            item.removeClass('active');
            // item.find('.radio').find('span').text('Unselect');
        }
    });


    $('.js-check :checkbox').change(function () {
        var check_attr_name = $(this).attr('name');
        if ($(this).is(':checked')) {
            $(this).closest('.js-check').addClass('active');
           // item.find('.radio').find('span').text('Add');
        } else {
            $(this).closest('.js-check').removeClass('active');
            // item.find('.radio').find('span').text('Unselect');
        }
    });



	//////////////////////// Bootstrap tooltip
	if($('[data-toggle="tooltip"]').length>0) {  // check if element exists
		$('[data-toggle="tooltip"]').tooltip()
	} // end if
    
    //// To swap images in product detail page as you click on them

    $('.img-block > img').click(function() {
        let $source = $(this).attr('src');
        $('#big-img').attr('src', $source);
        
    });

    //// sign-up validation user

    $('#signUpForm').validate({
        rules: {
            first_name:{
                required:true,
                minlength:4,
                maxlength:15

            },
            last_name:{
                required:true,
                minlength:4,
                maxlength:15,
            },
            email:{
                required:true,
                email:true,
            },
            phone:{
                required:true,
                number:true,
                digits:true,
                minlength:10,
                maxlength:10
            },
        },

        errorPlacement: function (error, element) { 
        element.css('background', 'none'); 
        error.css('background','none');
        error.insertAfter(element); 
        } 
    }); 

    // sign-in validation user

    $('#signInForm').validate({
        rules: {
            phone:{
                required:true,
                number:true,
                digits:true,
                minlength:10,
                maxlength:10
            },
        },
        errorPlacement: function (error, element) { 
            element.css('background', 'none'); 
            error.css('background','none');
            error.insertAfter(element); 
            } 
    });
    
    // Add to cart ajax
    
});

function addToCart(product_id){
    var btn = $('.add-to-cart-btn');
    var dat ={};
    dat['product_id'] = product_id
    $.ajax({
        url:'/add-cart/' ,
        type:'GET',
        data:dat,
        dataType:'json',
        beforeSend:function(){
            btn.attr('disabled',true);
        },
        success:function(res){
            $('#badgeCount').html(res.data)
            $('.ind_count').attr('value',res.ind_count)
            btn.attr('disabled',false)
        }
    })
}

function removeFromCart(product_id){
    var btn = $('.remove-from-cart-btn');
    var dat = {};
    dat['product_id'] = product_id
    $.ajax({
        url:'/remove-cart/',
        type:'GET',
        data:dat,
        dataType:'json',
        beforeSend:function() {
            btn.attr('disabled',true)
        },
        success:function(res){
            $('#badgeCount').html(res.data)
            $('.ind_count').attr('value',res.ind_count)
            btn.attr('disabled',false)
        }
    })

}