function draw() {
    var step1_x = $("#picStep1_x").val();
    var step1_y = $("#picStep1_y").val();
    var step2_x = $("#picStep2_x").val();
    var step2_y = $("#picStep2_y").val();
    var step3_x = $("#picStep3_x").val();
    var step3_y = $("#picStep3_y").val();
    var step4_x = $("#picStep4_x").val();
    var step4_y = $("#picStep4_y").val();
    var step5_x = $("#picStep5_x").val();
    var step5_y = $("#picStep5_y").val();
    var step6_x = $("#picStep6_x").val();
    var step6_y = $("#picStep6_y").val();
    var step7_x = $("#picStep7_x").val();
    var step7_y = $("#picStep7_y").val();
    var step8_1_x = $("#picStep8_1_x").val();
    var step8_1_y = $("#picStep8_1_y").val();
    var step8_2_x = $("#picStep8_2_x").val();
    var step8_2_y = $("#picStep8_2_y").val();
    var step8_3_x = $("#picStep8_3_x").val();
    var step8_3_y = $("#picStep8_3_y").val();
    var step8_4_x = $("#picStep8_4_x").val();
    var step8_4_y = $("#picStep8_4_y").val();
    var step8_5_x = $("#picStep8_5_x").val();
    var step8_5_y = $("#picStep8_5_y").val();
    var step9_x = $("#picStep9_x").val();
    var step9_y = $("#picStep9_y").val();
//    alert(step1_y);

//    第一步
    var canvas1 = document.getElementById("canvas1");
    if (canvas1.getContext) {
        var ctx = canvas1.getContext("2d");

        var img = new Image();   // 创建一个<img>元素
        img.onload = function(){
            // 执行drawImage语句
            ctx.scale(0.5, 0.5);
            ctx.drawImage(img,0,0);
            ctx.beginPath();
            ctx.moveTo(step1_x,step1_y);
            ctx.lineTo(step2_x,step2_y);
            ctx.lineTo(step3_x,step3_y);
            ctx.lineTo(step4_x,step4_y);
            ctx.strokeStyle = "blue";
            ctx.lineWidth = 4;
            ctx.stroke();
        };
        img.src = '/static/images/img-front.png'; // 设置图片源地址
    }

//    第二步
    var canvas2 = document.getElementById("canvas2");
    if (canvas2.getContext) {
        var ctx2 = canvas2.getContext("2d");

        var img2 = new Image();   // 创建一个<img>元素
        img2.onload = function(){
            // 执行drawImage语句
            ctx2.scale(0.5, 0.5);
            ctx2.drawImage(img2,0,0);
            ctx2.beginPath();
            ctx2.moveTo(step5_x,step5_y);
            ctx2.lineTo(step6_x,step6_y);
            ctx2.lineTo(550,2930)
            ctx2.lineTo(step7_x,step7_y); //(650,2930)
            if (step8_1_x != ''){
                ctx2.lineTo(step8_1_x,step8_1_y);
                ctx2.lineTo(step8_2_x,step8_2_y);
                ctx2.lineTo(step8_3_x,step8_3_y);
                ctx2.lineTo(step8_4_x,step8_4_y);
                ctx2.lineTo(step8_5_x,step8_5_y);
            }
            else if (step8_1_x == ''){
                ctx2.lineTo(step8_5_x,step8_5_y); //(670,)
                ctx2.lineTo(step8_5_x-140,step8_5_y); //(530,)
                ctx2.lineTo(530,2950) //(530,2950)
                //如果不是最后一块多2步
                if (step9_x != 230){
                    ctx2.lineTo(670,2950) //(530,2950)
                }
                ctx2.lineTo(step9_x,step9_y);
                if (step9_x != 230){
                    ctx2.lineTo(240,step9_y)
                }
            }
//            ctx2.lineTo(650,2400);
            ctx2.strokeStyle = "blue";
            ctx2.lineWidth = 4;
            ctx2.stroke();
        };
        img2.src = '/static/images/img-side.png'; // 设置图片源地址
    }
}