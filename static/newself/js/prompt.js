$(':submit').click(function () {
    $('.error').remove();
    var flag = true;
    $('#notice').find('input[type="text"]').each(function () {
        var v = $(this).val();
        if(v.length <= 0){
            flag = false;
            var tag = document.createElement('span');
            tag.className = 'error';
            tag.innerHTML = '必填';
            $(this).after(tag);
        }
    })
    return flag;
})
