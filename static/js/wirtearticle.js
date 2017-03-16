// 转换markdown格式展示
function markdown(){
		var text = $("#content").val();
		var converter = new showdown.Converter();
		var html = converter.makeHtml(text);
		$("#result").html(html);
	}

$(function(){
	var resultwh = $(document).height()-65;
    var contentwh = $(document).height()-105;
    var $oBtnSave = $('#save');
    var $oBtnSubmit = $('#submit');
    var $oForm = $('#form');
    var $content = $('#content');
    var $arttitle = $('#arttitle');

    // 动态获取result这个div的高
    $('#result').css('height',resultwh);
    $('#content').css('height',contentwh);
	$('.mask-info').click(function(){
                $('.pop').hide();
            })

    // 重新设置按钮方法
    $oBtnSave.click(function(){
        var hArray = window.location.href.split('/');
        var sLast = hArray[hArray.length-1];
        if (sLast == ''){
        	$oForm.prop({'action':"/book/save_article/"});
        }
        else{
        	href = "/book/save_article/" + sLast;
        	$oForm.prop({'action':href});
        }
        // $oForm.prop({'action':"{% url 'books:save_article' bookid %}"})
    })

    $oBtnSubmit.click(function(){
    	var hArray = window.location.href.split('/');
        var sLast = hArray[hArray.length-1];
        if (sLast == ''){
        	$oForm.prop({'action':"/book/release_article/"});
        }
        else{
        	href = "/book/release_article/" + sLast;
        	$oForm.prop({'action':href});
        }
        // $oForm.prop({'action':"{% url 'books:release_article' bookid %}"})
    })
})
