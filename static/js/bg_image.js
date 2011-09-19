        $(function() {   
 
            var theWindow        = $(window);
            var $bg_image        = $("#bg_image");
            var aspectRatio      = $bg_image.width() / $bg_image.height();
                                        
            function resizeBg() {
                
                if ( (theWindow.width() / theWindow.height()) < aspectRatio ) {
                    $bg_image
                        .removeClass()
                        .addClass('bg_image_height');
                } else {
                    $bg_image
                        .removeClass()
                        .addClass('bg_image_width');
                }
                            
            }
                                        
            theWindow.resize(function() {
                resizeBg();
            }).trigger("resize");
        
        });
 
