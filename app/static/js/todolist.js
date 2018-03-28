console.groupCollapsed('我们要做什么')
console.log('项目：待办事项')
console.log('英文名：TODOLIST')
console.log('功能：实现添加、修改、刷选、删除功能')
console.log('数据库：Mongodb')
console.groupEnd()

$(() => {
  // socket连接
  const socket_wrap = document.querySelector('.socket')

  // 如果url后面接？username=leeing 这样的话，后面的query字段会被忽略掉
  let socket = io.connect('http://localhost:5006/test', {query: "username=kobe&age=24", transports:['websocket'], timeout:30000})
  socket.on('connect', () => {
    console.log('*'.repeat(20))
    socket.emit('my event', {data: `I'm connected!`})
  })

  // socket.on('my response', msg => {
  //   console.log(msg)
  //   socket_wrap.innerHTML = `<h1>连接次数：${msg.data}</h1>`
  // })

  // 添加数据
  let $input = $('.add')
  $('.opr .btn').eq(3).on('click', e => {
    let title = $input.val()
    if (!title) return
    query('http://localhost:5002/api/todo', 'post', {title, status: false})
      .then(data => {
        console.log(data)
        if (data.result === 200) {
          $input.val('')
        }
      })
  })


})