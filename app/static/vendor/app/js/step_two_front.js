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
//    var step8_1_x = $("#picStep8_1_x").val();
//    var step8_1_y = $("#picStep8_1_y").val();
//    var step8_2_x = $("#picStep8_2_x").val();
//    var step8_2_y = $("#picStep8_2_y").val();
//    var step8_3_x = $("#picStep8_3_x").val();
//    var step8_3_y = $("#picStep8_3_y").val();
//    var step8_4_x = $("#picStep8_4_x").val();
//    var step8_4_y = $("#picStep8_4_y").val();
//    var step8_5_x = $("#picStep8_5_x").val();
//    var step8_5_y = $("#picStep8_5_y").val();
    var step9_x = $("#picStep9_x").val();
    var step9_y = $("#picStep9_y").val();
    var step10_x = $("#picStep10_x").val();
    var step10_y = $("#picStep10_y").val();
    var step11_x = $("#picStep11_x").val();
    var step11_y = $("#picStep11_y").val();
    var step12_x = $("#picStep12_x").val();
    var step12_y = $("#picStep12_y").val();
//    var step13_x = $("#picStep13_x").val();
//    var step13_y = $("#picStep13_y").val();
    var from_name = $("#from_name").val();
    var to_name = $("#to_name").val();
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
            ctx.font = "54px serif";
            ctx.fillStyle = 'red';
            ctx.fillText(from_name, 370, 60);
            ctx.fillText(to_name, 1200, 60);
            ctx.beginPath();
            ctx.moveTo(step1_x,step1_y);
            ctx.fillText("1", Number(step1_x)+20, Number(step1_y)+20);
            ctx.lineTo(step2_x,Number(step2_y)-25);
            ctx.arc(Number(step2_x)+25,Number(step2_y)-25,25,Math.PI,0.5*Math.PI,true);
            ctx.lineTo(Number(step4_x)-70-25,step3_y);
            ctx.arc(Number(step4_x)-70-25,Number(step3_y)+25,25,1.5*Math.PI,2*Math.PI,false);
            ctx.lineTo(Number(step4_x)-70,Number(step4_y)-25);
            ctx.arc(Number(step4_x)-70+25,Number(step4_y)-25,25,Math.PI,0.5*Math.PI,true);
            ctx.lineTo(Number(step4_x)+830-25, step4_y);
            ctx.arc(Number(step4_x)+830-25,Number(step4_y)-25,25,0.5*Math.PI,0,true);
            ctx.fillText("2", Number(step4_x)+830+20, Number(step4_y)+20);
            ctx.strokeStyle = "#FFF200";
            ctx.lineWidth = 6;
            ctx.stroke();
        };
        img.src = '/static/images/two-front.png'; // 设置图片源地址
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
            ctx2.fillText(to_name, 500, 70);
            ctx2.beginPath();
            ctx2.moveTo(step5_x,step5_y);
            ctx2.fillText("3", Number(step5_x)+80, Number(step5_y)-20);
            ctx2.lineTo(680-25,step5_y);
            ctx2.arc(680-25,Number(step5_y)-25,25,0.5*Math.PI,0,true);
            ctx2.lineTo(680,step6_y);
            ctx2.arc(680-25,step6_y,25,2*Math.PI,1.5*Math.PI,true);
            ctx2.lineTo(525,Number(step6_y)-25);
            ctx2.arc(525,Number(step6_y)-25+25,25,1.5*Math.PI,Math.PI,true);
            // // ctx2.lineTo(680,2930);
            // // ctx2.arc(680-25,2930,25,0,0.5*Math.PI,false);
            // // ctx2.lineTo(500+25,2930+25);
            // // ctx2.arc(500+25,2930,25,0.5*Math.PI,Math.PI,false);
            // // ctx2.lineTo(500,2810+25);
            // // ctx2.arc(500+25,2810+25,25,Math.PI,1.5*Math.PI,false);
            // // ctx2.lineTo(680-25-25,2810);
            // // ctx2.arc(680-25-25,2810-25,25,0.5*Math.PI,0,true);
            ctx2.lineTo(525-25,Number(step8_y)-25);
            ctx2.arc(525-25-25,Number(step8_y)-25,25,0,0.5*Math.PI,false);
            // // ctx2.lineTo(525+25,step7_y);
            // // ctx2.arc(525+25,Number(step7_y)+25,25,1.5*Math.PI,Math.PI,true);
            // // ctx2.lineTo(525,Number(step8_y));
            // // ctx2.arc(525-25,Number(step8_y)-25,25,0,0.5*Math.PI,false);
            ctx2.lineTo(step8_x,step8_y);
            ctx2.fillText("4", Number(step8_x)+150, Number(step8_y)-20);

            ctx2.strokeStyle = "#FFF200";
            ctx2.lineWidth = 6;
            ctx2.stroke();
        };
        img2.src = '/static/images/img-side.png'; // 设置图片源地址
    }


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
            ctx3.moveTo(step12_x,step12_y);
            ctx3.fillText("5", Number(step12_x)+20, Number(step12_y)+20);
            ctx3.lineTo(step12_x,Number(step11_y)+25);
            ctx3.arc(Number(step12_x)-25,Number(step11_y)+25,25,0,1.5*Math.PI,true);
            ctx3.lineTo(Number(step10_x)+25,step10_y);
            ctx3.arc(Number(step10_x)+25,Number(step10_y)-25,25,0.5*Math.PI,Math.PI,false);
            ctx3.lineTo(step9_x,step9_y);
            ctx3.fillText("6", Number(step9_x)+20, Number(step9_y)+20);
            ctx3.strokeStyle = "#FFF200";
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