// File Upload
// 
// $(document).ready(function(){
//   console.log('WINDOW READY FROM IMAGE UPLOAD JS')
//   $('#cancel_upload').on('click', function(){
//     resetFileUpload();
//   })
// })

// function ekUpload(){
//     function Init() {
  
//       console.log("Upload Initialised");
  
//       var fileSelect    = document.getElementById('file-upload'),
//           fileDrag      = document.getElementById('file-drag'),
//           submitButton  = document.getElementById('submit-button');
  
//       fileSelect.addEventListener('change', fileSelectHandler, false);
  
//       // Is XHR2 available?
//       var xhr = new XMLHttpRequest();
//       if (xhr.upload) {
//         // File Drop
//         fileDrag.addEventListener('dragover', fileDragHover, false);
//         fileDrag.addEventListener('dragleave', fileDragHover, false);
//         fileDrag.addEventListener('drop', fileSelectHandler, false);
//       }
//     }
  
//     function fileDragHover(e) {
//       var fileDrag = document.getElementById('file-drag');
  
//       e.stopPropagation();
//       e.preventDefault();
  
//       fileDrag.className = (e.type === 'dragover' ? 'hover' : 'modal-body file-upload');
//     }
  
//     function fileSelectHandler(e) {
//       // Fetch FileList object
//       var files = e.target.files || e.dataTransfer.files;
  
//       // Cancel event and hover styling
//       fileDragHover(e);
  
//       // Process all File objects
//       for (var i = 0, f; f = files[i]; i++) {
//         parseFile(f);
//         uploadFile(f);
//       }
//     }
  
//     // Output
//     function output(msg) {
//       // Response
//       var m = document.getElementById('messages');
//       m.innerHTML = msg;
//     }
  
//     function parseFile(file) {
  
//       console.log(file.name);
//       output(
//         '<strong>' + encodeURI(file.name) + '</strong>'
//       );
      
//       // var fileType = file.type;
//       // console.log(fileType);
//       var imageName = file.name;
  
//       var isGood = (/\.(?=gif|jpg|png|jpeg)/gi).test(imageName);
//       if (isGood) {
//         document.getElementById('start').classList.add("hidden");
//         document.getElementById('response').classList.remove("hidden");
//         document.getElementById('notimage').classList.add("hidden");
//         // Thumbnail Preview
//         document.getElementById('file-image').classList.remove("hidden");
//         document.getElementById('file-image').src = URL.createObjectURL(file);
//       }
//       else {
//         document.getElementById('file-image').classList.add("hidden");
//         document.getElementById('notimage').classList.remove("hidden");
//         document.getElementById('start').classList.remove("hidden");
//         document.getElementById('response').classList.add("hidden");
//         document.getElementById("file-upload-form").reset();
//       }
//     }
  
//     function setProgressMaxValue(e) {
//       var pBar = document.getElementById('file-progress');
  
//       if (e.lengthComputable) {
//         pBar.max = e.total;
//       }
//     }
  
//     function updateFileProgress(e) {
//       var pBar = document.getElementById('file-progress');
  
//       if (e.lengthComputable) {
//         pBar.value = e.loaded;
//       }
//     }
  
//     function uploadFile(file) {
  
//       var xhr = new XMLHttpRequest(),
//         fileInput = document.getElementById('class-roster-file'),
//         pBar = document.getElementById('file-progress'),
//         fileSizeLimit = 1024; // In MB
//       if (xhr.upload) {
//         // Check if file is less than x MB
//         if (file.size <= fileSizeLimit * 1024 * 1024) {
//           // Progress bar
//           pBar.style.display = 'inline';
//           xhr.upload.addEventListener('loadstart', setProgressMaxValue, false);
//           xhr.upload.addEventListener('progress', updateFileProgress, false);
  
//           // File received / failed
//           xhr.onreadystatechange = function(e) {
//             if (xhr.readyState == 4) {
//               // Everything is good!
  
//               // progress.className = (xhr.status == 200 ? "success" : "failure");
//               // document.location.reload(true);
//             }
//           };
  
//           // Start upload
//           xhr.open('POST', document.getElementById('file-upload-form').action, true);
//           xhr.setRequestHeader('X-File-Name', file.name);
//           xhr.setRequestHeader('X-File-Size', file.size);
//           xhr.setRequestHeader('Content-Type', 'multipart/form-data');
//           xhr.send(file);
//         } else {
//           output('Please upload a smaller file (< ' + fileSizeLimit + ' MB).');
//         }
//       }
//     }
  
//     // Check for the various File API support.
//     if (window.File && window.FileList && window.FileReader) {
//       Init();
//     } else {
//       document.getElementById('file-drag').style.display = 'none';
//     }
//   }
//   ekUpload();

// function resetFileUpload(){
//   $('#file-drag').removeClass('modal-body');
//   $('#file-image').attr('src', '');
//   $('#file-image').addClass('hidden');
//   $('#start').removeClass('hidden');
//   $('#response').addClass('hidden');
//   $('#messages').empty();
// }

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