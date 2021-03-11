layui.config({
  version: '1614920675134' //为了更新 js 缓存，可忽略
});
function jump(){
  layer.msg('成功，正在跳转')
}

function add(){
  $.post({
    url: '',
    data: '',
    success:function (request){
      if (request.requestcode == 200){
        layui.use('layer',function (){
          layer.msg('添加成功')
        });
      }
    },
    error:function (){
      layui.use('layer',function (){
          layer.msg('添加成功')
        });

    },

  })
}

// layui.use([ 'layer'], function add(){
//   $.ajax({
//     type:'POST',
//     dataType:'json',
//     url:'/goodsinfo/1',
//     data:$('#form1').serialize(),
//     success:function (result){
//       if (result.resultCode == 200){
//         layer.msg('成功');
//       };
//     },
//     error:function (){
//       layer.msg('失败');
//     }
//
//   });
//
//
//
// });