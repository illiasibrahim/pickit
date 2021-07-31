

var path = window.location.href;

$(document).ready(function () {

    //////////////////////// Prevent closing from click inside dropdown
    $(document).on('click', '.dropdown-menu', function (e) {
        e.stopPropagation();
    });


    $('.js-check :radio').change(function () {
        var check_attr_name = $(this).attr('name');
        if ($(this).is(':checked')) {
            $('input[name=' + check_attr_name + ']').closest('.js-check').removeClass('active');
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
    if ($('[data-toggle="tooltip"]').length > 0) {  // check if element exists
        $('[data-toggle="tooltip"]').tooltip()
    } // end if

    //// To swap images in product detail page as you click on them

    $('.img-block > img').click(function () {
        let $source = $(this).attr('src');
        $('#big-img').attr('src', $source);

    });

    //// sign-up validation user

    $('#signUpForm').validate({
        rules: {
            first_name: {
                required: true,
                minlength: 4,
                maxlength: 15

            },
            last_name: {
                required: true,
                minlength: 1,
                maxlength: 15,
            },
            email: {
                required: true,
                email: true,
            },
            phone: {
                required: true,
                number: true,
                digits: true,
                minlength: 10,
                maxlength: 10
            },
            password: {
                required:true,
                minlength: 6
            },
            password_confirm: {
                required:true,
                minlength: 6,
                equalTo: "#password"
            },
        },

        errorPlacement: function (error, element) {
            element.css('background', 'none');
            error.css('background', 'none');
            error.insertAfter(element);
        }
    });

    // sign-in validation user

    $('#signInForm').validate({
        rules: {
            phone: {
                required: true,
                number: true,
                digits: true,
                minlength: 10,
                maxlength: 10
            },
        },
        errorPlacement: function (error, element) {
            element.css('background', 'none');
            error.css('background', 'none');
            error.insertAfter(element);
        }
    });

    $('#signInFormPassword').validate({
        rules: {
            phone: {
                required: true,
                number: true,
                digits: true,
                minlength: 10,
                maxlength: 10
            },
            password: {
                required: true,

            }
        },
        errorPlacement: function (error, element) {
            element.css('background', 'none');
            error.css('background', 'none');
            error.insertAfter(element);
        }
    });

    $('#enable-edit').click(function () {
        $(this).hide()
        $('#edit-profile').show()
        $('.form-control').removeAttr('disabled')
    })

    $('#showAddAddress').click(function () {
        $('#addAddress').toggle()
        $('#editAddress').hide()
    })



    $('#loginWithPassword').click(function () {
        $('#signInFormPassword').show()
        $('#signInForm').hide()
    })

    $('#loginWithOTP').click(function () {
        $('#signInFormPassword').hide()
        $('#signInForm').show()
    })


});

// Add to cart ajax

function addToCart(product_id, product_name = null) {
    // var btn = $('.add-to-cart-btn');
    var id = "add"+product_id
    var btn = $('#'+id)
    // var btn = document.getElementById(product_id+product_id)
    var dat = {};
    dat['product_id'] = product_id
    $.ajax({
        url: '/add-cart/',
        type: 'GET',
        data: dat,
        dataType: 'json',
        beforeSend: function () {
            btn.attr('disabled', true);
        },
        success: function (res) {
            $('#badgeCount').html(res.data)
            $('#badgeCountMob').html(res.data)
            btn.attr('disabled', false)
            if (product_name != null) {
                document.getElementById(product_name).innerHTML = res.ind_count;
                document.getElementById('cartValue').innerHTML = '₹'+res.cart_value+'.00';
                document.getElementById(product_name+product_id).innerHTML = '₹ '+res.ind_price+'.00';
                
            }

        }
    })
}

function removeFromCart(product_id, product_name) {
    var count = document.getElementById(product_name).innerHTML
    if (count == 1) {
        var confirm_delete = confirm('Are you sure you want to delete this item from cart?')
        if (confirm_delete) {
            var btn = $('.remove-from-cart-btn');
            var dat = {};
            console.log(product_name)
            dat['product_id'] = product_id
            $.ajax({
                url: '/remove-cart/',
                type: 'GET',
                data: dat,
                dataType: 'json',
                beforeSend: function () {
                    btn.attr('disabled', true)
                },
                success: function (res) {
                    $('#badgeCount').html(res.data)
                    $('#badgeCountMob').html(res.data)
                    if (res.rem == true) {
                        document.getElementById(product_id).remove()
                        location.reload()
                    }
                    else {
                        document.getElementById(product_name).innerHTML = res.ind_count;
                        
                        btn.attr('disabled', false)
                    }
                }
            })
        }
    }
    else{
    var btn = $('.remove-from-cart-btn');
    var dat = {};
    console.log(product_name)
    dat['product_id'] = product_id
    $.ajax({
        url: '/remove-cart/',
        type: 'GET',
        data: dat,
        dataType: 'json',
        beforeSend: function () {
            btn.attr('disabled', true)
        },
        success: function (res) {
            $('#badgeCount').html(res.data)
            if (res.rem == true) {
                document.getElementById(product_id).remove()
                location.reload()
            }
            else {
                document.getElementById(product_name).innerHTML = res.ind_count;
                document.getElementById('cartValue').innerHTML = '₹'+res.cart_value+'.00';
                document.getElementById(product_name+product_id).innerHTML = '₹ '+res.ind_price+'.00';
                btn.attr('disabled', false)
            }
        }
    })
}
}


// edit address

function editAddress(address_id){
    $('#editAddress').toggle()
    $('#addAddress').hide()
    var section = document.getElementById('editAddress')
    var dat = {};
    dat['address_id'] = address_id
    $.ajax({
        url: '/edit-address/',
        type: 'GET',
        data: dat,
        dataType: 'json',
        beforeSend: function () {
            section.classList.remove('not-visible')

        },
        success: function (data) {
            console.log(data.first_name)
            document.getElementById('firstName').value = data.first_name
            document.getElementById('lastName').value = data.last_name
            document.getElementById('phone').value = data.phone
            document.getElementById('street').value = data.street
            document.getElementById('house').value = data.building
            document.getElementById('city').value = data.city
            document.getElementById('landMark').value = data.landmark
            document.getElementById('state').value = data.state
            document.getElementById('country').value = data.country
            document.getElementById('pin').value = data.pin
            document.getElementById('ID').value = data.id
            
        }
    })
}

// Makes sure that validation is done when a customer chooses a new address and 
// avoids validation when customer selects an existing addresss

if (path.includes('checkout')){
    var selected = $('input[name="delivery-address"]:checked').val();
    if (selected == 'add_new'){
        $('#addressForm').removeAttr('novalidate')
    }
    var radio = $('input[name="delivery-address"]')
    console.log(radio)
    radio.change(function(){
        console.log('changed')
        selected = $('input[name="delivery-address"]:checked').val();
        console.log(selected)
        if (selected != 'add_new'){
            $('#addressForm').attr('novalidate',true)
        }
        else{
            $('#addressForm').removeAttr('novalidate')
        }
    })
    console.log(selected)
 
}


// apply coupon

function applyCoupon(order_id){
    var coupon_code = $('#couponCode').val()
    console.log(order_id)
    code = {'coupon_code':coupon_code,'order_id':order_id}
    $.ajax({
        url: '/apply-coupon/',
        type: 'GET',
        data: code,
        dataType: 'json',
        success: function (res) {
            if ('expired' in res){  
                document.getElementById('couponError').innerHTML = "The coupon code you entered has been expired"
            }
            else if('none' in res) {
                document.getElementById('couponError').innerHTML = "The coupon code you entered does not exist"
            }
            else if('applied' in res) {
                document.getElementById('couponError').innerHTML = "You have already used this coupon"
            }
            else{
            document.getElementById('couponError').innerHTML = ""
            document.getElementById('total').innerHTML = '₹ '+res.order_total+'.00';
            document.getElementById('code').classList.remove('not-visible');
            document.getElementById('coupon').innerHTML = res.coupon_code;
            document.getElementById('couponDiscount').classList.remove('not-visible');
            document.getElementById('discount').innerHTML = '₹ '+res.coupon_discount+'.00';
            location.reload()
        }
        }
    })
}


// crop profile picture

if (path.includes('profile')) {
    var imageBox = document.getElementById('image-box')
    var confirmBtn = document.getElementById('confirm-btn')
    var input = document.getElementById('id_image')
    var cropped = document.getElementById('cropped')
    var updateBtn = document.getElementById('update-dp')
    var allowedExtensions = /(\.jpg|\.jpeg|\.png)$/i;


    input.addEventListener('change', () => {
        if (!allowedExtensions.exec(input.value)) {
            alert('Invalid file type');
            input.value = '';
            cropped.src = '';
            confirmBtn.classList.add('not-visible')
            imageBox.classList.add('not-visible')
            updateBtn.classList.add('not-visible')

        }
        else {

            confirmBtn.classList.remove('not-visible')
            imageBox.classList.remove('not-visible')
            cropped.src = ''
            updateBtn.classList.add('not-visible')

            var img_data = input.files[0]
            var url = URL.createObjectURL(img_data)
            imageBox.innerHTML = `<img src="${url}" id="image" width="500px">`

            var $image = $('#image');



            $image.cropper({
                aspectRatio: 1 / 1,
                crop: function (event) {
                    console.log(event.detail.x);
                    console.log(event.detail.y);
                    console.log(event.detail.width);
                    console.log(event.detail.height);
                    console.log(event.detail.rotate);
                    console.log(event.detail.scaleX);
                    console.log(event.detail.scaleY);
                }
            });

            // Get the Cropper.js instance after initialized
            var cropper = $image.data('cropper');

            confirmBtn.addEventListener('click', () => {
                cropper.getCroppedCanvas().toBlob((blob) => {
                    let fileInputElement = document.getElementById('id_image');
                    let file = new File([blob], img_data.name, { type: "image/*", lastModified: new Date().getTime() });
                    let container = new DataTransfer();
                    container.items.add(file);
                    fileInputElement.files = container.files;

                    var reader = new FileReader();
                    reader.onload = function (e) {
                        cropped.src = e.target.result
                    }
                    reader.readAsDataURL(input.files[0]);
                    imageBox.classList.add('not-visible');
                    $('#image').attr("src", "");
                    confirmBtn.classList.add('not-visible');
                    updateBtn.classList.remove('not-visible')


                })
            })
        }
    })
}

// validate password update form

$('#passwordForm').validate({
    rules: {
        new_password: {
            minlength: 6
        },

        password_confirm: {
            minlength: 6,
            equalTo: "#newPassword"
        },
    },

    errorPlacement: function (error, element) {
        element.css('background', 'none');
        error.css('background', 'none');
        error.insertAfter(element);
    }
});


// validate address form

$('#addressForm').validate({
    rules: {
        first_name: {
            minlength: 4,
            required: true,
        },

        last_name: {
            minlength: 1,
            required: true,
        },
        phone: {
            minlength: 10,
            maxlength: 10,
            required: true,
            number: true,
            digits: true,

        },
        email: {
            email:true,
            required: true,
        },
        state: {
            minlength: 3,
            required: true,
        },
        street: {
            minlength: 5,
            required: true,
        },
        city: {
            minlength: 3,
            required: true,
        },
        pin: {
            minlength: 6,
            maxlength:6,
            number: true,
            digits: true,
            required: true,
        },
    },

    errorPlacement: function (error, element) {
        element.css('background', 'none');
        error.css('background', 'none');
        error.insertAfter(element);
    }
});


// image zoom

if (path.includes('product')){
    var image = document.querySelector('#image')

    image.addEventListener('mousemove', function(e){
        let width = image.offsetWidth;
        let height = image.offsetHeight;
        let mouseX = e.offsetX;
        let mouseY = e.offsetY;

        let bgPosX = (mouseX / width * 100);
        let bgPosY = (mouseY / height * 100);

        image.style.backgroundPosition = `${bgPosX}% ${bgPosY}%`;

    });

    image.addEventListener('mouseleave',function(){
        image.style.backgroundPosition = 'center';
    });

    var image1 = document.querySelector('#image1');
    var image2 = document.querySelector('#image2');
    var image3 = document.querySelector('#image3');
    var image4 = document.querySelector('#image4');
    var image_1_big = document.querySelector('#image1Big')
    var image_2_big = document.querySelector('#image2Big')
    var image_3_big = document.querySelector('#image3Big')
    var image_4_big = document.querySelector('#image4Big')

    image1.addEventListener('mouseover',function(){
        var imgsrc = image_1_big.src;
        image.style.backgroundImage = `url(${imgsrc})`;
        image1.classList.add('img-border')
        image2.classList.remove('img-border')
        image3.classList.remove('img-border')
        image4.classList.remove('img-border')
    })
    image2.addEventListener('mouseover',function(){
        var imgsrc = image_2_big.src;
        image.style.backgroundImage = `url(${imgsrc})`;
        image1.classList.remove('img-border')
        image2.classList.add('img-border')
        image3.classList.remove('img-border')
        image4.classList.remove('img-border')
    })
    image3.addEventListener('mouseover',function(){
        var imgsrc = image_3_big.src;
        image.style.backgroundImage = `url(${imgsrc})`;
        image1.classList.remove('img-border')
        image2.classList.remove('img-border')
        image3.classList.add('img-border')
        image4.classList.remove('img-border')
    })
    image4.addEventListener('mouseover',function(){
        var imgsrc = image_4_big.src;
        image.style.backgroundImage = `url(${imgsrc})`;
        image1.classList.remove('img-border')
        image2.classList.remove('img-border')
        image3.classList.remove('img-border')
        image4.classList.add('img-border')
    })



}
