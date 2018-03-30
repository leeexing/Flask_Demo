$(() => {
  // 听来自redis上面数据的变化

  let socket = io.connect('http://localhost:5006/SLIP_RING', {query: 'client_name=james_23&team=Cavaliers', timeout: 5000})
  let $slip = $('.slip-wrap')

  socket.on('connect', e => {
    console.log(7878)
    socket.emit('client_response', {data: 'SLIP_RING hi~'})
  })

  socket.on('server_response', msg => {
    console.log(msg)
    $slip.html(`<span>Title: ${msg.title}</span> -- Status: ${msg.status} -- Time: ${msg.create_time}`)
  })
})