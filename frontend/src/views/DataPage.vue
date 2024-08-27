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

    <!-- Display the list of CSV and TXT files -->
    <section class="file-display">
      <h2>Uploaded CSV and TXT Files:</h2>
      <ul>
        <li v-for="file in filesList" :key="file">{{ file }}</li>
      </ul>

      <!-- Show Graphs Button -->
      <button class="show-graphs-button" @click="showGraphs">
        Show Graphs
      </button>
    </section>
  </div>
</template>

<script>
export default {
  name: "DataPage",
  data() {
    return {
      filesList: this.$route.params.files || [], // Correctly access the files passed from HomePage
    };
  },
  methods: {
    goToHomePage() {
      this.$router.push({ name: "HomePage" });
    },
    showGraphs() {
      this.$router.push({ name: "GraphPage" });
    },
  },
};
</script>

<style scoped>
.homepage {
  background-image: url("@/assets/background.jpg");
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

.file-display {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 80%;
  max-width: 600px;
}

.file-display h2 {
  font-size: 24px;
}

.show-graphs-button {
  margin-top: 20px;
  padding: 10px 20px;
  background-color: transparent;
  color: white;
  border: 2px solid white;
  border-radius: 5px;
  font-size: 18px;
  cursor: pointer;
}

.show-graphs-button:hover {
  background-color: white;
  color: #000;
}
</style>
