
$(document).ready(function(){
    // alert('jquery 확인');

    $("#upload").change(function(){
        // console.log('on change')
        readURL(this);
        uploadFile();
    });
});

var name = ""

function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
    
        reader.onload = function (e) {
        $("#image_section1").attr("src", e.target.result);
        $("#image_section2").attr("src", '');   
        }
    
        reader.readAsDataURL(input.files[0]);
    }
}

function uploadFile(){
    var form = $('#FILE_FORM')[0];
    var formData = new FormData(form);
    formData.append("fileObj", $("#upload")[0].files[0]);

    $.ajax({
            url: "upload/",
            processData: false,
            contentType: false,
            data: formData,
            type: 'POST',
            success: function(result){
                // alert("업로드 성공!!");
                // alert(result);
                name = result
            }
        });
}

function resultfunc(){
    
    $.ajax({
            url: "resultView/",
            // processData: false,
            contentType: false,
            data: {
                name: name,
            },
            type: 'GET',
            success: function(result){
                // alert("업로드 성공!!");
                // result = "/media/로고만.jpg"
                // alert(result);
                $("#image_section2").attr("src", result);  
            }
        });
}

