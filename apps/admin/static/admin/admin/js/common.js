BASE_PATH = 'http://127.0.0.1:5000';
layui.jquery.cookie = function (name, value, options) {
    let $ = layui.jquery
    if (typeof value != 'undefined') {
        options = options || {};
        if (value === null) {
            value = '';
            options.expires = -1;
        }
        var expires = '';
        if (options.expires && (typeof options.expires == 'number' || options.expires.toUTCString)) {
            var date;
            if (typeof options.expires == 'number') {
                date = new Date();
                date.setTime(date.getTime() + (options.expires * 24 * 60 * 60 * 1000));
            } else {
                date = options.expires;
            }
            expires = '; expires=' + date.toUTCString();
        }
        var path = options.path ? '; path=' + options.path : '';
        var domain = options.domain ? '; domain=' + options.domain : '';
        var secure = options.secure ? '; secure' : '';
        document.cookie = [name, '=', encodeURIComponent(value), expires, path, domain, secure].join('');
    } else {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = $.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
};

function addHeaders(jqXHR) {
    let $ = layui.jquery;
    //jqXHR.setRequestHeader('FLASK-CSRF-TOKEN', $.cookie('flask_redis_csrf_token'))
    jqXHR.setRequestHeader('FLASK-CSRF-TOKEN', localStorage.getItem("flask_redis_csrf_token"))
}

function dealWithError(xhr) {
    var regx = /^5.*/;
    if (regx.test(xhr.status)) {
        layer.alert('内部服务器错误，请联系管理员或稍后再试！');
    } else {
        layer.alert('网络异常！');
    }
}

function dealWithComplete(xhr) {
//    console.log(xhr.responseText)
//    var res = JSON.parse(xhr.responseText);
    //console.log(xhr.getResponseHeader('CSRF_TOKEN'));
    csrfToken = xhr.getResponseHeader('CSRF_TOKEN');
    if (csrfToken) {
//        alert(csrfToken);
        localStorage.setItem("flask_redis_csrf_token", csrfToken);
//        console.log(localStorage.getItem("flask_redis_csrf_token"));
    }
    if (xhr.responseText.status == 401) { // 未登录
        window.location.href = '/login'
    }
}

layui.jquery.ajaxSetup({
    beforeSend: function (jqXHR, settings) {
        // if (location.hostname == 'localhost') {
        //     settings.url = 'https://www.abc.com/' + settings.url;
        // }

        /*header里加请求头参数*/
        addHeaders(jqXHR);
//        console.log(localStorage.getItem("flask_redis_csrf_token"));

        // alert('进入Ajax beforeSend 方法');
    },
    success: function (result, status, xhr) {

    },
    error: function (xhr, status, error) {
        dealWithError(xhr);
        return false;
    },
    complete: function (xhr, status) {
        dealWithComplete(xhr);
    }

});
/* defaultErrFunc = function (data) {
    if (data.loading) {
        layer.close(loading)
    }
    layer.msg('网络错误', { icon: 2, time: 1000 })
}

function novelAjax(data) {
    var ret = null;
    let $ = data.$;

    $.ajax({
        url: data.url,
        data: data.transfer2Json ? JSON.stringify(data) : data,
        dataType: 'json',
        contentType: 'application/json',
        type: data.type ? data.type : 'GET',
        success: function (res) {
            if (data.success && $.isFunction(data.success)) {
                data.success();
            }

            ret = res;
        },
        // error: (data.error && $.isFunction(data.error)) ? data.error : defaultErrFunc(data)
        error: (data.error && $.isFunction(data.error)) ? data.error : function () {
            if (data.loading) {
                layer.close(loading)
            }
            layer.msg('网络错误', { icon: 2, time: 1000 })
        }
    });

    return ret;
} */
