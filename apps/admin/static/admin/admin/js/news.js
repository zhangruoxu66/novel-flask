const $ = layui.jquery
const form = layui.form;

var E = window.wangEditor
var editor = new E('#newsContentEditor') // 两个参数也可以传入 elem 对象，class 选择器
// 自定义菜单配置
editor.customConfig.menus = [
    'head',  // 标题
    'bold',  // 粗体
    'fontSize',  // 字号
    'fontName',  // 字体
    'italic',  // 斜体
    'underline',  // 下划线
    'strikeThrough',  // 删除线
    'foreColor',  // 文字颜色
    //'backColor',  // 背景颜色
    //'link',  // 插入链接
    'list',  // 列表
    'justify',  // 对齐方式
    'quote',  // 引用
    'emoticon',  // 表情
    'image',  // 插入图片
    'table',  // 表格
    'code',  // 插入代码
    'undo',  // 撤销
    'redo'  // 重复
];
//开启debug模式
editor.customConfig.debug = true;
// 关闭粘贴内容中的样式
editor.customConfig.pasteFilterStyle = false
// 忽略粘贴内容中的图片
editor.customConfig.pasteIgnoreImg = true
// 使用 base64 保存图片
editor.customConfig.uploadImgShowBase64 = true;

// 上传图片到服务器
editor.customConfig.uploadFileName = 'file'; //设置文件上传的参数名称
//editor.customConfig.uploadImgServer = '/admin/file/upload'; //设置上传文件的服务器路径
editor.customConfig.uploadImgMaxSize = 2 * 1024 * 1024; // 将图片大小限制为 2M
editor.customConfig.uploadImgMaxLength = 2
//自定义上传图片事件
/*editor.customConfig.uploadImgHooks = {
    before: function (xhr, editor, files) {
        // console.log(localStorage.getItem("flask_redis_csrf_token"));
        // let $ = layui.jquery;
        // xhr.setRequestHeader('FLASK-CSRF-TOKEN', localStorage.getItem("flask_redis_csrf_token"))
        addHeaders(xhr);
    },
    success: function (xhr, editor, result) {
        console.log("上传成功");
        // csrfToken = xhr.getResponseHeader('CSRF_TOKEN');
        // if (csrfToken) {
        //     localStorage.setItem("flask_redis_csrf_token", csrfToken);
        // }
        dealWithComplete(xhr);
    },
    fail: function (xhr, editor, result) {
        console.log("上传失败,原因是" + result);
        if (result.msg) {
            layer.alert(result.msg);
        }
    },
    error: function (xhr, editor) {
        console.log("上传出错");
        dealWithError(xhr);
    },
    timeout: function (xhr, editor) {
        console.log("上传超时");
    },
    // 如果服务器端返回的不是 {errno:0, data: [...]} 这种格式，可使用该配置
    // （但是，服务器端返回的必须是一个 JSON 格式字符串！！！否则会报错）
    customInsert: function (insertImg, result, editor) {
        // 图片上传并返回结果，自定义插入图片的事件（而不是编辑器自动插入图片！！！）
        // insertImg 是插入图片的函数，editor 是编辑器对象，result 是服务器端返回的结果

        // 举例：假如上传图片成功后，服务器端返回的是 {url:'....'} 这种格式，即可这样插入图片：
        console.log(result);
        if (result.code == 0) {
            insertImg(result.data.src);
        }
        // if (result.code == 0) {
        //     var urls = result.data
        //     for (let url in urls) {
        //         insertImg(url)
        //     }
        // }
    }
};*/
//自己定义上传的方法
editor.customConfig.customUploadImg = function (files, insert) {
    var daw = new FormData();
    for (var i = 0; i < files.length; i++) {
        daw.append("files", files[i]);
    }
    index = layer.load(1, {
        shade: [0.1, '#fff'] //0.1透明度的白色背景
    });

    $.ajax({
        url: '/admin/file/weImgUpload',
        type: "POST",
        data: daw,
        async: false,
        cache: false,
        contentType: false,
        processData: false,
        success: function (res) {
            layer.close(index);
            if (res.code == 0) {
                let urls = res.data;
                for (let url of urls) {
                    // console.log(url);
                    insert(url);
                }
            } else {
                layer.alert(res.msg);
                return;
            }
        }
    });
};
editor.customConfig.onchange = function (html) {
    // html 即变化之后的内容
    $("#content").val(html);
}

editor.create();

function setEditorText() {
    editor.txt.html($("#content").val());
}

function loadCategories(elementId, defaultValue) {
    const $ = layui.jquery
    const form = layui.form

    $.ajax({
        url: '/admin/news_category/all',
        type: 'get',
        dataType: 'json',
        success: function (result) {
            if (result.success) {
                data = result.data;
                var content = '';
                for (var i = 0; i < data.length; i++) {
                    if (defaultValue && defaultValue == data[i].id) {
                        content += `<option value="${data[i].id}" selected>${data[i].name}</option>`
                    } else {
                        content += `<option value="${data[i].id}">${data[i].name}</option>`
                    }
                }
                $('#' + elementId).append(content);

                form.on('select(catIdOnchange)', function (data) {
                    // console.log(data.elem); //得到select原始DOM对象
                    // console.log(data.elem.id); //得到select id 属性
                    // console.log(data.elem.name); //得到select name 属性
                    // console.log(data.value); //得到被选中的值
                    // console.log(data.othis); //得到美化后的DOM对象
                    let catName = $(data.elem).find("option:selected").text();
                    if (catName != '直接选择或搜索选择') {
                        $("#cat_name").val(catName);
                        // console.log($("#cat_name").val());
                    } else {
                        $("#cat_name").val('');
                    }
                });

                form.render();
            } else {
                alert('加载新闻分类失败')
            }
        }
    });
}