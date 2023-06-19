<template> 
  <div>
    <h5  class="float-left">INGRESAR CONSULTA:</h5>
    <div class="input-group mb-3">
      <input
        type="text"
        class="form-control"
        placeholder="Escribir query"
        aria-label="Escribir query"
        aria-describedby="button-addon2"
        v-model="query"
      />
      <input
        type="text"
        class="form-control"
        placeholder="Buscar top K"
        aria-label="Buscar top K"
        aria-describedby="button-addon2"
        v-model="topk"
      />
      <div class="input-group-append">
        <button
          class="btn btn-outline-secondary"
          type="button"
          id="button-addon2"
          @click="search_query()"
        >
          Buscar
        </button>
      </div>
    </div>
    <div class="container cont-height">
      <div
        class="row h-100 justify-content-center align-items-center"
        v-if="loading"
      >
        <div
          class="spinner-border text-primary"
          style="width: 5rem; height: 5rem"
          role="status"
        >
          <span class="sr-only">Cargando</span>
        </div>
      </div>
      <div
        class="row w-100 mr-0 ml-0 justify-content-center"
        v-else
        v-for="tweet in tweets"
        v-bind:key="tweet"
      >
        <div class="tw-block-parent w-100">
          <div class="timeline-TweetList-tweet">
            <div class="timeline-Tweet">
              <div class="timeline-Tweet-author">
                <div class="TweetAuthor">
                  <a class="TweetAuthor-link" href="#channel"> </a
                  ><span class="TweetAuthor-avatar">
                    <div class="Avatar"></div></span>
                  <span class="TweetAuthor-name">{{ tweet.user_name }}</span
                  > 
                </div>
              </div>
              <div class="timeline-Tweet-text mb-4">
                {{ tweet.text }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "BrowserView",
  data() {
    return {
      query: "",
      topk: "",
      loading: false,
      tweets: [],
    };
  },
  methods: {
    search_query() {
      const body = {
        query: this.query,
      };
      this.loading = true;
      console.log(this.topk)
      axios.post(`http://127.0.0.1:8080/query/${+this.topk || 0}`, body).then((response) => {
        console.log(response);
        this.tweets = response.data;
        this.loading = false;
      });
    },
  },
};
</script>
