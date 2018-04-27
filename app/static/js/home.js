$(() => {
  console.log(`%c Flask_Demo 首页 `, 'background:#ff85c0;color:#fff')

  let input_file = document.querySelector('#file')
  input_file.onchange = e => {
    console.log(e.target.files)
    let files = Array.from(e.target.files)
    let formData = new FormData()
    if (files) {
      formData.set('avatar', files[0])
    } else {
      return false
    }
    // let fileData = upload(e.target.files)
    setAvatar(formData)
  }

  let upload_btn = document.querySelector('.upload')
  upload_btn.onclick = () => {
    input_file.click()
  }

  function setAvatar(formData) {
    console.log(formData)
    console.log(formData.get('avatar'))
    $.ajax({
      url: 'http://localhost:5002/api/user/setavatar',
      type: 'POST',
      headers: {
        Authorization: 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1MjQ4MDgzMjQsIm5iZiI6MTUyNDgwODMyNCwianRpIjoiZDAxODg1NTItMGJhMy00MjZjLWIzNjItOGU2MzY2YTFhMmU2IiwiZXhwIjoxNTI0ODk0NzI0LCJpZGVudGl0eSI6WzIsImxlZWluZyJdLCJmcmVzaCI6ZmFsc2UsInR5cGUiOiJhY2Nlc3MiLCJ1c2VyX2NsYWltcyI6Mn0._3ejXG5ft31qnwpVjXsIrs2FIhU0-7glRRASNdwEb-Y',
      },
      data: formData,
      enctype: 'multipart/form-data',
      // 告诉jQuery不要去处理发送的数据
      processData : false, 
      // 告诉jQuery不要去设置Content-Type请求头
      contentType : false,
      success(data) {
        console.log(data)
      },
      error(err) {
        console.log(err)
      }
    })
  }
})