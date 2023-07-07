$(document).ready(function (e) {
  function enterContainer() {
    $('#upload-container').addClass('bg-accent');
    $('#upload-container').removeClass('text-accent');
    $('#browse-file').addClass('btn-neutral');
    $('#browse-file').removeClass('btn-accent');
  }

  function leaveContainer() {
    $('#upload-container').addClass('text-accent');
    $('#upload-container').removeClass('bg-accent');
    $('#browse-file').addClass('btn-accent');
    $('#browse-file').removeClass('btn-neutral');
  }

  $('#upload-container').on('dragenter', function (e) {
    e.preventDefault();
    e.stopPropagation();
    enterContainer();
  });

  $('#upload-container').on('dragleave', function (e) {
    e.preventDefault();
    e.stopPropagation();
    leaveContainer();
  });

  $('#upload-container').on('dragover', function (e) {
    e.preventDefault();
    e.stopPropagation();
    enterContainer();
  });

  function displayFile(fileName) {
    $('#drop-file-cmd').addClass('hidden');
    $('#file-name').html(fileName);
    $('#error-file').addClass('hidden');

    $('#remove-file').removeClass('hidden');
    $('#submit-file').removeClass('hidden');
  }

  $('#upload-container').on('drop', function (e) {
    e.preventDefault();
    e.stopPropagation();

    const draggedData = e.originalEvent.dataTransfer;
    const files = draggedData.files;

    const arrLenFile = files[0].name.split('.').length;

    const fileFormat = files[0].name.split('.')[arrLenFile - 1];

    switch (fileFormat) {
      case 'webp':
        $('#webp-icon').removeClass('hidden');
        break;
      case 'png':
        $('#png-icon').removeClass('hidden');
        break;
      case 'jpeg':
      case 'jpg':
        $('#jpg-icon').removeClass('hidden');
        break;
      default:
        $('#error-file').removeClass('hidden');
        leaveContainer();
        return;
    }

    displayFile(files[0].name);
  });

  $('#upload-file').on('change', function (e) {
    e.preventDefault();
    e.stopPropagation();

    const file = this.files[0];

    const arrLenFile = file.name.split('.').length;

    const fileFormat = file.name.split('.')[arrLenFile - 1];
    switch (fileFormat) {
      case 'webp':
        $('#webp-icon').removeClass('hidden');
        break;
      case 'png':
        $('#png-icon').removeClass('hidden');
        break;
      case 'jpeg':
      case 'jpg':
        $('#jpg-icon').removeClass('hidden');
        break;
      default:
        $('#error-file').removeClass('hidden');
        leaveContainer();
        return;
    }

    displayFile(file.name);

    enterContainer();
  });

  function hideIcon() {
    $('#jpg-icon').addClass('hidden');
    $('#webp-icon').addClass('hidden');
    $('#png-icon').addClass('hidden');
  }

  $('#remove-file').click(function (e) {
    $('#remove-file').addClass('hidden');
    $('#submit-file').addClass('hidden');

    $('#drop-file-cmd').removeClass('hidden');
    $('#file-name').html('');
    $('#next-btn').attr('disabled', '');
    leaveContainer();
    hideIcon();
  });

  $('#submit-file').click(function (e) {
    e.preventDefault();
    $('#next-btn').removeAttr('disabled');

    const formData = new FormData($('#form-file-upload')[0]);

    $('#loading-setup').removeClass('hidden');

    $('#image-input').addClass('hidden');

    $.ajax({
      method: 'POST',
      url: '/',
      data: formData,
      dataType: 'json',
      cache: false,
      contentType: false,
      processData: false,
      success: function (data) {
        $('#image-input').removeClass('hidden');
        $('#original-fire-image').attr('src', data.image_uri);
        if (data.fire_percentage < 0.1) {
          $('#fire-percentage').html('below 10%');
          $('#warning-msg').removeClass('hidden');
          $('#fire-percentage').addClass('text-error');
        } else {
          $('#fire-percentage').html(`${parseInt(data.fire_percentage * 100)}%`);
          $('#procceed-btn').removeClass('hidden');
        }
      },
      complete: function () {
        $('#loading-setup').addClass('hidden');
      },
    });
  });

  $('.procceed-btn').click(function (e) {
    const formData = new FormData($('#form-file-upload')[0]);

    $('#output').addClass('hidden');

    $('#loading-proccess').removeClass('hidden');

    $.ajax({
      method: 'POST',
      url: '/process_image',
      data: formData,
      dataType: 'json',
      cache: false,
      contentType: false,
      processData: false,
      success: function (data) {
        $('#output').removeClass('hidden');
        $('#output-image').attr('src', data.image_uri);
      },
      complete: function () {
        $('#loading-proccess').addClass('hidden');
      },
    });
  });
});
