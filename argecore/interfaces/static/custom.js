/*!
  * BURAK TOZ
  * Copyright
  * Licensed under MIT
  */



// // Form resetleme
$('#matModal').on('hidden.bs.modal', function (e) {
    $('#formMat').trigger("reset");
});
//
// $('#diverterModal').on('hidden.bs.modal', function (e) {
//     $('#formDiverter').trigger("reset");
// });
//
// $('#rcpModal').on('hidden.bs.modal', function (e) {
//     $('#formRcp').trigger("reset");
// });
//
// $('#rcpInputModal').on('hidden.bs.modal', function (e) {
//     $('#formRcpInput').trigger("reset");
// });
//
// $('#rcpOutputModal').on('hidden.bs.modal', function (e) {
//     $('#formRcpOutput').trigger("reset");
// });

$('#productOrdModal').on('hidden.bs.modal', function (e) {
    $('#formProductOrd').trigger("reset");
});


$('#mixOrdModal').on('hidden.bs.modal', function (e) {
    $('#formMixOrd').trigger("reset");
});

//. Form resetleme


function check(id) {
    document.getElementById(id).checked = true;
}

function uncheck(id) {
    document.getElementById(id).checked = false;
}


function removeOptions(selectElement) {
   var i, L = selectElement.options.length - 1;
   for(i = L; i >= 0; i--) {
      selectElement.remove(i);
   }
}

// using the function:
