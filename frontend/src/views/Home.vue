<template>
  <div class="homepage">
    <!-- Navigation Bar -->
    <nav class="navbar">
      <div class="navbar-content">
        <h1 class="navbar-title" @click="goToHomePage">
          Junior High Sociogram
        </h1>
        <ul class="navbar-links">
          <li><a href="#">About</a></li>
          <li><a href="#">Graphs</a></li>
        </ul>
      </div>
    </nav>

    <!-- File Upload Section -->
    <section class="file-upload">
      <h2>File Upload</h2>
      <p>Upload the game data to get started</p>
      <input
        type="file"
        ref="fileInput"
        @change="handleFileUpload"
        style="display: none"
      />
      <button class="upload-button" @click="triggerFileInput">
        Upload File
      </button>
    </section>
  </div>
</template>

<script>
export default {
  name: "HomePage",
  data() {
    return {
      selectedFile: null,
    };
  },
  methods: {
    triggerFileInput() {
      this.$refs.fileInput.click();
    },
    handleFileUpload(event) {
      this.selectedFile = event.target.files[0];
      this.uploadFile();
    },
    async uploadFile() {
      if (!this.selectedFile) {
        alert("Please select a file first");
        return;
      }

      const formData = new FormData();
      formData.append("file", this.selectedFile);

      try {
        const response = await fetch("/api/upload", {
          method: "POST",
          body: formData,
        });

        if (response.ok) {
          const data = await response.json();
          if (data.files && data.files.length > 0) {
            this.$router.push({
              name: "DataPage",
              params: { files: data.files }, // Correctly pass files as route params
            });
          } else {
            alert("No CSV or TXT files found in the uploaded ZIP.");
          }
        } else {
          alert("Error uploading file");
        }
      } catch (error) {
        console.error("Error uploading file:", error);
        alert("Error uploading file");
      }
    },
    goToHomePage() {
      this.$router.push({ name: "HomePage" });
    },
  },
};
</script>

<style scoped>
.homepage {
  background-image: url("@/assets/home.jpg");
  background-size: cover;
  background-position: center;
  height: 100vh;
  color: white;
  text-align: center;
}

.navbar {
  background-color: rgba(76, 39, 39, 0.8);
  padding: 20px;
}

.navbar-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.navbar-title {
  font-size: 32px;
  color: white;
  margin: 0;
  cursor: pointer;
}

.navbar-links {
  list-style-type: none;
  padding: 0;
  margin: 0;
  display: flex;
}

.navbar-links li {
  margin-left: 20px;
}

.navbar-links li a {
  color: white;
  text-decoration: none;
  font-size: 18px;
}

.file-upload {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.file-upload h2 {
  font-size: 24px;
}

.upload-button {
  margin-top: 10px;
  padding: 10px 20px;
  background-color: transparent;
  color: white;
  border: 2px solid white;
  border-radius: 5px;
  font-size: 18px;
  cursor: pointer;
}

.upload-button:hover {
  background-color: white;
  color: #000;
}

.uploaded-files {
  margin-top: 20px;
  text-align: left;
}

.uploaded-files h3 {
  font-size: 20px;
  color: white;
}

.uploaded-files ul {
  list-style-type: none;
  padding: 0;
}

.uploaded-files li {
  color: white;
  font-size: 16px;
  margin: 5px 0;
}
</style>
