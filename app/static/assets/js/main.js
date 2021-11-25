$(function () {
    $("#show-password button").on('click', function (e) {
        e.preventDefault();
        if ($('#show-password input').attr("type") == "password") {
            $('#show-password input').attr('type', 'text');
            $('#show-password i').addClass("bi-eye-slash-fill");
            $('#show-password i').removeClass("bi-eye-fill");
        } else {
            $('#show-password input').attr('type', 'password');
            $('#show-password i').removeClass("bi-eye-slash-fill");
            $('#show-password i').addClass("bi-eye-fill");
        }
    });

    $("#form-upload").on('submit', function () {
        fetch("classify-flower", {
                method: "POST"
            })
            .then(function (res) {
                res.json()
            })
            .then(function (data) {
                console.log(data);
            })
            .catch(function (e) {
                console.log(e);
            });
    })
});