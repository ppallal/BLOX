<?php

	//INPUT FORMAT
	/*
		All GET Parameters must follow these rules.
		loc[Number][Parameter]
		Number -> Start with 1. Increment for each text element.
		Paramenter -> 	S -> Size of text
						L -> Distance from left to place
						R -> Distance from top to place
						T -> The text to display

	*/



    $image = imagecreate(400,300);
    $blue = imagecolorallocate($image, 0, 0, 255);
    $white = ImageColorAllocate($image, 255,255,255);

    // if(!isset($_GET['size'])) $_GET['size'] = 44;
    // if(!isset($_GET['text'])) $_GET['text'] = "Hello, world!";

    $i = 1;
    while(1){
    	if(isset($_GET['loc'.$i.'L'])){
    		imagettftext($image, $_GET['loc'.$i.'S'], 0, $_GET['loc'.$i.'L'], $_GET['loc'.$i.'R'], $white, "/var/www/TNR.ttf", $_GET['loc'.$i.'T']);		
    		$i++;
    	}else{
    		break;
    	}
    } 
    header("content-type: image/png");
    imagepng($image);
    imagedestroy($image);
?>
