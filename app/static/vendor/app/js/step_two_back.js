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
    var step8_x = $("#picStep8_x").val();
    var step8_y = $("#picStep8_y").val();
    // var step8_1_x = $("#picStep8_1_x").val();
    // var step8_1_y = $("#picStep8_1_y").val();
    // var step8_2_x = $("#picStep8_2_x").val();
    // var step8_2_y = $("#picStep8_2_y").val();
    // var step8_3_x = $("#picStep8_3_x").val();
    // var step8_3_y = $("#picStep8_3_y").val();
    // var step8_4_x = $("#picStep8_4_x").val();
    // var step8_4_y = $("#picStep8_4_y").val();
    // var step8_5_x = $("#picStep8_5_x").val();
    // var step8_5_y = $("#picStep8_5_y").val();
    var step9_x = $("#picStep9_x").val();
    var step9_y = $("#picStep9_y").val();
    var step10_x = $("#picStep10_x").val();
    var step10_y = $("#picStep10_y").val();
    var step11_x = $("#picStep11_x").val();
    var step11_y = $("#picStep11_y").val();
    var step12_x = $("#picStep12_x").val();
    var step12_y = $("#picStep12_y").val();
    var step13_x = $("#picStep13_x").val();
    var step13_y = $("#picStep13_y").val();
    var from_name = $("#from_name").val();
    var to_name = $("#to_name").val();
   // alert(step1_y);

//    第一步
    var canvas1 = document.getElementById("canvas1");
    if (canvas1.getContext) {
        var ctx = canvas1.getContext("2d");

        var img = new Image();   // 创建一个<img>元素
        img.onload = function(){
            // 执行drawImage语句
            ctx.scale(0.5, 0.5);
            ctx.drawImage(img,0,0);
            ctx.font = "54px serif";
            ctx.fillStyle = 'red';
            ctx.fillText(from_name, 370, 70);
            ctx.beginPath();
            ctx.moveTo(step1_x,step1_y);
            ctx.fillText("1", Number(step1_x)+20, Number(step1_y)+20);
            ctx.lineTo(Number(step2_x)+25,step2_y);
            ctx.arc(Number(step2_x)+25, Number(step2_y)+25, 25, 1.5*Math.PI, Math.PI, true);
            // ctx.moveTo(step2_x, Number(step2_y)+25);
            ctx.lineTo(step3_x,step3_y);
            ctx.fillText("2", Number(step3_x)+20, Number(step3_y)+20);
            ctx.lineTo(step4_x,step4_y);
            ctx.fillText("3", Number(step4_x)+20, Number(step4_y)+20);
            // ctx.lineTo(step5_x, step5_y);

            ctx.strokeStyle = "#FFF200";
            ctx.lineWidth = 6;
            ctx.stroke();
        };
        img.src = '/static/images/img-back.png'; // 设置图片源地址
    }

    //    第二步
    var canvas4 = document.getElementById("canvas4");
    if (canvas4.getContext) {
        var ctx4 = canvas4.getContext("2d");

        var img4 = new Image();   // 创建一个<img>元素
        img4.onload = function(){
            // 执行drawImage语句
            ctx4.scale(0.5, 0.5);
            ctx4.drawImage(img4,0,0);
            ctx4.font = "54px serif";
            ctx4.fillStyle = 'red';
            ctx4.fillText(from_name, 500, 70);
            ctx4.beginPath();
            ctx4.moveTo(step5_x,step5_y);
            ctx4.fillText("1", Number(step5_x)-200, Number(step5_y));
            ctx4.lineTo(680+25,step5_y);
            ctx4.arc(680+25, Number(step5_y)-25, 25, 0.5*Math.PI, Math.PI, false);
            ctx4.lineTo(680,Number(step6_y)+25-25);
            ctx4.arc(680-25, Number(step6_y)+25-25, 25, 0, 1.5*Math.PI, true);
            ctx4.lineTo(Number(step6_x)-65,Number(step6_y)-25);
            ctx4.arc(Number(step6_x)-65,Number(step6_y)+25-25,25,1.5*Math.PI,Math.PI,true);
            ctx4.lineTo(500,Number(step13_y)-25);
            ctx4.arc(500-25,Number(step13_y)-25,25,0,0.5*Math.PI,false);
            ctx4.lineTo(step13_x,step13_y);
            ctx4.fillText("2", Number(step13_x)+100, Number(step13_y)-10);

            ctx4.strokeStyle = "#FFF200";
            ctx4.lineWidth = 6;
            ctx4.stroke();
        };
        img4.src = '/static/images/img-side.png'; // 设置图片源地址
    }
//

    //    第三步
    var canvas5 = document.getElementById("canvas5");
    if (canvas5.getContext) {
        var ctx5 = canvas5.getContext("2d");

        var img5 = new Image();   // 创建一个<img>元素
        img5.onload = function(){
            // 执行drawImage语句
            ctx5.scale(0.5, 0.5);
            ctx5.drawImage(img5,0,0);
            ctx5.font = "54px serif";
            ctx5.fillStyle = 'red';
            ctx5.fillText(from_name, 370, 60);
            ctx5.fillText(to_name, 1200, 60);
            ctx5.beginPath();
            ctx5.moveTo(step10_x,step10_y);
            ctx5.fillText("1", Number(step10_x)-40, Number(step10_y)+20);
            ctx5.lineTo(step11_x,Number(step11_y)+25);
            ctx5.arc(Number(step11_x)+25,Number(step11_y)+25,25,Math.PI,1.5*Math.PI,false);
            ctx5.lineTo(step12_x,step12_y);
            ctx5.fillText("2", Number(step12_x)+20, Number(step12_y)+20);
//            // ctx3.lineTo(step10_x,step10_y);
            ctx5.strokeStyle = "#FFF200";
            ctx5.lineWidth = 4;
            ctx5.stroke();
        };
        img5.src = '/static/images/two-front.png'; // 设置图片源地址
    }
//

//    第二步
    var canvas2 = document.getElementById("canvas2");
    if (canvas2.getContext) {
        var ctx2 = canvas2.getContext("2d");

        var img2 = new Image();   // 创建一个<img>元素
        img2.onload = function(){
            // 执行drawImage语句
            ctx2.scale(0.5, 0.5);
            ctx2.drawImage(img2,0,0);
            ctx2.font = "54px serif";
            ctx2.fillStyle = 'red';
            ctx2.fillText(from_name, 500, 70);
            ctx2.beginPath();
            ctx2.moveTo(step5_x,step5_y);
            ctx2.fillText("1", Number(step5_x)-200, Number(step5_y));
            ctx2.lineTo(680+25,step5_y);
            ctx2.arc(680+25, Number(step5_y)-25, 25, 0.5*Math.PI, Math.PI, false);
            // ctx2.moveTo(680, Number(step5_y)-25);
            ctx2.lineTo(680,Number(step6_y)+25-25);
            ctx2.arc(680-25, Number(step6_y)+25-25, 25, 0, 1.5*Math.PI, true);
            // ctx2.moveTo(680-25, step6_y);
            ctx2.lineTo(Number(step6_x)-65,Number(step6_y)-25);
            ctx2.arc(Number(step6_x)-65,Number(step6_y)+25-25,25,1.5*Math.PI,Math.PI,true);
            // ctx2.moveTo(Number(step6_x)-95,Number(step6_y)+25);
            ctx2.lineTo(Number(step6_x)-90,2930);
            ctx2.arc(Number(step6_x)-90+25,2930,25,Math.PI,0.5*Math.PI,true);
            // ctx2.moveTo(Number(step6_x)-95+25,2930+25);
            ctx2.lineTo(680-25,2930+25);
            ctx2.arc(680-25,2930,25,0.5*Math.PI,0,true);
            ctx2.lineTo(680,2810+25);
            ctx2.arc(680-25,2810+25,25,0,1.5*Math.PI,true);
            ctx2.lineTo(525+25,2810);
            ctx2.arc(525+25,2810-25,25,0.5*Math.PI,Math.PI,false);
            ctx2.lineTo(525,Number(step7_y)+25);
            ctx2.arc(525+25,Number(step7_y)+25,25,Math.PI,1.5*Math.PI,false);
            ctx2.lineTo(655-25,step7_y);
            ctx2.arc(655-25,Number(step7_y)+25,25,1.5*Math.PI,2*Math.PI,false);
            ctx2.lineTo(655,Number(step8_y)-25);
            ctx2.arc(655+25,Number(step8_y)-25,25,Math.PI,0.5*Math.PI,true);
            ctx2.lineTo(step8_x,step8_y);
            ctx2.fillText("2", Number(step8_x)-170, Number(step8_y));
            // ctx2.arc(Number(step8_x)-25,Number(step8_y)-25,25,0.5*Math.PI,0,true);
            ctx2.lineTo(step9_x,step9_y);
            // if (step8_y == step9_y){
            //     ctx2.fillText(",3", Number(step9_x)+50, Number(step9_y)+20);
            // }
            // else if (step5_y == step9_y){
            //     ctx2.fillText(",3", Number(step9_x)+50, Number(step9_y)+20);
            // }
            // else {
            //     ctx2.fillText("3", Number(step9_x)+20, Number(step9_y)+20);
            // }
            ctx2.fillText("3", Number(step9_x), Number(step9_y)+50);

            ctx2.strokeStyle = "#FFF200";
            ctx2.lineWidth = 6;
            ctx2.stroke();
        };
        img2.src = '/static/images/img-side.png'; // 设置图片源地址
    }
//
//
    //    第三步
    var canvas3 = document.getElementById("canvas3");
    if (canvas3.getContext) {
        var ctx3 = canvas3.getContext("2d");

        var img3 = new Image();   // 创建一个<img>元素
        img3.onload = function(){
            // 执行drawImage语句
            ctx3.scale(0.5, 0.5);
            ctx3.drawImage(img3,0,0);
            ctx3.font = "54px serif";
            ctx3.fillStyle = 'red';
            ctx3.fillText(to_name, 370, 70);
            ctx3.beginPath();
            ctx3.moveTo(step10_x,step10_y);
            ctx3.fillText("1", Number(step10_x)-40, Number(step10_y)+20);
            ctx3.lineTo(step11_x,Number(step11_y)+25);
            ctx3.arc(Number(step11_x)+25,Number(step11_y)+25,25,Math.PI,1.5*Math.PI,false);
            ctx3.lineTo(step12_x,step12_y);
            ctx3.fillText("2", Number(step12_x)+20, Number(step12_y)+20);
//            // ctx3.lineTo(step10_x,step10_y);
            ctx3.strokeStyle = "#FFF200";
            ctx3.lineWidth = 4;
            ctx3.stroke();
        };
        img3.src = '/static/images/img-back.png'; // 设置图片源地址
    }
}
