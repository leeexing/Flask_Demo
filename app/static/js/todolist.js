console.groupCollapsed('我们要做什么')
console.log('项目：待办事项')
console.log('英文名：TODOLIST')
console.log('功能：实现添加、修改、刷选、删除功能')
console.log('数据库：Mongodb')
console.groupEnd()

$(() => {
  // 添加数据
  let $input = $('.add')
  $('.opr .btn').eq(3).on('click', e => {
    console.log(7878)
    let title = $input.val()
    if (!title) return
    console.log(title)
    $.post('http://localhost:5002/api/todo', {title}, data => {
      console.log(data)
    })
    // query('http://localhost:5002/api/todo', 'post', {title, status: false})
    //   .then(data => {
    //     console.log(data)
    //   })
  })
})