$(function modifyWidth(){
    var imgWidth = $(".img").width();
    $(".img").css("border-top-left-radius","15px");
    $(".img").css("border-top-right-radius","15px");
    $(".imgHome").css("border-bottom-left-radius","15px");
    $(".imgHome").css("border-bottom-right-radius","15px");
    $(".iconesAlbum").css("margin-bottom","20px");
    $(".iconesAlbum").css("margin-top","20px");
    $(".fond-gris").css("width",imgWidth+"px");
    $(".fond-gris").css("margin","auto");
    $(".fond-gris").css("background","#989898");
    $(".fond-gris").css("border-bottom-left-radius","15px");
    $(".fond-gris").css("border-bottom-right-radius","15px");
    $(".blanc").css("color","white");
    // $(".setWidthImage").css("width",imgWidth);
    // $(".setWidthImage").css("margin","auto");
    $(".dateGris").css("color","#E6E6E6");
});
