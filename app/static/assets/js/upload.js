$(function () {
    $('#profile').addClass('dragging').removeClass('dragging');
});

$('#profile').on('dragover', function () {
    $('#profile').addClass('dragging');
}).on('dragleave', function () {
    $('#profile').removeClass('dragging');
}).on('drop', function (e) {
    $('#profile').removeClass('dragging hasImage');

    if (e.originalEvent) {
        var file = e.originalEvent.dataTransfer.files[0];
        var fileName = file.name;
        var idxDot = fileName.lastIndexOf(".") + 1;
        var extFile = fileName.substr(idxDot, fileName.length).toLowerCase();

        if (extFile == "jpg" || extFile == "jpeg" || extFile == "png") {
            var reader = new FileReader();
            
            reader.readAsDataURL(file);
            reader.onload = function (e) {
                console.log(reader.result);
                $('#profile').css('background-image', 'url(' + reader.result + ')').addClass('hasImage');
            }
        } else {
            $("#modalMessageLabel").text("Aviso");
            $("#modal-text").text("┬íSolamente estan permitidos archivos jpg/jpeg y png!");
            $("#modal-message").modal('show');
        }
        

    }
})
$('#profile').on('click', function (e) {
    console.log('clicked')
    $('#mediaFile').click();
});
window.addEventListener("dragover", function (e) {
    e = e || event;
    e.preventDefault();
}, false);
window.addEventListener("drop", function (e) {
    e = e || event;
    e.preventDefault();
}, false);

$('#mediaFile').on("change", function (e) {
    var input = e.target;

    if (input.files && input.files[0]) {
        var file = input.files[0];
        var fileName = file.name;
        var idxDot = fileName.lastIndexOf(".") + 1;
        var extFile = fileName.substr(idxDot, fileName.length).toLowerCase();
        
        if (extFile == "jpg" || extFile == "jpeg" || extFile == "png") {
            var file = input.files[0];
            var reader = new FileReader();

            reader.readAsDataURL(file);
            reader.onload = function (e) {
                console.log(reader.result);
                $('#profile').css('background-image', 'url(' + reader.result + ')').addClass('hasImage');
            }
        } else {
            $("#modalMessageLabel").text("Aviso");
            $("#modal-text").text("┬íSolamente estan permitidos archivos jpg/jpeg y png!");
            $("#modal-message").modal('show');
        }
        
    }
});
