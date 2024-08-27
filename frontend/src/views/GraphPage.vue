<template>
  <div class="homepage">
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

    <!-- Graph Section -->
    <section class="graph-section">
      <h2>Graphs</h2>
      <div id="graph-container" ref="graph"></div>
      <!-- This is where the graph will be rendered -->
    </section>
  </div>
</template>

<script>
import Plotly from "plotly.js-dist-min";

export default {
  name: "GraphPage",
  data() {
    return {
      graphData: null,
    };
  },
  mounted() {
    this.fetchGraphData();
  },
  methods: {
    goToHomePage() {
      this.$router.push({ name: "HomePage" });
    },
    async fetchGraphData() {
      try {
        const response = await fetch("/api/generate_graph", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ graph_type: "cluster_chat_graph" }), // Ensure this matches your backend
        });
        if (response.ok) {
          const data = await response.json();
          this.graphData = data.graph;
          console.log("Graph data received:", this.graphData);
          this.renderGraph();
        } else {
          console.error("Failed to generate graph");
        }
      } catch (error) {
        console.error("Error:", error);
      }
    },
    renderGraph() {
      if (this.graphData) {
        const graphElement = this.$refs.graph;
        Plotly.react(
          graphElement,
          JSON.parse(this.graphData).data,
          JSON.parse(this.graphData).layout
        );
      }
    },
  },
};
</script>

<style scoped>
/* Add styles similar to your other pages to maintain consistency */
.homepage {
  background-image: url("@/assets/background2.jpg");
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
  transition: color 0.3s;
}

.navbar-links li a:hover {
  color: #f0c040; /* Optional: Change color on hover for better effect */
}

.graph-section {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 80%;
  max-width: 800px;
  color: white;
}

.graph-section h2 {
  font-size: 24px;
  margin-bottom: 20px;
}
</style>
