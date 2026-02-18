document.addEventListener("DOMContentLoaded", () => {

    /* -------- Auto focus -------- */
    const nameInput = document.querySelector("input[name='name']");
    if (nameInput) nameInput.focus();

    /* -------- Mobile validation -------- */
    const mobileInput = document.querySelector("input[name='mobile']");
    if (mobileInput) {
        mobileInput.addEventListener("input", () => {
            mobileInput.value = mobileInput.value.replace(/\D/g, "").slice(0, 10);
        });
    }

    /* -------- Aadhaar validation -------- */
    const aadhaarInput = document.querySelector("input[name='aadhaar']");
    if (aadhaarInput) {
        aadhaarInput.addEventListener("input", () => {
            aadhaarInput.value = aadhaarInput.value.replace(/\D/g, "").slice(0, 12);
        });
    }

    /* -------- Signature Pad -------- */
    const canvas = document.getElementById("signaturePad");
    const clearBtn = document.getElementById("clearSign");
    const sigInput = document.getElementById("signatureData");
    const form = document.querySelector("form");

    if (canvas && sigInput && form) {
        const ctx = canvas.getContext("2d");
        let drawing = false;

        canvas.addEventListener("mousedown", () => drawing = true);
        canvas.addEventListener("mouseup", () => {
            drawing = false;
            ctx.beginPath();
        });
        canvas.addEventListener("mouseleave", () => {
            drawing = false;
            ctx.beginPath();
        });

        canvas.addEventListener("mousemove", e => {
            if (!drawing) return;

            const rect = canvas.getBoundingClientRect();
            ctx.lineWidth = 2;
            ctx.lineCap = "round";
            ctx.strokeStyle = "#000";

            ctx.lineTo(e.clientX - rect.left, e.clientY - rect.top);
            ctx.stroke();
            ctx.beginPath();
            ctx.moveTo(e.clientX - rect.left, e.clientY - rect.top);
        });

        if (clearBtn) {
            clearBtn.addEventListener("click", () => {
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                sigInput.value = "";
            });
        }

        /* -------- SIGNATURE MANDATORY CHECK -------- */
        form.addEventListener("submit", (e) => {
            const emptyCanvas = document.createElement("canvas");
            emptyCanvas.width = canvas.width;
            emptyCanvas.height = canvas.height;

            if (canvas.toDataURL() === emptyCanvas.toDataURL()) {
                e.preventDefault();
                alert("Signature is required before submitting the form.");
                return;
            }

            // ✅ FINAL FIX
            sigInput.value = canvas.toDataURL("image/png");
        });
    }
});
let stream = null;
let facingMode = "environment";

document.addEventListener("DOMContentLoaded", () => {

    document.getElementById("galleryBtn").onclick = () => {
        document.getElementById("galleryInput").click();
    };

    document.getElementById("cameraBtn").onclick = () => {
        openCamera();
    };

    document.getElementById("switchBtn").onclick = () => {
        switchCamera();
    };

    document.getElementById("captureBtn").onclick = () => {
        capturePhoto();
    };

    document.getElementById("retakeBtn").onclick = () => {
        retakePhoto();
    };
});

// ---------- CAMERA ----------
function openCamera() {
    navigator.mediaDevices.getUserMedia({
        video: { facingMode: facingMode }
    }).then(s => {
        stream = s;
        const video = document.getElementById("camera");
        video.srcObject = stream;
        video.classList.remove("d-none");

        document.getElementById("captureBtn").classList.remove("d-none");
        document.getElementById("switchBtn").classList.remove("d-none");
    }).catch(err => {
        alert("Camera access blocked or unavailable");
        console.error(err);
    });
}

function switchCamera() {
    stopCamera();
    facingMode = facingMode === "environment" ? "user" : "environment";
    openCamera();
}

function capturePhoto() {
    const video = document.getElementById("camera");
    const canvas = document.getElementById("photoCanvas");

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    canvas.getContext("2d").drawImage(video, 0, 0);

    canvas.toBlob(blob => {
        const file = new File([blob], "visitor.jpg", {
            type: "image/jpeg",
            lastModified: Date.now()
        });

        const dt = new DataTransfer();
        dt.items.add(file);
        document.getElementById("finalPhotoInput").files = dt.files;

        const img = document.getElementById("photoPreview");
        img.src = URL.createObjectURL(blob);
        img.classList.remove("d-none");

        document.getElementById("retakeBtn").classList.remove("d-none");
        document.getElementById("captureBtn").classList.add("d-none");

        stopCamera();
    }, "image/jpeg", 0.9);
}

function retakePhoto() {
    document.getElementById("photoPreview").classList.add("d-none");
    document.getElementById("retakeBtn").classList.add("d-none");
    document.getElementById("captureBtn").classList.remove("d-none");
    openCamera();
}

function stopCamera() {
    if (stream) {
        stream.getTracks().forEach(t => t.stop());
        stream = null;
    }
    document.getElementById("camera").classList.add("d-none");
}
