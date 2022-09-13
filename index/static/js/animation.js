$(document).ready(function(){
	
    var t = setInterval(next,3000);
	var color= ['red','blue','green'];
	$("#quote_color").css('background-color','red');

	var num = 0;

	function next(){
        num++;
		var color1 = $("#quote_color");
		if (num > color.length){
			num = 0;
		}
		$("#quote_color").css('background-color',color[num]);

	}
	

})