<template> 
  <div class="container">
    <nav class="navbar navbar-dark bg-dark md-5">
      <span class="navbar-brand mb-0 h1" href="#">TweetsSearch</span>
    </nav>
    <div class="container">
      <Search />
    </div>
  </div>
</template>

<script>
import Search from "./components/Search.vue";

export default {
  components: {
    Search
  }
};
</script>

<style>
@import url("https://fonts.googleapis.com/css2?family=Teko:wght@500&display=swap");

#app {
  font-family: Arial;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
