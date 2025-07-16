function clearFormMessage() {
  const messageBox = document.getElementById("formMessage");
  if (messageBox) {
    messageBox.textContent = "";
    messageBox.classList.add("d-none");
    messageBox.classList.remove("error", "success");
  }
}

function showMeta(type) {
    const sections = ['meta-objects', 'meta-relationships', 'meta-performance', 'meta-visual', 'meta-scene'];
    sections.forEach(id => {
      const el = document.getElementById(id);
      if (el) el.classList.add('d-none');
    });
    const target = document.getElementById('meta-' + type);
    if (target) target.classList.remove('d-none');
  }

  function showMeta(panelId) {
    const sections = ["meta-visual", "meta-objects", "meta-relationships", "meta-scene", "meta-performance"];
    const buttons = document.querySelectorAll('.glass-btn');
  
    sections.forEach(id => document.getElementById(id)?.classList.add('d-none'));
    buttons.forEach(btn => btn.classList.remove('active'));
  
    document.getElementById(`meta-${panelId}`)?.classList.remove('d-none');
    event.target.classList.add('active');
  }
  
  const dropArea = document.getElementById('drop-area');
  const imageInput = document.getElementById('imageInput');
  const previewContainer = document.getElementById('previewContainer');
  const previewImage = document.getElementById('previewImage');
  const fileName = document.getElementById('fileName');
  const fileSize = document.getElementById('fileSize');
  const uploadPrompt = document.getElementById('uploadPrompt');
  
  function formatSize(bytes) {
    return (bytes / 1024 / 1024).toFixed(2) + " MB";
  }
  
  function handleFiles(files) {
    clearFormMessage(); 
    const file = files[0];
    if (file && file.type.startsWith('image/')) {
      const reader = new FileReader();
      reader.onload = e => {
        previewImage.src = e.target.result;
        previewContainer.classList.remove('d-none');
        uploadPrompt.classList.add('d-none');
        fileName.textContent = file.name;
        fileSize.textContent = formatSize(file.size);
      };
      reader.readAsDataURL(file);
    }
  }
  
  if (imageInput) {
    imageInput.addEventListener('change', () => handleFiles(imageInput.files));
  }
  
  if (dropArea) {
    dropArea.addEventListener('dragover', e => {
      e.preventDefault();
      dropArea.classList.add('dragover');
    });
  
    dropArea.addEventListener('dragleave', () => {
      dropArea.classList.remove('dragover');
    });
  
    dropArea.addEventListener('drop', e => {
      e.preventDefault();
      dropArea.classList.remove('dragover');
      const files = e.dataTransfer.files;
      imageInput.files = files;
      handleFiles(files);
    });
  }
  
  function clearPreview() {
    previewContainer.classList.add('d-none');
    uploadPrompt.classList.remove('d-none');
    imageInput.value = '';
  }
  
  function copyCaption() {
    const captionSpan = event.target.closest('.caption-box').querySelector('span');
    const copyButton = event.target;
  
    navigator.clipboard.writeText(captionSpan.innerText).then(() => {
      copyButton.textContent = "✅ Copied!";
      setTimeout(() => {
        copyButton.textContent = "📋 Copy";
      }, 1500);
    });
  }
  
  

  document.querySelector("form").addEventListener("submit", function (e) {
    const fileInput = document.getElementById("imageInput");
    const messageBox = document.getElementById("formMessage");
  
    if (!fileInput.files || fileInput.files.length === 0) {
      e.preventDefault();
      messageBox.textContent = "⚠️ Please upload an image before submitting.";
      messageBox.classList.remove("d-none");
      messageBox.classList.add("error");
      return;
    }

    const submitText = document.getElementById("submitBtnText");
    const submitSpinner = document.getElementById("submitSpinner");
    submitText.classList.add("d-none");
    submitSpinner.classList.remove("d-none");

    document.getElementById("submitBtn").disabled = true;
  
    messageBox.textContent = "";
    messageBox.classList.add("d-none");
  });
  
  
  