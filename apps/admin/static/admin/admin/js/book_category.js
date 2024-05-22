//function loadCategories($, form, elementId) {
function loadCategories(elementId) {
    const $ = layui.jquery
    const form = layui.form

    $.ajax({
          url: '/admin/book_category/all',
          type: 'get',
          dataType: 'json',
          success: function (result) {
            if (result.success) {
                data = result.data;
                var content = '';
                for (var i = 0; i < data.length; i++) {
                    content += '<option value="' + data[i].id + '">' + data[i].id + '：' + data[i].name + '</option>'
                }
                $('#' + elementId).append(content);
                form.render();
            } else {
              alert('加载小说分类失败')
            }
          }
        });
}