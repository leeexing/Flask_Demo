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
  // let socket = io.connect('http://localhost:5006/test', {query: "client_name=kobe_2018&age=24", transports:['websocket']})
  // socket.on('connect', () => {
  //   console.log('*'.repeat(20))
  //   socket.emit('my event', {data: `I'm connected!`})
  // })

  // socket.on('my response', msg => {
  //   console.log(msg)
  //   socket_wrap.innerHTML = `<h1>连接次数：${msg.data}</h1>`
  // })

  // 添加数据
  let $input = $('.add')
  let $renderWrap = $('.item-title')
  $('.opr .btn').eq(3).on('click', e => {
    let title = $input.val()
    if (!title) return
    query('http://localhost:5002/api/todo', 'post', {title})
      .then(data => {
        console.log(data)
        if (data.result === 200) {
          $input.val('')
        }
      })
  })

  // 全部
  $('.opr .btn').eq(0).on('click', e => {
    query('http://localhost:5002/api/todos')
      .then(data => {
        console.log(data)
        let list = renderTodoList(data.data)
        $renderWrap.siblings().remove().end().after(list)
      })
  })

  // 只显示完成的
  $('.opr .btn').eq(1).on('click', e => {
    query('http://localhost:5002/api/todo/1')
      .then(data => {
        console.log(data)
        if (data.data) {
          let list = renderTodoList(data.data)
          $renderWrap.siblings().remove().end().after(list)
        } else {
          $renderWrap.siblings().remove().end().after('<li class="item">还没有完成一项，抓紧时间</li>')
        }
      })
  })

  // 未完成的
  $('.opr .btn').eq(2).on('click', e => {
    query('http://localhost:5002/api/todo/0')
      .then(data => {
        console.log(data)
        let list = renderTodoList(data.data)
        $renderWrap.siblings().remove().end().after(list)
      })
  })

  function renderTodoList(data) {
    let list = ''
    data.forEach(item => {
      list += `
      <li class="item">
        <input type="checkbox" ${item.status ? 'checked' : ''}>
        <span class="title">${item.title}</span>
        <time>${item.create_time}</time>
        ${item.status ? '<a class="btn primary delete">删除</a>' : '<a class="btn primary edit">编辑</a>'}
      </li>`
    })
    return list
  }

  $('.todo').on('click', '.delete', function(){
    let title = $(this).siblings('.title').text()
    console.log(title)
    query('http://localhost:5002/api/todo', 'delete', {title})
      .then(data => {
        console.log(data)
        if (data.result === 200) {
          $(this).parent().remove()
        }
      })
  })
})