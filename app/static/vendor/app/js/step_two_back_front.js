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
    var step8_1_x = $("#picStep8_1_x").val();
    var step8_1_y = $("#picStep8_1_y").val();
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
    var step5_1_x = $("#picStep5_1_x").val();
    var step5_1_y = $("#picStep5_1_y").val();
    var step13_1_x = $("#picStep13_1_x").val();
    var step13_1_y = $("#picStep13_1_y").val();
    var step6_6_x = $("#picStep6_6_x").val();
    var step6_6_y = $("#picStep6_6_y").val();
    var step7_7_x = $("#picStep7_7_x").val();
    var step7_7_y = $("#picStep7_7_y").val();
    var step7_8_x = $("#picStep7_8_x").val();
    var step7_8_y = $("#picStep7_8_y").val();
    var from_name = $("#from_name").val();
    var to_name = $("#to_name").val();
    var color = $("#color").val();
    var right_to_left = $("#right_to_left").val();
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
            ctx.lineTo(step4_x,Number(step4_y)+30);
            ctx.fillText("3", Number(step4_x)+20, Number(step4_y)+70);
            // ctx.lineTo(step5_x, step5_y);

            ctx.strokeStyle = color;
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
            ctx4.fillText("4", Number(step5_x)-200, Number(step5_y));
            ctx4.lineTo(900+25,step5_y);
            ctx4.arc(900+25,Number(step5_y)+25,25,1.5*Math.PI,Math.PI,true);
            ctx4.lineTo(900,step5_1_y);
            ctx4.arc(900-25,step5_1_y,25,0,0.5*Math.PI,false);
            ctx4.lineTo(680+25,Number(step5_1_y)+25);
            ctx4.arc(680+25,step5_1_y,25,0.5*Math.PI,Math.PI,false);
            ctx4.lineTo(680,Number(step6_y)+25-25);

            ctx4.arc(680-25, Number(step6_y)+25-25, 25, 0, 1.5*Math.PI, true);
            ctx4.lineTo(Number(step6_x)-65,Number(step6_y)-25);
            ctx4.arc(Number(step6_x)-65,Number(step6_y)+25-25,25,1.5*Math.PI,Math.PI,true);

            if (step13_1_x == 0){
                ctx4.lineTo(Number(step6_x)-90,Number(step13_y)-25);
                ctx4.arc(Number(step6_x)-115,Number(step13_y)-25,25,0,0.5*Math.PI,false)
            }
            else{
                ctx4.lineTo(Number(step6_x)-90,Number(step13_1_y)-25);
                ctx4.arc(Number(step6_x)-115,Number(step13_1_y)-25,25,0,0.5*Math.PI,false);
                ctx4.lineTo(330+25,step13_1_y);
                ctx4.arc(330+25,Number(step13_1_y)-25,25,0.5*Math.PI,Math.PI,false);
                ctx4.lineTo(330,Number(step13_y)+25);
                ctx4.arc(330-25,Number(step13_y)+25,25,0,1.5*Math.PI,true);
            }
            ctx4.lineTo(step13_x,step13_y);
            ctx4.fillText("5", Number(step13_x)+10, Number(step13_y)-10);

            ctx4.strokeStyle = color;
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
            if (right_to_left == 0){
                ctx5.fillText(from_name, 370, 60);
                ctx5.fillText(to_name, 1200, 60);
                ctx5.beginPath();
                ctx5.moveTo(step8_1_x,step8_1_y);
                ctx5.fillText("6", Number(step8_1_x)-40, Number(step8_1_y)+20);
                ctx5.arc(Number(step8_1_x)+25,Number(step8_1_y),25,Math.PI,0.5*Math.PI,true);
                ctx5.lineTo(Number(step8_1_x)+930,Number(step8_1_y)+25);
                ctx5.arc(Number(step8_1_x)+930,Number(step8_1_y),25,0.5*Math.PI,0,true);
                // ctx5.lineTo(Number(step8_1_x)+930-50,Number(step8_1_y)-50);
                // ctx5.arc(Number(step8_1_x)+930-75,Number(step8_1_y)-50,25,0,1.5*Math.PI,true);
                // ctx5.lineTo(Number(step8_1_x)+930-125,Number(step8_1_y)-75);
                ctx5.fillText("7", Number(step8_1_x)+930, Number(step8_1_y));
            }
            else if (right_to_left == 1){
                ctx5.fillText(to_name, 370, 60);
                ctx5.fillText(from_name, 1200, 60);
                ctx5.beginPath();
                ctx5.moveTo(step8_1_x,step8_1_y);
                ctx5.fillText("6", Number(step8_1_x), Number(step8_1_y)+20);
                ctx5.arc(Number(step8_1_x)-25, step8_1_y, 25, 0, 0.5*Math.PI, false);
                ctx5.lineTo(Number(step8_1_x)-930-25, Number(step8_1_y)+25);
                ctx5.arc(Number(step8_1_x)-930-25,Number(step8_1_y),25,0.5*Math.PI,Math.PI,false);
                ctx5.lineTo(Number(step8_1_x)-930-50,Number(step8_1_y)-55);
                ctx5.arc(Number(step8_1_x)-930-75,Number(step8_1_y)-55,25,0,1.5*Math.PI,true);
                ctx5.lineTo(650, Number(step8_1_y)-55-25);
                ctx5.fillText("7", 650-50, Number(step8_1_y)-55);
            }

            ctx5.strokeStyle = color;
            ctx5.lineWidth = 6;
            ctx5.stroke();
        };
        img5.src = '/static/images/two-front.png'; // 设置图片源地址
    }


    if (right_to_left == 0) {
            //    第四-1步
        var canvas41 = document.getElementById("canvas41");
        if (canvas41.getContext) {
            var ctx41 = canvas41.getContext("2d");

            var img41 = new Image();   // 创建一个<img>元素
            img41.onload = function(){
                // 执行drawImage语句
                ctx41.scale(0.5, 0.5);
                ctx41.drawImage(img41,0,0);
                ctx41.font = "54px serif";
                ctx41.fillStyle = 'red';
                ctx41.fillText(to_name, 500, 70);
                ctx41.beginPath();

                ctx41.moveTo(Number(step13_x),Number(step13_y));
                ctx41.fillText("8", Number(step13_x)+20, Number(step13_y)-20);
                if (step13_1_x == 0){
                    ctx41.lineTo(500-25,Number(step13_y)+100);
                    ctx41.arc(500-25,Number(step13_y)-25+100,25,0.5*Math.PI,0,true);
                }
                else{
                    ctx41.lineTo(330-25,Number(step13_y));
                    ctx41.arc(330-25,Number(step13_y)+25,25,1.5*Math.PI,0,false);
                    ctx41.lineTo(330,step13_1_y);
                    ctx41.arc(330+25,step13_1_y,25,Math.PI,0.5*Math.PI,true);
                    ctx41.lineTo(500-25,Number(step13_1_y)+25);
                    ctx41.arc(500-25,step13_1_y,25,0.5*Math.PI,0,true);
                }

                ctx41.lineTo(500,step6_6_y);
                ctx41.arc(500+25,step6_6_y,25,Math.PI,1.5*Math.PI,false);
                ctx41.lineTo(680-25,Number(step6_6_y)-25);
                ctx41.arc(680-25,Number(step6_6_y)-25+25,25,1.5*Math.PI,2*Math.PI,false);
                ctx41.lineTo(680,2930);
                ctx41.arc(680-25,2930,25,0,0.5*Math.PI,false);
                ctx41.lineTo(500+50,2930+25);
                ctx41.arc(500+50,2930,25,0.5*Math.PI,Math.PI,false);
                ctx41.lineTo(500+25,2810+25);
                ctx41.arc(500+50,2810+25,25,Math.PI,1.5*Math.PI,false);
                ctx41.lineTo(680-25-25,2810);
                ctx41.arc(680-25-25,2810-25,25,0.5*Math.PI,0,true);
                ctx41.lineTo(680-25,Number(step7_7_y)+25);
                ctx41.arc(680-25-25,Number(step7_7_y)+25,25,0,1.5*Math.PI,true);
                ctx41.lineTo(525+25,step7_7_y);
                ctx41.arc(525+25,Number(step7_7_y)+25,25,1.5*Math.PI,Math.PI,true);
                if (step7_8_x == 0){
                    ctx41.lineTo(525,Number(step8_y)-25);
                    ctx41.arc(525-25,Number(step8_y)-25,25,0,0.5*Math.PI,false);
                }
                else{
                    ctx41.lineTo(525,Number(step7_8_y)-25);
                    ctx41.arc(525-25,Number(step7_8_y)-25,25,0,0.5*Math.PI,false);
                    ctx41.lineTo(330+25,step7_8_y);
                    ctx41.arc(330+25,Number(step7_8_y)-25,25,0.5*Math.PI,Math.PI,false);
                    ctx41.lineTo(330,Number(step8_y)+25);
                    ctx41.arc(330-25,Number(step8_y)+25,25,0,1.5*Math.PI,true);
                }
                ctx41.lineTo(step8_x,step8_y);
                ctx41.fillText("9", Number(step8_x), Number(step8_y)+50);

                ctx41.strokeStyle = color;
                ctx41.lineWidth = 6;
                ctx41.stroke();
            };
            img41.src = '/static/images/img-side.png'; // 设置图片源地址
        }
    }


    //    第四步
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
            if (right_to_left == 0){
                ctx3.moveTo(750,step10_y);
                ctx3.fillText("10", 680, Number(step8_y)-30);
                ctx3.lineTo(Number(step10_x)+18,step10_y);
                ctx3.arc(Number(step10_x)+18,Number(step10_y)-25,25,0.5*Math.PI,Math.PI,false);
                ctx3.lineTo(Number(step9_x)-7,step9_y);
                ctx3.fillText("11", Number(step9_x)-7+20, Number(step9_y)+20);
            }
            else if (right_to_left == 1){
                ctx3.moveTo(680,step10_y);
                ctx3.fillText("8", 680, Number(step8_1_y)-30);
                ctx3.lineTo(Number(step10_x)+12,step10_y);
                ctx3.arc(Number(step10_x)+12,Number(step10_y)-25,25,0.5*Math.PI,Math.PI,false);
                ctx3.lineTo(Number(step9_x)-13,step9_y);
                ctx3.fillText("9", Number(step9_x)+20-13, Number(step9_y)+20);
            }
            ctx3.strokeStyle = color;
            ctx3.lineWidth = 6;
            ctx3.stroke();
        };
        img3.src = '/static/images/img-front.png'; // 设置图片源地址
    }
}


jQuery(document).ready(function($){
	// browser window scroll (in pixels) after which the "back to top" link is shown
	var offset = 300,
		//browser window scroll (in pixels) after which the "back to top" link opacity is reduced
		offset_opacity = 1200,
		//duration of the top scrolling animation (in ms)
		scroll_top_duration = 700,
		//grab the "back to top" link
		$back_to_top = $('.cd-top');

	//hide or show the "back to top" link
	$(window).scroll(function(){
		( $(this).scrollTop() > offset ) ? $back_to_top.addClass('cd-is-visible') : $back_to_top.removeClass('cd-is-visible cd-fade-out');
		if( $(this).scrollTop() > offset_opacity ) {
			$back_to_top.addClass('cd-fade-out');
		}
	});

	//smooth scroll to top
	$back_to_top.on('click', function(event){
		event.preventDefault();
		$('body,html').animate({
			scrollTop: 0 ,
		 	}, scroll_top_duration
		);
	});

});