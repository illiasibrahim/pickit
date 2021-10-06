$(document).ready(function () {
  $("#search-input").on("keyup", function () {
    var value = $(this).val().toLowerCase();
    $("#data-table tbody tr").filter(function () {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });


  // admin form validations
  $('#inputForm').validate()

  var path = window.location.href;
  console.log(path)

  // cropping and validating images on uploading banners 

  if (path.includes('add-banner') || path.includes('edit-banner') || path.includes('add-poster') || path.includes('edit-poster') || path.includes('add-category') || path.includes('edit-category')) {
    var imageBox = document.getElementById('image-box')
    var confirmBtn = document.getElementById('confirm-btn')
    var input = document.getElementById('id_image')
    var cropped = document.getElementById('cropped')
    var allowedExtensions = /(\.jpg|\.jpeg|\.png)$/i;
    var addBtn = document.getElementById('addBtn')
    input.addEventListener('change', () => {
      if (!allowedExtensions.exec(input.value)) {
        alert('Invalid file type');
        input.value = '';
        cropped.src = '';
        confirmBtn.classList.add('not-visible')
        imageBox.classList.add('not-visible')

      }
      else {
        var size = parseFloat(input.files[0].size / 1024).toFixed(2);
        if (size > 200) {
          alert('Please choose an image of size less than 200KB')
          input.value = '';
          cropped.src = '';
          confirmBtn.classList.add('not-visible')
          imageBox.classList.add('not-visible')
        }
        else {
          addBtn.setAttribute("disabled", true)
          confirmBtn.classList.remove('not-visible')
          imageBox.classList.remove('not-visible')
          cropped.src = ''

          var img_data = input.files[0]
          var url = URL.createObjectURL(img_data)
          imageBox.innerHTML = `<img src="${url}" id="image" width="500px">`

          var $image = $('#image');

          if (path.includes('add-banner')) {
            // aspect_ratio = 21 / 4;
            aspect_ratio = 21 / 5;
          }
          else if (path.includes('edit-banner')) {
            aspect_ratio = 21 / 5;
            // aspect_ratio = 21 / 4;
          }
          else if (path.includes('add-poster')) {
            aspect_ratio = 12 / 7;
          }
          else if (path.includes('edit-poster')) {
            aspect_ratio = 12 / 7;
          }
          else if (path.includes('add-category')) {
            aspect_ratio = 1 / 1;
          }
          else if (path.includes('edit-category')) {
            aspect_ratio = 1 / 1;
          }

          $image.cropper({
            aspectRatio: aspect_ratio,
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
              confirmBtn.classList.add('not-visible')
              imageBox.classList.add('not-visible')
              addBtn.removeAttribute('disabled')
            }, "image/jpeg", 0.75);  // mime=JPEG, quality=0.75 quality control
          })
        }
      }
    })
  }
  else if (path.includes('add-product') || path.includes('edit-product')) {
    // // cropping and validating images on uploading products

    var imageBox = document.getElementById('image-box')
    var confirmBtn = document.getElementById('confirm-btn')
    var input1 = document.getElementById('id_image_1')
    var input2 = document.getElementById('id_image_2')
    var input3 = document.getElementById('id_image_3')
    var input4 = document.getElementById('id_image_4')
    var cropped1 = document.getElementById('cropped1')
    var cropped2 = document.getElementById('cropped2')
    var cropped3 = document.getElementById('cropped3')
    var cropped4 = document.getElementById('cropped4')
    var allowedExtensions = /(\.jpg|\.jpeg|\.png)$/i;
    var addBtn = document.getElementById('addBtn')

    input1.addEventListener('change', () => {
      if (!allowedExtensions.exec(input1.value)) {
        alert('Invalid file type');
        input1.value = '';
        cropped1.src = '';
        confirmBtn.classList.add('not-visible')
        imageBox.classList.add('not-visible')

      }
      else {
        var size = parseFloat(input1.files[0].size / 1024).toFixed(2);
        if (size > 200) {
          alert('Please choose an image of size less than 200KB')
          input1.value = '';
          cropped1.src = '';
          confirmBtn.classList.add('not-visible')
          imageBox.classList.add('not-visible')
        }
        else {
        addBtn.setAttribute('disabled', true)
        input2.setAttribute('disabled', true)
        input3.setAttribute('disabled', true)
        input4.setAttribute('disabled', true)
        confirmBtn.classList.remove('not-visible')
        imageBox.classList.remove('not-visible')
        cropped1.src = ''

        var img_data = input1.files[0]
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
            let fileInputElement = document.getElementById('id_image_1');
            let file = new File([blob], img_data.name, { type: "image/*", lastModified: new Date().getTime() });
            let container = new DataTransfer();
            container.items.add(file);
            fileInputElement.files = container.files;

            var reader = new FileReader();
            reader.onload = function (e) {
              cropped1.src = e.target.result
            }
            reader.readAsDataURL(input1.files[0]);
            confirmBtn.classList.add('not-visible')
            imageBox.classList.add('not-visible')
            addBtn.removeAttribute('disabled')
            input2.removeAttribute('disabled')
            input3.removeAttribute('disabled')
            input4.removeAttribute('disabled')

          }, "image/jpeg", 0.75);
        })
      }
    }
    })
    // second image

    input2.addEventListener('change', () => {
      if (!allowedExtensions.exec(input2.value)) {
        alert('Invalid file type');
        input2.value = '';
        cropped2.src = '';
        confirmBtn.classList.add('not-visible')
        imageBox.classList.add('not-visible')

      }
      else {
        var size = parseFloat(input2.files[0].size / 1024).toFixed(2);
        if (size > 200) {
          alert('Please choose an image of size less than 200KB')
          input2.value = '';
          cropped2.src = '';
          confirmBtn.classList.add('not-visible')
          imageBox.classList.add('not-visible')
        }
        else {
        addBtn.setAttribute('disabled', true)
        input1.setAttribute('disabled', true)
        input3.setAttribute('disabled', true)
        input4.setAttribute('disabled', true)
        confirmBtn.classList.remove('not-visible')
        imageBox.classList.remove('not-visible')
        cropped2.src = ''

        var img_data = input2.files[0]
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
            let fileInputElement = document.getElementById('id_image_2');
            let file = new File([blob], img_data.name, { type: "image/*", lastModified: new Date().getTime() });
            let container = new DataTransfer();
            container.items.add(file);
            fileInputElement.files = container.files;

            var reader = new FileReader();
            reader.onload = function (e) {
              cropped2.src = e.target.result
            }
            reader.readAsDataURL(input2.files[0]);
            confirmBtn.classList.add('not-visible')
            imageBox.classList.add('not-visible')
            addBtn.removeAttribute('disabled')
            input1.removeAttribute('disabled')
            input3.removeAttribute('disabled')
            input4.removeAttribute('disabled')

          })
        })
      }
    }
    })
    // third image 


    input3.addEventListener('change', () => {
      if (!allowedExtensions.exec(input3.value)) {
        alert('Invalid file type');
        input3.value = '';
        cropped3.src = '';
        confirmBtn.classList.add('not-visible')
        imageBox.classList.add('not-visible')

      }
      else {
        var size = parseFloat(input3.files[0].size / 1024).toFixed(2);
        if (size > 200) {
          alert('Please choose an image of size less than 200KB')
          input3.value = '';
          cropped3.src = '';
          confirmBtn.classList.add('not-visible')
          imageBox.classList.add('not-visible')
        }
        else {
        addBtn.setAttribute('disabled', true)
        input1.setAttribute('disabled', true)
        input2.setAttribute('disabled', true)
        input4.setAttribute('disabled', true)
        confirmBtn.classList.remove('not-visible')
        imageBox.classList.remove('not-visible')
        cropped3.src = ''

        var img_data = input3.files[0]
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
            let fileInputElement = document.getElementById('id_image_3');
            let file = new File([blob], img_data.name, { type: "image/*", lastModified: new Date().getTime() });
            let container = new DataTransfer();
            container.items.add(file);
            fileInputElement.files = container.files;

            var reader = new FileReader();
            reader.onload = function (e) {
              cropped3.src = e.target.result
            }
            reader.readAsDataURL(input3.files[0]);
            confirmBtn.classList.add('not-visible')
            imageBox.classList.add('not-visible')
            addBtn.removeAttribute('disabled')
            input1.removeAttribute('disabled')
            input2.removeAttribute('disabled')
            input4.removeAttribute('disabled')
          }, "image/jpeg", 0.75);
        })
      }
    }
    })
    // fourth image

    input4.addEventListener('change', () => {
      if (!allowedExtensions.exec(input4.value)) {
        alert('Invalid file type');
        input4.value = '';
        cropped4.src = '';
        confirmBtn.classList.add('not-visible')
        imageBox.classList.add('not-visible')

      }
      else {
        var size = parseFloat(input4.files[0].size / 1024).toFixed(2);
        if (size > 200) {
          alert('Please choose an image of size less than 200KB')
          input4.value = '';
          cropped4.src = '';
          confirmBtn.classList.add('not-visible')
          imageBox.classList.add('not-visible')
        }
        else {
        addBtn.setAttribute('disabled', true)
        input1.setAttribute('disabled', true)
        input2.setAttribute('disabled', true)
        input3.setAttribute('disabled', true)
        confirmBtn.classList.remove('not-visible')
        imageBox.classList.remove('not-visible')
        cropped4.src = ''

        var img_data = input4.files[0]
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
            let fileInputElement = document.getElementById('id_image_4');
            let file = new File([blob], img_data.name, { type: "image/*", lastModified: new Date().getTime() });
            let container = new DataTransfer();
            container.items.add(file);
            fileInputElement.files = container.files;

            var reader = new FileReader();
            reader.onload = function (e) {
              cropped4.src = e.target.result
            }
            reader.readAsDataURL(input4.files[0]);
            confirmBtn.classList.add('not-visible')
            imageBox.classList.add('not-visible')
            addBtn.removeAttribute('disabled')
            input1.removeAttribute('disabled')
            input2.removeAttribute('disabled')
            input3.removeAttribute('disabled')
          }, "image/jpeg", 0.75);
        })
      }
    }
    })
  }

});

// change order status

function approve(order_id) {
  dat = { 'order_id': order_id }
  $.ajax({
    url: '/admin/approve/',
    type: 'GET',
    data: dat,
    dataType: 'json',
    success: function (res) {
      document.getElementById(order_id).innerHTML = res.status
      document.getElementById(order_id).classList.remove('text-danger')

    }
  })
}
function dispatch(order_id) {
  dat = { 'order_id': order_id }
  $.ajax({
    url: '/admin/dispatch/',
    type: 'GET',
    data: dat,
    dataType: 'json',
    success: function (res) {
      document.getElementById(order_id).innerHTML = res.status
      document.getElementById(order_id).classList.remove('text-danger')

    }
  })
}
function deliver(order_id) {
  dat = { 'order_id': order_id }
  $.ajax({
    url: '/admin/deliver/',
    type: 'GET',
    data: dat,
    dataType: 'json',
    success: function (res) {
      document.getElementById(order_id).innerHTML = res.status
      document.getElementById(order_id).classList.remove('text-danger')
    }
  })
}
function reject(order_id) {
  dat = { 'order_id': order_id }
  $.ajax({
    url: '/admin/reject/',
    type: 'GET',
    data: dat,
    dataType: 'json',
    success: function (res) {
      document.getElementById(order_id).innerHTML = res.status
      document.getElementById(order_id).classList.add('text-danger')

    }
  })
}

function openUpdateCategoryOffer(cat_offer, cat_id, cat_name) {
  document.getElementById('catOffer').value = cat_offer
  document.getElementById('catId').value = cat_id
  document.getElementById('exampleModalLongTitle').innerHTML = cat_name
}

function updateCategoryOffer() {
  cat_offer = document.getElementById('catOffer').value
  cat_id = document.getElementById('catId').value
  dat = {
    'cat_id': cat_id,
    'cat_offer': cat_offer,
  }
  if (cat_offer < 100) {
    $.ajax({
      url: '/admin/update-category-offer/',
      type: 'GET',
      data: dat,
      dataType: 'json',
      success: function (res) {
        document.getElementById(cat_id).innerHTML = res.cat_offer + '%'
        if (res.cat_offer != 0) {
          document.getElementById('catoffer' + cat_id).classList.remove('not-visible')
        }
      }
    })
  }
}

function deleteCategoryOffer(cat_id) {
  dat = {
    'cat_id': cat_id,
  }
  choice = confirm('Are you sure you want to remove this offer?')
  if (choice) {
    $.ajax({
      url: '/admin/delete-category-offer/',
      type: 'GET',
      data: dat,
      dataType: 'json',
      success: function (res) {
        document.getElementById(cat_id).innerHTML = '0%'
        document.getElementById('catoffer' + cat_id).classList.add('not-visible')
      }
    })
  }
}


function changeCouponStatus(coupon_id) {
  console.log(coupon_id)
  dat = {
    'coupon_id': coupon_id,
  }
  $.ajax({
    url: '/admin/update-coupon-status/',
    type: 'GET',
    data: dat,
    dataType: 'json',
    beforeSend: function () {
      document.querySelectorAll(".trigger").forEach(e => e.disabled = true)
    },
    success: function (res) {
      document.querySelectorAll(".trigger").forEach(e => e.disabled = false)
    }
  })
}


function openUpdateProductOffer(pro_offer, pro_id, pro_name) {
  document.getElementById('productOffer').value = pro_offer;
  document.getElementById('productId').value = pro_id
  console.log(pro_id)
  document.getElementById('productTitle').innerHTML = pro_name
}

function updateProductOffer() {
  product_offer = document.getElementById('productOffer').value
  product_id = document.getElementById('productId').value
  dat = {
    'product_id': product_id,
    'product_offer': product_offer,
  }
  if (product_offer < 100) {
    $.ajax({
      url: '/admin/update-product-offer/',
      type: 'GET',
      data: dat,
      dataType: 'json',
      success: function (res) {
        document.getElementById('offer' + product_id).innerHTML = res.product_offer + '% off'
      }
    })
  }
}

function exportToLocal() {
  from_date = document.getElementById('fromDate').value
  to_date = document.getElementById('toDate').value
  file_type = document.getElementById('fileType').value
  if (from_date == "") {
    from_date = "2021-05-01"
  }
  if (to_date == "") {
    var to_date = new Date();
    var dd = String(to_date.getDate()).padStart(2, '0');
    var mm = String(to_date.getMonth() + 1).padStart(2, '0'); //January is 0!
    var yyyy = to_date.getFullYear();

    to_date = yyyy + '-' + mm + '-' + dd;
  }
  console.log(from_date)
  console.log(to_date)
  console.log(file_type)
  dat = {
    'from_date': from_date,
    'to_date': to_date,
    'file_type': file_type,
  }
  $.ajax({
    url: '/admin/export/',
    type: 'GET',
    data: dat,
    dataType: 'json',
    success: function (res) {
      console.log('success')
    }
  })
}


// validate add product form
$('#productForm').validate({
  rules: {
    product_name: {
      minlength: 3,
    },
    quantity: {
      maxlength: 7,
    },
    mrp: {
      number: true,
      digits: true,
    },
  },

  errorPlacement: function (error, element) {
    element.css('background', 'none');
    error.css('background', 'none');
    error.insertAfter(element);
  }
});


// validate product offer form
$('#productOfferForm').validate({
  rules: {
    offer: {
      number: true,
      digits: true,
      maxlength: 2,
    },
  },

  errorPlacement: function (error, element) {
    element.css('background', 'none');
    error.css('background', 'none');
    error.insertAfter(element);
  }
});

// validate category offer form
$('#catOfferForm').validate({
  rules: {
    offer: {
      number: true,
      digits: true,
      maxlength: 2,
    },
  },

  errorPlacement: function (error, element) {
    element.css('background', 'none');
    error.css('background', 'none');
    error.insertAfter(element);
  }
});


// validate category offer form
$('#couponForm').validate({
  rules: {
    discount: {
      number: true,
      digits: true,
      maxlength: 2,
    },
  },

  errorPlacement: function (error, element) {
    element.css('background', 'none');
    error.css('background', 'none');
    error.insertAfter(element);
  }
});

function changeBannerStatus(banner_id) {
  dat = {
    'banner_id': banner_id,
  }
  $.ajax({
    url: '/admin/update-banner-status/',
    type: 'GET',
    data: dat,
    dataType: 'json',
    beforeSend: function () {
      document.querySelectorAll(".trigger").forEach(e => e.disabled = true)
    },
    success: function (res) {
      document.querySelectorAll(".trigger").forEach(e => e.disabled = false)
    }
  })
}

function changePosterStatus(poster_id) {
  dat = {
    'poster_id': poster_id,
  }
  $.ajax({
    url: '/admin/update-poster-status/',
    type: 'GET',
    data: dat,
    dataType: 'json',
    beforeSend: function () {
      document.querySelectorAll(".trigger").forEach(e => e.disabled = true)
    },
    success: function (res) {
      document.querySelectorAll(".trigger").forEach(e => e.disabled = false)
    }
  })
}

function orderFrom() {
  from_date = document.getElementById('fromDate').value
  to_date = document.getElementById('toDate').value
  document.getElementById('fromError').classList.add('not-visible')
  if (to_date == "") {
    var to_date = new Date();
    var dd = String(to_date.getDate()).padStart(2, '0');
    var mm = String(to_date.getMonth() + 1).padStart(2, '0'); //January is 0!
    var yyyy = to_date.getFullYear();
    to_date = yyyy + '-' + mm + '-' + dd;
  }
  if (from_date == "") {
    from_date = "2021-05-01"
  }
  if (from_date > to_date) {
    document.getElementById('fromDate').value = ""
    from_date = ""
    document.getElementById('fromError').classList.remove('not-visible')
  }

  dat = {
    'from_date': from_date,
    'to_date': to_date,
  }
  if (from_date != "" && to_date != "") {
    $.ajax({
      url: '/admin/filter-order/',
      type: 'GET',
      data: dat,
      dataType: 'json',
      success: function (res) {
        window.location.href = '/admin/order/'
      }
    })
  }
}


function orderTo() {
  from_date = document.getElementById('fromDate').value
  to_date = document.getElementById('toDate').value
  document.getElementById('toError').classList.add('not-visible')
  if (from_date == "") {
    from_date = "2021-05-01"
  }
  var today = new Date();
  var dd = String(today.getDate()).padStart(2, '0');
  var mm = String(today.getMonth() + 1).padStart(2, '0');
  var yyyy = today.getFullYear();
  today = yyyy + '-' + mm + '-' + dd;
  if (to_date == "") {
    document.getElementById('toError').classList.add('not-visible')
    to_date = today
  }
  else {
    if (to_date > today) {
      document.getElementById('toDate').value = today
      to_date = today
    }
    if (to_date < from_date) {
      document.getElementById('toDate').value = ""
      to_date = ""
      document.getElementById('toError').classList.remove('not-visible')
    }
  }
  console.log(from_date)
  console.log(to_date)
  dat = {
    'from_date': from_date,
    'to_date': to_date,
  }
  if (from_date != "" && to_date != "") {
    $.ajax({
      url: '/admin/filter-order/',
      type: 'GET',
      data: dat,
      dataType: 'json',
      success: function (res) {
        window.location.href = '/admin/order/'
      }
    })
  }
}



function toClick() {
  var to = document.getElementById('toDate')
  var from = document.getElementById('fromDate').value
  var today = new Date();
  var dd = String(today.getDate()).padStart(2, '0');
  var mm = String(today.getMonth() + 1).padStart(2, '0');
  var yyyy = today.getFullYear();
  today = yyyy + '-' + mm + '-' + dd;
  to.setAttribute("max", today);
  to.setAttribute("min", from)
}

function fromClick() {
  var to = document.getElementById('toDate').value
  var from = document.getElementById('fromDate')
  from.setAttribute("max", to);
}

