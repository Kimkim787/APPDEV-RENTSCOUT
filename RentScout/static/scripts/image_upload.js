function ekUploadRoomPhoto() {
  function InitRoomPhoto() {
    console.log('Room Photo Upload Initialized');

    // File input and drag-drop area
    const fileSelect = document.getElementById('room-photo-upload');
    const fileDrag = document.getElementById('room-file-drag');

    // Add event listeners
    fileSelect.addEventListener('change', fileSelectHandlerRoomPhoto, false);

    const xhr = new XMLHttpRequest();
    if (xhr.upload) {
      fileDrag.addEventListener('dragover', fileDragHoverRoomPhoto, false);
      fileDrag.addEventListener('dragleave', fileDragHoverRoomPhoto, false);
      fileDrag.addEventListener('drop', fileSelectHandlerRoomPhoto, false);
    }
  }

  function fileDragHoverRoomPhoto(e) {
    e.stopPropagation();
    e.preventDefault();
    const fileDrag = document.getElementById('room-file-drag');
    fileDrag.className =
      e.type === 'dragover' ? 'hover' : 'modal-body file-upload';
  }

  function fileSelectHandlerRoomPhoto(e) {
    // Handle selected or dropped files
    const files = e.target.files || e.dataTransfer.files;

    // Cancel drag hover styling
    fileDragHoverRoomPhoto(e);

    // Process each file
    Array.from(files).forEach((file) => parseFileRoomPhoto(file));
  }

  function parseFileRoomPhoto(file) {
    console.log('Room Photo File selected:', file.name);
    const isImage = /\.(gif|jpg|jpeg|png)$/i.test(file.name);

    if (isImage) {
      // Update UI for valid file
      $('#room-start').addClass('hidden');
      $('#room-response').removeClass('hidden');
      $('#room-notimage').addClass('hidden');
      $('#room-image-preview')
        .removeClass('hidden')
        .attr('src', URL.createObjectURL(file));
    } else {
      // Reset UI for invalid file
      $('#room-image-preview').addClass('hidden');
      $('#room-notimage').removeClass('hidden');
      $('#room-start').removeClass('hidden');
      $('#room-response').addClass('hidden');
      $('#room-photo-upload-form')[0].reset();
    }
  }

  if (window.File && window.FileList && window.FileReader) {
    InitRoomPhoto();
  } else {
    $('#room-file-drag').hide();
    console.error('File APIs are not fully supported in this browser.');
  }
}

function resetFileUploadRoomPhoto() {
  // Reset file upload UI
  $('#room-file-drag').removeClass('modal-body');
  $('#room-image-preview')
    .attr('src', '')
    .addClass('hidden');
  $('#room-start').removeClass('hidden');
  $('#room-response').addClass('hidden');
  $('#room-messages').empty();
  $('#room-photo-upload-form')[0].reset();
}
ekUploadRoomPhoto();

// --------------------------------------------------


function ekUpload2() {
  function Init2() {
    console.log('Certificate Upload Initialized');

    // File input and drag-drop area
    const fileSelect = document.getElementById('certificate-upload');
    const fileDrag = document.getElementById('file-drag2');

    // Add event listeners
    fileSelect.addEventListener('change', fileSelectHandler2, false);

    const xhr = new XMLHttpRequest();
    if (xhr.upload) {
      fileDrag.addEventListener('dragover', fileDragHover2, false);
      fileDrag.addEventListener('dragleave', fileDragHover2, false);
      fileDrag.addEventListener('drop', fileSelectHandler2, false);
    }
  }

  function fileDragHover2(e) {
    e.stopPropagation();
    e.preventDefault();
    const fileDrag = document.getElementById('file-drag2');
    fileDrag.className =
      e.type === 'dragover' ? 'hover' : 'modal-body file-upload';
  }

  function fileSelectHandler2(e) {
    // Handle selected or dropped files
    const files = e.target.files || e.dataTransfer.files;

    // Cancel drag hover styling
    fileDragHover2(e);

    // Process each file
    Array.from(files).forEach((file) => parseFile2(file));
  }

  function parseFile2(file) {
    console.log('Certificate File selected:', file.name);
    const isImage = /\.(gif|jpg|jpeg|png)$/i.test(file.name);

    if (isImage) {
      // Update UI for valid file
      $('#start2').addClass('hidden');
      $('#response2').removeClass('hidden');
      $('#notimage2').addClass('hidden');
      $('#certificate-image')
        .removeClass('hidden')
        .attr('src', URL.createObjectURL(file));
    } else {
      // Reset UI for invalid file
      $('#certificate-image').addClass('hidden');
      $('#notimage2').removeClass('hidden');
      $('#start2').removeClass('hidden');
      $('#response2').addClass('hidden');
      $('#certificate-upload-form')[0].reset();
    }
  }

  if (window.File && window.FileList && window.FileReader) {
    Init2();
  } else {
    $('#file-drag2').hide();
    console.error('File APIs are not fully supported in this browser.');
  }
}

ekUpload2();

function resetFileUpload2() {
  // Reset file upload UI
  $('#file-drag2').removeClass('modal-body');
  $('#certificate-image')
    .attr('src', '')
    .addClass('hidden');
  $('#start2').removeClass('hidden');
  $('#response2').addClass('hidden');
  $('#messages2').empty();
  $('#certificate-upload-form')[0].reset();
}