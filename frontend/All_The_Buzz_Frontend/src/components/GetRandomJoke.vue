<script lang="ts">
import axios from 'axios'
import { defineComponent } from 'vue'

export default defineComponent({
	name: 'GetRandomJoke',
		props: 
			jwt: {
				type: String,
				required: true
			}
		},
	data() {
		return {
			msg: "",
			apiData: {}
		}
	},

methods: {
    GetRand() {
    axios.get(`http://localhost:8081/random-joke/1`, {
      headers: {
        'Bearer': `${this.jwt}`
      }
    })
    .then(response => {
      this.apiData = response.data;
      this.msg = '';
    })
    .catch(error => {
      this.msg = "Error: Status Code = " + (error.response?.status || 'Unknown');
    });
  },
  isContentTypeOneLiner(): boolean {
    return this.apiData && this.apiData.content.type === "one-liner";
  }
});
</script>

<template>
	<div class="random-joke" >
		<div v-if="isContentTypeOneLiner()">
            {{ this.apiData.content.text }}
        </div>
        <div v-if="!isContentTypeOneLiner()">
            {{ this.apiData.content.question }}
        </div>
	</div>
</template>

<style>

</style>