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

    <!-- Graph Section for First Graph -->
    <section class="graph-section">
      <h2>Popularity Graph</h2>
      <div id="graph-container" ref="graph1"></div>
      <!-- This is where the first graph will be rendered -->
    </section>

    <!-- Graph Section for Second Graph -->
    <section class="graph-section">
      <h2>Interaction Graph</h2>
      <div id="graph-container-2" ref="graph2"></div>
      <!-- This is where the second graph will be rendered -->
    </section>
  </div>
</template>

<script>
import Plotly from "plotly.js-dist-min";

export default {
  name: "GraphPage",
  data() {
    return {
      graphData1: null,
      graphData2: null, // New data property for the second graph
    };
  },
  mounted() {
    this.fetchGraphData();
    this.fetchGraphData2(); // Fetch data for the second graph
  },
  methods: {
    goToHomePage() {
      this.$router.push({ name: "HomePage" });
    },
    async fetchGraphData() {
      try {
        const response = await fetch("/api/generate_pop_graph", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({}), // No need to specify graph_type
        });
        if (response.ok) {
          const data = await response.json();
          this.graphData1 = JSON.parse(data.graph);
          this.renderGraph();
        } else {
          console.error("Failed to generate popularity graph");
        }
      } catch (error) {
        console.error("Error:", error);
      }
    },
    async fetchGraphData2() {
      try {
        const response = await fetch("/api/generate_sent_graph", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({}), // No need to specify graph_type
        });
        if (response.ok) {
          const data = await response.json();
          this.graphData2 = JSON.parse(data.graph);
          this.renderGraph2();
        } else {
          console.error("Failed to generate sentiment graph");
        }
      } catch (error) {
        console.error("Error:", error);
      }
    },
    renderGraph() {
      if (this.graphData1) {
        const graphElement = this.$refs.graph1;
        Plotly.react(
          graphElement,
          this.graphData1.data,
          this.graphData1.layout
        );
      }
    },
    renderGraph2() {
      if (this.graphData2) {
        const graphElement2 = this.$refs.graph2;
        Plotly.react(
          graphElement2,
          this.graphData2.data,
          this.graphData2.layout
        );
      }
    },
  },
};
</script>

<style scoped>
/* Ensure the body and html can grow beyond the viewport */
html,
body {
  height: 100%;
  margin: 0;
  overflow-x: hidden; /* Prevent horizontal scrolling */
}

.homepage {
  background-image: url("@/assets/background2.jpg");
  background-size: cover;
  background-position: center;
  min-height: 100vh; /* Ensure the page takes full viewport height */
  color: white;
  text-align: center;
  overflow-y: auto; /* Enable vertical scrolling if content exceeds the viewport */
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
  position: relative;
  margin: 20px auto;
  width: 80%;
  max-width: 800px;
  color: white;
}

.graph-section h2 {
  font-size: 24px;
  margin-bottom: 20px;
}
</style>
