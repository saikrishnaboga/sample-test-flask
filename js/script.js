let mediaRecorder;
let recordedChunks = [];
let recordings = [];
let selectedRecording = null;
let wavesurfer;


function transcribe() {
    if (selectedRecording !== "") {
        const formData = new FormData();

        formData.append('audio', selectedRecording.blob);
        console.log(formData)
        fetch('http://127.0.0.1:5000/transcribe', {
            method: 'POST',
            body: formData,
            headers: {
                'Accept': 'application/json',
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log(data);
            document.getElementById('transcript').value = data.transcription;
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
}
