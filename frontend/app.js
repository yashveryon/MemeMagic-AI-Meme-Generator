const uploadInput = document.getElementById("fileInput");
const generateBtn = document.getElementById("generateBtn");
const loading = document.getElementById("loading");
const result = document.getElementById("result");
const memeImage = document.getElementById("memeImage");
const downloadLink = document.getElementById("downloadLink");

const editBtn = document.getElementById("editCaptionToggleBtn");
const editBox = document.getElementById("editCaptionBox");
const captionInput = document.getElementById("editCaptionInput");
const saveBtn = document.getElementById("saveCaptionBtn");

const shareBtn = document.getElementById("shareBtn");
const socialOptions = document.getElementById("socialOptions");
const whatsappLink = document.getElementById("shareWhatsapp");
const facebookLink = document.getElementById("shareFacebook");
const instagramLink = document.getElementById("shareInstagram");

const tempSlider = document.getElementById("temperatureSlider");
const tempValueDisplay = document.getElementById("tempValue");

// Update displayed temperature value as slider moves
tempSlider.addEventListener("input", () => {
  tempValueDisplay.textContent = tempSlider.value;
});

let latestUploadedFile = null;
let latestCaption = "";

// Handle meme generation
generateBtn.addEventListener("click", async () => {
  const file = uploadInput.files[0];
  if (!file) {
    alert("Please choose an image first.");
    return;
  }

  latestUploadedFile = file;

  const formData = new FormData();
  formData.append("file", file);
  formData.append("temperature", tempSlider.value);  // 🔥 Use slider value

  loading.classList.remove("hidden");
  result.classList.add("hidden");
  editBox.classList.add("hidden");
  shareBtn.classList.add("hidden");
  socialOptions.classList.add("hidden");

  try {
    const response = await fetch("/meme/generate", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) throw new Error("Server returned an error");

    const imageURL = "/memes/output_meme.jpg?t=" + new Date().getTime();
    memeImage.src = imageURL;
    downloadLink.href = imageURL;

    latestCaption = response.headers.get("X-Caption") || "Your AI-generated caption";
    console.log("📩 Caption from backend:", latestCaption);

    loading.classList.add("hidden");
    result.classList.remove("hidden");
    shareBtn.classList.remove("hidden");

    const fullImageURL = window.location.origin + memeImage.src;
    const encodedText = encodeURIComponent("Check out this AI-generated meme! 😂");

    whatsappLink.href = `https://api.whatsapp.com/send?text=${encodedText}%20${encodeURIComponent(fullImageURL)}`;
    facebookLink.href = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(fullImageURL)}`;
    instagramLink.href = "#";

  } catch (error) {
    console.error("❌ Fetch error:", error);
    loading.classList.add("hidden");
    alert("Something went wrong while generating the meme.\n\n" + error.message);
  }
});

// Show edit caption box
editBtn.addEventListener("click", () => {
  captionInput.value = latestCaption;
  editBox.classList.remove("hidden");
});

// Save custom caption and redraw meme
saveBtn.addEventListener("click", async () => {
  const editedCaption = captionInput.value.trim();
  if (!editedCaption || !latestUploadedFile) {
    alert("Please enter a caption and make sure an image is uploaded.");
    return;
  }

  const formData = new FormData();
  formData.append("file", latestUploadedFile);
  formData.append("custom_caption", editedCaption);
  formData.append("temperature", tempSlider.value);  // 🔥 Send slider value again

  loading.classList.remove("hidden");
  result.classList.add("hidden");
  editBox.classList.add("hidden");
  shareBtn.classList.add("hidden");
  socialOptions.classList.add("hidden");

  try {
    const response = await fetch("/meme/generate", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) throw new Error("Server returned an error");

    const imageURL = "/memes/output_meme.jpg?t=" + new Date().getTime();
    memeImage.src = imageURL;
    downloadLink.href = imageURL;

    latestCaption = editedCaption;

    loading.classList.add("hidden");
    result.classList.remove("hidden");
    shareBtn.classList.remove("hidden");

    const fullImageURL = window.location.origin + memeImage.src;
    const encodedText = encodeURIComponent("Check out this AI-generated meme! 😂");

    whatsappLink.href = `https://api.whatsapp.com/send?text=${encodedText}%20${encodeURIComponent(fullImageURL)}`;
    facebookLink.href = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(fullImageURL)}`;
    instagramLink.href = "#";

  } catch (error) {
    console.error("❌ Error updating caption:", error);
    loading.classList.add("hidden");
    alert("Something went wrong while applying the edited caption.");
  }
});

// Toggle display of share links
shareBtn.addEventListener("click", () => {
  socialOptions.classList.toggle("hidden");
});
