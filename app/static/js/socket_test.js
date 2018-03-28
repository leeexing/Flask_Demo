$(() => {
  console.log(`%c web socket `, 'background:#f90')

  const socket_wrap = document.querySelector('.socket-wrap')

  // 如果url后面接？username=leeing 这样的话，后面的query字段会被忽略掉
  let socket = io.connect('http://localhost:5006/test', {query: "client_name=leeing_0712&age=23", transports:['websocket'], timeout:30000})
  socket.on('connect', () => {
    console.log('*'.repeat(20))
    socket.emit('my event', {data: `I'm connected!`})
  })

  socket.on('my response', msg => {
    console.log(msg)
    socket_wrap.innerHTML = `<h1>连接次数：${msg.data}</h1>`
  })


})