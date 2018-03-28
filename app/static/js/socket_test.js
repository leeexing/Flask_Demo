$(() => {
  console.log(`%c web socket `, 'background:#f90')

  const socket_wrap = document.querySelector('.socket-wrap')

  let socket = io.connect('http://localhost:5006/test', {timeout:30000})
  socket.on('connect', () => {
    console.log('*'.repeat(20))
    socket.emit('my event', {data: `I'm connected!`})
  })

  socket.on('my response', msg => {
    console.log(msg)
    socket_wrap.innerHTML = `<h1>连接次数：${msg.data}</h1>`
  })
})