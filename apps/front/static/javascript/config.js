var needLoginPath = ['/user/favorites.html','/user/comment.html','/user/feedback.html',
    '/user/feedback_list.html','/user/read_history.html','/user/set_name.html',
    '/user/set_password.html','/user/set_sex.html','/user/setup.html','/user/userinfo.html',
    "/pay/index.html," +
    "/author/register.html","/author/index.html"];

function addHeaders(jqXHR) {
    jqXHR.setRequestHeader('X-CSRF-TOKEN', $.cookie('csrf_access_token'))
}

function dealWithError(xhr) {
    var regx = /^5.*/;
    if (regx.test(xhr.status)) {
         layer.alert('内部服务器错误，请联系管理员或稍后再试！');
    } else if (xhr.status == 401) { // 未登录
        $.cookie('access_token_cookie', null, { path: '/'  });
        if(needLoginPath.indexOf(window.location.pathname) != -1){
            location.href = '/user/login.html';
        }
    } else {
        layer.alert('网络异常！');
    }
}

if (typeof layui !== "undefined") {
    layui.$.ajaxSetup({

        beforeSend: function (jqXHR, settings) {
            // if (location.hostname == 'localhost') {
            //     settings.url = 'https://www.abc.com/' + settings.url;
            // }

            /*header里加请求头参数*/
            addHeaders(jqXHR);

            // alert('进入Ajax beforeSend 方法');
        },
        success: function (result, status, xhr) {

        },
        error: function (xhr, status, error) {
            dealWithError(xhr);
        },
        complete: function (xhr, status) {

        }

    });
}

if (typeof $ !== "undefined") {
    $.ajaxSetup({

    beforeSend: function (jqXHR, settings) {
        /*header里加请求头参数*/
        addHeaders(jqXHR);
    },
    success: function (result, status, xhr) {

    },
    error: function (xhr, status, error) {
        dealWithError(xhr);
    },
    complete: function (xhr, status) {

    }

});
}