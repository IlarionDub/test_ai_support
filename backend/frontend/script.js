

// const video = document.getElementById('video');
// const snap = document.getElementById('snap');
// const responseText = document.getElementById('response');

// navigator.mediaDevices.getUserMedia({
//     video: {
//         width: { ideal: 1920 },
//         height: { ideal: 1080 },
//         facingMode: { exact: "environment" }
//     }
// })
// .then(stream => {
//     video.srcObject = stream;
//     video.style.transform = 'scale(2.0)';
// })
// .catch(err => {
//     console.error("Помилка доступу до камери: ", err);
// });

// snap.addEventListener('click', async () => {
//     const canvas = document.createElement('canvas');
//     canvas.width = video.videoWidth;
//     canvas.height = video.videoHeight;
//     canvas.getContext('2d').drawImage(video, 0, 0);

//     const blob = await new Promise(resolve => canvas.toBlob(resolve, 'image/jpeg', 1.0));
//     const formData = new FormData();
//     formData.append('file', blob, 'photo.jpg');

//     const response = await fetch('/upload/', {
//         method: 'POST',
//         body: formData
//     });

//     const result = await response.json();
//     if (result.answer) {
//         responseText.textContent = result.answer;
//     } else {
//         responseText.textContent = "Помилка отримання відповіді.";
//     }
// });





const video = document.getElementById('video');
const snap = document.getElementById('snap');
const responseText = document.getElementById('response');

navigator.mediaDevices.getUserMedia({
    video: {
        width: { ideal: 1920 },
        height: { ideal: 1080 },
        facingMode: { exact: "environment" }
    }
})
.then(stream => {
    video.srcObject = stream;
    video.style.transform = 'scale(2.0)';
})
.catch(err => {
    console.error("Помилка доступу до камери: ", err);
});

snap.addEventListener('click', async () => {
    responseText.textContent = "Čakám na odpoveď...";  // ОЧИСТИТИ/ОНОВИТИ поле перед відправкою
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0);

    const blob = await new Promise(resolve => canvas.toBlob(resolve, 'image/jpeg', 1.0));
    const formData = new FormData();
    formData.append('file', blob, 'photo.jpg');

    const response = await fetch('/upload/', {
        method: 'POST',
        body: formData
    });

    const result = await response.json();
    if (result.answer) {
        responseText.textContent = result.answer;
    } else {
        responseText.textContent = "Помилка отримання відповіді.";
    }
});





