$(function(){
    $.material.init();
    $(".image").click(function(){
    	id = this.id
        // Agarra el numero del ID
    	id = id.substring(5, id.length);
        // Ajax request a image details ej: 1/34/*ID*
        $.ajax({
        	url: id,
        	dataType: "json",
        	success: function( data ){
        	console.log(data.url)
            // Caso origen Gelwebsite, agrega como iframe
            if(data.url.substring(0,15)== "https://href.li"){
                // $('body').append('<iframe src="'+data.url+'" class="iframe" scrolling="no">')
                // $('body').append("<div class='fullscreen' style='position:absolute;z-index:11;width:100%;height:100%;'></div>")
                var redirectWindow = window.open(data.url, '_blank')
                redirectWindow.focus();
            }
            // Caso webm
            else if(data.url.substring(data.url.length - 4, data.url.length) == "webm"){
                $('body').append('<video id="video" class="fullscreen" autoplay loop muted=""><source src="'+data.url+'" type="video/webm"></video>')
                // Hide thumbnails para ahorar recursos
                $('.image').hide()
                $('.navbar').hide()
                // Agrega fondo
                $('#blackback').addClass('blackback')
            }
            else if(data.url.substring(data.url.length - 3, data.url.length) == "swf"){
                $('body').append('<object type="application/x-shockwave-flash" data="'+data.url+'" width="90%" height="90%" class="fullscreen"><param name="movie" value="'+data.url+'"/><param name="quality" value="high"/></object>')
                $('body').append("<div class='fullscreen' style='position:absolute;z-index:11;width:100%;height:100%;'></div>")
                // Hide thumbnails para ahorar recursos
                $('.image').hide()
                $('.navbar').hide()
                // Agrega fondo
                $('#blackback').addClass('blackback')
            }
            // Caso normal
            else{
        	   $('body').append("<img src="+data.url+" class='fullscreen'>")
                // Hide thumbnails para ahorar recursos
                $('.image').hide()
                $('.navbar').hide()
                // Agrega fondo
                $('#blackback').addClass('blackback')
            }
        	}
    	});
        console.log(id)
    })
    // Click en imagen maximizada
    $('body').on('click', '.fullscreen', function(){
        // Caso webm
        if(document.getElementById("video")){
            // location.reload()
            this.pause();
            this.src = "";
            this.load();
            $(this).remove();
        }
        // Caso normal
        else{
        	$('.fullscreen').remove()
            $('.iframe').remove()
        }
        // Revierte thumbnails y quita fondo
        $('.image').show()
        $('.navbar').show()
        $('#blackback').removeClass('blackback')
            
        
    })
})
