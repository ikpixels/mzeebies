$(function (){

       $("#id_file").change(function () {
        if (this.files && this.files[0]) {
          var reader = new FileReader();
          
          reader.onload = function (e) {
            
            $("#ik_image").attr("src", e.target.result);
            $('#form_area').css("display","none");
            $("#ik_modal").css("display","block");
            var image = document.querySelector('#ik_image');


            var cropper = new Cropper(image, {
            dragMode: 'move',
            aspectRatio:1/1,
            autoCropArea:0.5,
            restore: true,
            guides: false,
            center: true,
            highlight: false,
            cropBoxMovable: true,
            cropBoxResizable: true,
            toggleDragModeOnDblclick: false,

          ready: function () {
           cropper.setCropBoxData(cropBoxData).setCanvasData(canvasData)

          }

          });
          count = 0.1;
          $("#plus").click(function () {
          cropper.zoomTo(count);
          count +=0.1;
          });
          
          count1 = 1;
          $("#minus").click(function () {
             cropper.zoomTo(count1);
             count1 -=0.1;
          });


          $("#send").click(function(){
            var cropData = cropper.getData();
            $("#id_x").val(cropData["x"]);
            $("#id_y").val(cropData["y"]);
            $("#id_height").val(cropData["height"]);
            $("#id_width").val(cropData["width"]);
            $("#formUpload").submit();

          })

        }

          reader.readAsDataURL(this.files[0]);
      }



      });  

});
//___________________________________________________________
$(function ()  {

       $("#id_image").change(function () {
        if (this.files && this.files[0]) {
          var reader = new FileReader();
          
          reader.onload = function (e) {
            
            $("#ik_image").attr("src", e.target.result);
            $('#form_area').css("display","none");
            $("#ik_modal").css("display","block");
            var image = document.querySelector('#ik_image');


            var cropper = new Cropper(image, {
            dragMode: 'move',
            aspectRatio: 16 / 9,
            autoCropArea: 0.65,
            restore: false,
            guides: false,
            center: false,
            highlight: false,
            cropBoxMovable: true,
            cropBoxResizable: true,
            toggleDragModeOnDblclick: false,

          ready: function () {
           cropper.setCropBoxData(cropBoxData).setCanvasData(canvasData)

          }

          });
          count = 0.1;
          $("#plus").click(function () {
          cropper.zoomTo(count);
          count +=0.1;
          });
          
          count1 = 1;
          $("#minus").click(function () {
             cropper.zoomTo(count1);
             count1 -=0.1;
          });


          $("#send").click(function(){
            var cropData = cropper.getData();
            $("#id_x").val(cropData["x"]);
            $("#id_y").val(cropData["y"]);
            $("#id_height").val(cropData["height"]);
            $("#id_width").val(cropData["width"]);
            $("#formUpload").submit();

          })

        }

          reader.readAsDataURL(this.files[0]);
      }



      });  

});
//___________________________________________________________
$(function ()  {

       $("#id_file2").change(function () {
        if (this.files && this.files[0]) {
          var reader = new FileReader();
          
          reader.onload = function (e) {
            
            $("#ik_image").attr("src", e.target.result);
            $('#form_area').css("display","none");
            $("#ik_modal").css("display","block");
            var image = document.querySelector('#ik_image');


            var cropper = new Cropper(image, {
            dragMode: 'move',
            aspectRatio: 2 / 1,
            autoCropArea: 0.5,
            restore: false,
            guides: false,
            center: false,
            highlight: false,
            cropBoxMovable: true,
            cropBoxResizable: true,
            toggleDragModeOnDblclick: false,

          ready: function () {
           cropper.setCropBoxData(cropBoxData).setCanvasData(canvasData)

          }

          });
          count = 0.1;
          $("#plus").click(function () {
          cropper.zoomTo(count);
          count +=0.1;
          });
          
          count1 = 1;
          $("#minus").click(function () {
             cropper.zoomTo(count1);
             count1 -=0.1;
          });


          $("#send").click(function(){
            var cropData = cropper.getData();
            $("#id_x").val(cropData["x"]);
            $("#id_y").val(cropData["y"]);
            $("#id_height").val(cropData["height"]);
            $("#id_width").val(cropData["width"]);
            $("#formUpload").submit();

          })

        }

          reader.readAsDataURL(this.files[0]);
      }



      });  

});