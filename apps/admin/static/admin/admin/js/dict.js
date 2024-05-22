//function loadDicts($, form) {
function loadDicts() {
    const $ = layui.jquery
    const form = layui.form

    selects = $('.dict-select')
    $.each(selects, function(index, select){
        let id = select.id;
        let dictKey = $('#' + id).attr('dict-key');
        var setDef = false;
        var defValue = null;
        if (select.hasAttribute('def-value')) {
            setDef = true;
            defValue = $('#' + id).attr('def-value');
        }

        $.ajax({
          url: '/admin/dict/dictData/get?dictKey=' +dictKey,
          type: 'get',
          dataType: 'json',
          success: function (result) {
            //console.log(result);
            if (result.success) {
                //console.log(result.data);
                //data = eval('(' + result.data + ')');
                // 如果后端返回result的data是直接从Redis里取出的json字符串，且未经转换（成模型对象），则需要使用eval函数解析json字符串
                // 如果后端把从Redis查出来的json字符串转换成模型对象（或字典），那么经过视图函数的jsonify之后返回给前端的的json对象就不需要转换了
                data = result.data;
                //data = result.data;
                //console.log(data);
                var first = '<option value="">————请选择————</option>';
                var others = '';
                for (var i = 0; i < data.length; i++) {
                    //console.log(data[i]);
                    if (setDef && data[i].data_value == defValue) {
                        first = '<option value="' + data[i].data_value + '">' + data[i].data_value + '：' + data[i].data_label + '</option>';
                        others += '<option value="">——请选择——</option>';
                    } else {
                        others += '<option value="' + data[i].data_value + '">' + data[i].data_value + '：' + data[i].data_label + '</option>'
                    }
                }
                $('#' + id).html(first + others);
                //console.log($('#' + id).html());
                //重新渲染select标签中的内容
                form.render();
            } else {
              alert('加载数据字典【' + dictKey + '】失败')
            }
          }
        });

    })
}

/*function loadDicts($, form) {
    selects = $('.dict-select')
    $.each(selects, function(index, select){
        loadDict($, form, select)
    })
}*/

function loadDict(select) {
    const $ = layui.jquery
    const form = layui.form

    let id = select.id;
    let dictKey = $('#' + id).attr('dict-key');
    var setDef = false;
    var defValue = null;
    if (select.hasAttribute('def-value')) {
        setDef = true;
        defValue = $('#' + id).attr('def-value');
    }

    $.ajax({
      url: '/admin/dict/dictData/get?dictKey=' +dictKey,
      type: 'get',
      dataType: 'json',
      success: function (result) {
        if (result.success) {
            data = result.data;
            var first = '<option value="">————请选择————</option>';
            var others = '';
            for (var i = 0; i < data.length; i++) {
                if (setDef && data[i].data_value == defValue) {
                    first = '<option value="' + data[i].data_value + '">' + data[i].data_value + '：' + data[i].data_label + '</option>';
                    others += '<option value="">——请选择——</option>';
                } else {
                    others += '<option value="' + data[i].data_value + '">' + data[i].data_value + '：' + data[i].data_label + '</option>'
                }
            }
            $('#' + id).html(first + others);
            form.render();
        } else {
          alert('加载数据字典【' + dictKey + '】失败')
        }
      }
    });
}