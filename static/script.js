function validateForm() {
  var youtubeLink = document.getElementById("link").value.trim();
  var audioFile = document.getElementById("audio-file").value.trim();

  if (youtubeLink === "" && audioFile === "") {
    alert("Please enter a YouTube link or choose an audio file.");
    return false;
  }

  return true;
}
