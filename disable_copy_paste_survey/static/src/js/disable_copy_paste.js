document.addEventListener('DOMContentLoaded', function () {

   let secondsLeft = 30;
        const countdownElement = document.getElementById('countdown');

        const countdownInterval = setInterval(function () {
            secondsLeft--;
            if (countdownElement) {
                countdownElement.textContent = secondsLeft;
            }

            if (secondsLeft <= 0) {
                clearInterval(countdownInterval);

                // Attempt to close the tab (won't work unless opened via JS)
                window.open('', '_self');
                window.close();

                // Fallback: redirect to homepage
                window.location.href = '/web'; // or '/' if it's a public site
            }
        }, 1000);
  

    function requestFullScreenAndStartAssessment(event) {
        event.preventDefault(); // Prevent default form submission temporarily

        var elem = document.documentElement;

        function goFullScreen() {
            if (elem.requestFullscreen) {
                elem.requestFullscreen();
            } else if (elem.mozRequestFullScreen) {
                elem.mozRequestFullScreen();
            } else if (elem.webkitRequestFullscreen) {
                elem.webkitRequestFullscreen();
            } else if (elem.msRequestFullscreen) {
                elem.msRequestFullscreen();
            } else {
                console.error("Fullscreen API is not supported by this browser.");
                alert("Your browser does not support full-screen mode.");
                return;
            }
        }

        goFullScreen();

        // Delay form submission slightly to allow full-screen to activate
//        setTimeout(function () {
//            event?.target?.closest("form").submit(); // Proceed with form submission
//        }, 500); // Adjust delay if needed
    }

    function disableCopyPaste() {
        document.querySelectorAll('.o_survey_form input, .o_survey_form textarea').forEach(function (element) {
            element.addEventListener('copy', function (e) {
                e.preventDefault();
                reportCopyPaste();
                alert("Copy-Paste is disabled for this assessment.");
                
            });
            element.addEventListener('paste', function (e) {
                e.preventDefault();
                reportCopyPaste();
                alert("Copy-Paste is disabled for this assessment.");
                
            });
            element.addEventListener('cut', function (e) {
                e.preventDefault();
                reportCopyPaste();
                alert("Copy-Paste is disabled for this assessment.");
                
            });
        });

        document.addEventListener('contextmenu', function (e) {
            e.preventDefault();
            alert("Right-click is disabled for this assessment.");
        });

        document.addEventListener('keydown', function (e) {
            if ((e.ctrlKey || e.metaKey) && (e.key === 'c' || e.key === 'v' || e.key === 'x' || e.key === 'a')) {
                e.preventDefault();
                reportCopyPaste();
                alert("Copy-Paste is disabled for this assessment.");
                
            }
        });
    }

    function detectFocusLoss() {
        let lastAlertTime = 0;
        const alertCooldown = 5000; // 5 seconds cooldown
    
        document.addEventListener("visibilitychange", function () {
            if (document.hidden) {
                const now = Date.now();
                if (now - lastAlertTime > alertCooldown) {
                    lastAlertTime = now;
                    console.warn("Focus lost detected. Showing warning...");
                    
                    setTimeout(() => {
                        alert("Warning: You switched tabs or minimized the window. This may be considered suspicious behavior.");
                        reportFocusLoss();
                    }, 200); // Small delay to ensure real loss
                }
            }
        });
    
        window.addEventListener("blur", function () {
            const now = Date.now();
            if (now - lastAlertTime > alertCooldown) {
                lastAlertTime = now;
                console.warn("Blur event detected. Possible focus loss.");
                
                setTimeout(() => {
                    //alert("Warning: You switched tabs or minimized the window. This may be considered suspicious behavior.");
                    reportFocusLoss();
                }, 200);
            }
        });
    }
    function detectTabSwitch() {
        let lastTime = performance.now();
        let lastAlertTime = 0;
        const alertCooldown = 5000; // 5 seconds cooldown
    
        function checkFocus() {
            let now = performance.now();
            if (now - lastTime > 1000) { // If browser paused updates (inactive)
                const alertNow = Date.now();
                if (alertNow - lastAlertTime > alertCooldown) {
                    lastAlertTime = alertNow;
                    alert("Warning: You switched tabs or minimized the window.");
                    reportFocusLoss();
                }
            }
            lastTime = now;
            requestAnimationFrame(checkFocus);
        }
    
        requestAnimationFrame(checkFocus);
    }
    
    
    
    
    let mediaRecorder;
    let chunks = [];
    let stream;
    // function startVideoCapture() {
    //     if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
    //         console.error("getUserMedia is not supported in this browser.");
    //         alert("Your browser does not support webcam access. Please use a modern browser.");
    //         return;
    //     }

    //     navigator.mediaDevices.getUserMedia({ video: true })
    //         .then(function (stream) {
    //             var mediaRecorder = new MediaRecorder(stream);
    //             var chunks = [];

    //             mediaRecorder.ondataavailable = function (event) {
    //                 chunks.push(event.data);
    //             };

    //             mediaRecorder.onstop = function () {
    //                 var blob = new Blob(chunks, { type: 'video/mp4' });

    //                 var reader = new FileReader();
    //                 reader.readAsDataURL(blob);
    //                 reader.onloadend = function () {
    //                     var base64data = reader.result.split(',')[1];
    //                     fetch('/survey/video_capture', {
    //                         method: 'POST',
    //                         headers: { 'Content-Type': 'application/json' },
    //                         body: JSON.stringify({
    //                             assessment_id: getSurveyAndAssessmentId(),
    //                             video_data: base64data,
    //                             filename: 'survey_video_' + Date.now() + '.mp4'
    //                         })
    //                     })
    //                     .then(response => console.log("Video successfully uploaded."))
    //                     .catch(error => console.error("Error uploading video:", error));
    //                 };
    //             };

    //             mediaRecorder.start();
    //             setTimeout(function () {
    //                 mediaRecorder.stop();
    //             }, 10000);
    //         })
    //         .catch(function (error) {
    //             console.error("Error accessing webcam: ", error);
    //             alert("Webcam access is required for this assessment.");
    //         });
    // }
    function startVideoCapture() {
        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
            console.error("getUserMedia is not supported in this browser.");
            alert("Your browser does not support webcam access. Please use a modern browser.");
            return;
        }
        navigator.mediaDevices.getUserMedia({ video: {width: 1280, height: 720, frameRate: 30},audio: true })
            .then(function (mediaStream) {
                stream = mediaStream;
                mediaRecorder = new MediaRecorder(stream , { mimeType: 'video/webm; codecs=vp8, opus', videoBitsPerSecond: 2500000,audioBitsPerSecond: 128000});
                console.log(MediaRecorder.isTypeSupported('video/webm; codecs=vp9'));
                console.log(MediaRecorder.isTypeSupported('video/webm; codecs=vp8'));
                console.log(MediaRecorder.isTypeSupported('video/mp4; codecs=avc1'));
                mediaRecorder.ondataavailable = function (event) {
                    console.log(event.data.size);
                    if (event.data.size > 0) {
                        chunks.push(event.data);
                    }
                };
    
                mediaRecorder.onstop = function () {
                    if (chunks.length > 0) {
                        saveVideo();
                    }
                    cleanup();
                };
    
                mediaRecorder.start();
            })
            .catch(function (error) {
                console.error("Error accessing media devices:", error);
            });
    }

    function stopRecording() {
        if (mediaRecorder && mediaRecorder.state !== "inactive") {
            setTimeout(() => {
                mediaRecorder.stop();
            }, 500);
        }
    }
    function saveVideo() {
        const blob = new Blob(chunks, { type: 'video/webm' });
        const reader = new FileReader();
        reader.readAsDataURL(blob);
        reader.onloadend = function () {
            const base64data = reader.result.split(',')[1];
            fetch('/survey/video_capture', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    assessment_id: getSurveyAndAssessmentId(),
                    video_data: base64data,
                    filename: 'survey_video_' + Date.now() + '.webm'
                })
            })
            .then(response => console.log("Video successfully uploaded."))
            .catch(error => console.error("Error uploading video:", error));
        };
    }
    function cleanup() {
        if (stream) {
            stream.getTracks().forEach(track => track.stop());
        }
        //mediaRecorder = null;
        //chunks = [];
    }
    

    function reportFocusLoss() {
    	fetch('/survey/focus_loss', {
        	method: 'POST',
        	headers: { 'Content-Type': 'application/json' },
       		body: JSON.stringify({ assessment_id: getSurveyAndAssessmentId() })
    	});
    }
    function reportCopyPaste() {
        fetch('/survey/copy_paste_attempt', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ assessment_id: getSurveyAndAssessmentId() })
        });
    }

    function getSurveyAndAssessmentId() {
        let pathSegments = window.location.pathname.split("/");
        console.log("logger works");
        return {
                survey_id: pathSegments[2],       // Survey ID
                assessment_id: pathSegments[3],   // Assessment ID
            };
        
    }
    function stopRecordingOnCompletion() {
       
        const observer = new MutationObserver(() => {
            if (document.body.innerText.includes("Close") || document.body.innerText.includes("*")) {
                stopRecording();
                console.log("-------------------++++++++++++++++_-----------------");
                observer.disconnect(); // Stop observing after stopping the recording
            }
        });
        observer.observe(document.body, { childList: true, subtree: true });
	stopRecording();
	window.location.href = '/';
    }
    

    var startButton = document.querySelector("button[type='submit'][value='start']");
    if (startButton) {
        startButton.classList.remove("disabled"); // Ensure the button is enabled
        startVideoCapture();
        stopRecordingOnCompletion();
        startButton.addEventListener('click', requestFullScreenAndStartAssessment);

    }
    console.log(getSurveyAndAssessmentId());
    disableCopyPaste();
    detectFocusLoss();
    
    
    detectTabSwitch();
});
