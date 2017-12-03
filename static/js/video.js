
function main() {
  let video = document.getElementById('video')
  // let canvas = document.createElement('canvas')
  let canvas = document.getElementById('canvas')
  // let image = document.getElementById('image')
  let started = false
  let sendRate = 8 // interval

  let constraints = {
    audio: false,
    video: true
  }

  video.addEventListener('playing', (event) => {
    if (started) return

      started = true

    let width = video.videoWidth
    let height = video.videoHeight

    video.width = width
    video.height = height

    canvas.width = width
    canvas.height = height

  //   let context = canvas.getContext('2d')
  //   context.drawImage(video, 0, 0, width, height)
  //   let data = canvas.toDataURL('image/jpeg')

  //   // console.log(data)
  //   // post('/sendStaticImage', 'image='+data).then(() => {
  //   //     console.log('done')
  //   //   }
  //   // )
  //   $.post("/sendStaticImage", {
  //     image : data       
  //   }).done(function(response) {
  //   // alert("Server returned: " + response);
  // }).fail(function() {
  //   console.log("failed to return results");
  // });

  window.setInterval(() => {
    let context = canvas.getContext('2d')
    context.drawImage(video, 0, 0, width, height)
    let data = canvas.toDataURL('image/jpeg')
      // image.src = data

      // console.log(data)

      $.post("/sendStaticImage", {
        image: data       
      }).done(function(response) {
        var results = response
        console.log(results)
        var bestGuess=results[0]
        $('#guess').text(bestGuess)
        // alert("Server returned: " + response);
      }).fail(function() {
        console.log("failed to return results");
  });
}, sendRate * 1000)
})

  navigator.mediaDevices.getUserMedia(constraints)
  .then((stream) => {
    video.srcObject = stream
    video.play()
  })
}


window.onload = main
