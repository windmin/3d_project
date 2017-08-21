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
    // var step7_x = $("#picStep7_x").val();
    // var step7_y = $("#picStep7_y").val();
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
    var step10_x = $("#picStep10_x").val();
    var step10_y = $("#picStep10_y").val();
    var step11_x = $("#picStep11_x").val();
    var step11_y = $("#picStep11_y").val();
    // var step12_x = $("#picStep12_x").val();
    // var step12_y = $("#picStep12_y").val();
    // var step13_x = $("#picStep13_x").val();
    // var step13_y = $("#picStep13_y").val();
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
            ctx.beginPath();
            ctx.moveTo(step1_x,step1_y);
            ctx.fillText("1", Number(step1_x)+20, Number(step1_y)+20);
            ctx.lineTo(step2_x,step2_y);
            ctx.lineTo(step3_x,step3_y)
            ctx.fillText("2", Number(step3_x)+20, Number(step3_y)+20);
            if (step4_x != ''){
                ctx.lineTo(step4_x,step4_y);
                ctx.fillText("3", Number(step4_x)+20, Number(step4_y)+20);
                ctx.bezierCurveTo(Number(step4_x)-150,Number(step4_y)+100,80,170,180,270);
                ctx.fillText("4", 200, 290);
            }
            else if (step4_x == ''){
                ctx.bezierCurveTo(Number(step3_x)-150,Number(step3_y)+200,80,170,180,270);
                ctx.fillText("3", 200, 290);
            }

            ctx.strokeStyle = "blue";
            ctx.lineWidth = 4;
            ctx.stroke();
        };
        img.src = '/static/images/img-back.png'; // 设置图片源地址
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
            ctx2.font = "54px serif";
            ctx2.fillStyle = 'red';
            ctx2.beginPath();
            ctx2.moveTo(590,240);
            if (step4_x == ''){
                ctx2.fillText("4", 610, 260);
            }
            else if(step4_x != ''){
                ctx2.fillText("5", 610, 260);
            }
            ctx2.bezierCurveTo(460,110,410,2965,590,2930);

            //需要13个先绕一圈
            if (step8_1_x != ''){
//                 ctx2.lineTo(step8_1_x,step8_1_y);
//                 ctx2.lineTo(step8_2_x,step8_2_y);
//                 ctx2.lineTo(step8_3_x,step8_3_y);
// ////                ctx2.lineTo(step8_4_x,step8_4_y);
// ////                ctx2.lineTo(step8_5_x,step8_5_y);
//                 //如果不是最后一块多2步
//                 if (step9_x != 230){
//                     ctx2.lineTo(670,2950); //(530,2950)
//                 }
//                 ctx2.lineTo(step9_x,step9_y);
//                 if (step9_x != 230){
//                     ctx2.lineTo(240,step9_y);
//                 }
            }
            else if (step8_1_x == '' && step8_5_x != ''){
                ctx2.bezierCurveTo(730,2965,740,step8_5_y-20,590,step8_5_y);
                //from_point[0]==12
                if (step4_x == ''){
                    ctx2.fillText("5", 610, Number(step8_5_y)-10);
                }
                else if(step4_x != ''){
                    ctx2.fillText("6", 610, Number(step8_5_y)-10);
                }
                ctx2.bezierCurveTo(440,step8_5_y-20,440,2985,590,2950);
                // to_point[0] != 12
                if (step5_x != '') {
                    ctx2.bezierCurveTo(880, 2985, Number(step5_x) - 200, Number(step5_y) - 200, step5_x, step5_y);
                    if (step4_x == '') {
                        ctx2.fillText("6", Number(step5_x) + 20, Number(step5_y) + 20);
                    }
                    else if (step4_x != '') {
                        ctx2.fillText("7", Number(step5_x) + 20, Number(step5_y) + 20);
                    }
                    ctx2.quadraticCurveTo(Number(step6_x)+20,Number(step6_y)+20,step6_x,step6_y);
                    if (step4_x == ''){
                        ctx2.fillText("7", Number(step6_x) + 20, Number(step6_y) + 20)
                    }
                    else if (step4_x != ''){
                        ctx2.fillText("8", Number(step6_x) + 20, Number(step6_y) + 20)
                    }
                }
                else if(step5_x == ''){
                    ctx2.bezierCurveTo(880,2985,Number(step6_x)-20,Number(step6_y)-20,step6_x,step6_y)
                    if (step4_x == ''){
                        ctx2.fillText("6", Number(step6_x) + 20, Number(step6_y) + 20);
                    }
                    else if (step4_x != ''){
                        ctx2.fillText("7", Number(step6_x) + 20, Number(step6_y) + 20);
                    }
                }
            }
            //不用绕圈
            else if (step8_1_x == '' && step8_5_x == ''){
//              // to_point[0] != 12
                if (step5_x != '') {
                    ctx2.bezierCurveTo(880, 2985, Number(step5_x) - 200, Number(step5_y) - 200, step5_x, step5_y);
                    if (step4_x == '') {
                        ctx2.fillText("6", Number(step5_x) + 20, Number(step5_y) + 20);
                    }
                    else if (step4_x != '') {
                        ctx2.fillText("7", Number(step5_x) + 20, Number(step5_y) + 20);
                    }
                    ctx2.quadraticCurveTo(Number(step6_x)+20,Number(step6_y)+20,step6_x,step6_y);
                    if (step4_x == ''){
                        ctx2.fillText("7", Number(step6_x) + 20, Number(step6_y) + 20)
                    }
                    else if (step4_x != ''){
                        ctx2.fillText("8", Number(step6_x) + 20, Number(step6_y) + 20)
                    }
                }
                else if(step5_x == ''){
                    ctx2.bezierCurveTo(880,2985,Number(step6_x)-20,Number(step6_y)-20,step6_x,step6_y)
                    if (step4_x == ''){
                        ctx2.fillText("6", Number(step6_x) + 20, Number(step6_y) + 20);
                    }
                    else if (step4_x != ''){
                        ctx2.fillText("7", Number(step6_x) + 20, Number(step6_y) + 20);
                    }
                }
            }

            ctx2.strokeStyle = "blue";
            ctx2.lineWidth = 4;
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
            ctx3.beginPath();
            ctx3.moveTo(step9_x,Number(step9_y)-30);
            if (step4_x == '' && step5_x == ''){
                ctx3.fillText("7", Number(step9_x)+20, Number(step9_y)-10);
            }
            else if (step4_x == '' || step5_x == ''){
                ctx3.fillText("8", Number(step9_x)+20, Number(step9_y)-10);
            }
            else {
                ctx3.fillText("9", Number(step9_x)+20, Number(step9_y)-10);
            }
            ctx3.lineTo(step10_x,step10_y);
            ctx3.lineTo(step11_x,step11_y);
            if (step4_x == '' && step5_x == ''){
                ctx3.fillText("8", Number(step11_x)+20, Number(step11_y)+20);
            }
            else if (step4_x == '' || step5_x == ''){
                ctx3.fillText("9", Number(step11_x)+20, Number(step11_y)+20);
            }
            else {
                ctx3.fillText("10", Number(step11_x)+20, Number(step11_y)+20);
            }
            // ctx3.lineTo(step10_x,step10_y);
            ctx3.strokeStyle = "blue";
            ctx3.lineWidth = 4;
            ctx3.stroke();
        };
        img3.src = '/static/images/img-back.png'; // 设置图片源地址
    }
}
