$(document).ready(function (msg) {
    $("#login").click(function (event) {
        var name = $("#username").val();
        var pwd = $("#password").val();
        if (name == "") {
            alert("用户名不能为空！");
        } else if (pwd == "") {
            alert("密码不能为空！");
        } else if (pwd != "" && pwd.length < 3) {
            alert("密码不能小于位！");
        } else if (name != "" && pwd != "" && pwd.length >= 3) {
            if (name == "alex" && pwd == "123") {
                // alert("登录成功！");
                console.log("登录成功！！！")
            } else {
                // alert("用户名或密码错误！");
                console.log("用户名或密码错误")
                window.location.href = "../../../templates/login.html";
            }
        }
    });
    $("#reset").click(function (event) {
        $("#username").val("");
        $("#password").val("");
});
    $(".login-status").delay(2000).fadeOut();
});
