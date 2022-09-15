function bindCaptchaBtnClick(){
    $("#captcha-btn").on("click",function (event){
        var $this = $(this);
        var email = $("input[name= 'email']").val();
        if (!email){
            alert("Please enter your email first")
            return;
        }
        $.ajax({
            url: "/user/captcha",
            method: "POST",
            data:{
                "email": email
            },
            success: function (res){
                var code = res['code']
                if (code === 200){
                    $this.off("click");
                    var countDown = 60;

                    var timer = setInterval(function (){
                        countDown -= 1
                        if (countDown > 0){
                            $this.text(countDown + "s")
                        }else{
                            $this.text("TestGetCode")
                            bindCaptchaBtnClick();
                            clearInterval(timer)
                        }

                    },1000)
                    alert("The verification code is sent successfully")

                }else{
                    alert(res['message'])
                }

            }

        })
    });


}

$(function (){
    bindCaptchaBtnClick();
});