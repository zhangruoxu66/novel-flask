/**
 * 加载单条数据，用于编辑回显、查看详情加载等情况
 * @param url 请求数据的url
 * @param params 请求数据的查询参数
 * @param formElement 需要回显/展示数据的表单元素对象id，不需要加＃号
 * @return 后端返回的data对象
 */
function loadData(url, params, formElement) {
    const $ = layui.jquery
    const layuiForm = layui.form

    var ret;

    $.ajax({
        url: url,
        type: 'get',
        dataType: 'json',
        data: params,
        async: false,
        success: function (result) {
            if (result.code == 0) {
                let data = result.data
                layuiForm.val(formElement, data);
                ret = data;
            } else {
                if (result.msg) {
                    layer.msg(result.msg, { icon: 2, time: 1000 })
                } else {
                    layer.msg('加载数据失败！', { icon: 2, time: 1000 })
                }
            }
        },
        error: function () {
            layer.msg('网络错误，加载数据失败！', { icon: 2, time: 1000 })
        },
    });

    return ret;
}