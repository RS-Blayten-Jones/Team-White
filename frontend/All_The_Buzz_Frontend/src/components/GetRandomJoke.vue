<script lang="ts">
import axios from 'axios'
import { defineComponent } from 'vue'

export default defineComponent({
	name: 'GetRandomJoke',
		props: {
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
mounted() {
  console.log(this.apiData);
  this.GetRand();
},
methods: {
    GetRand() {
    axios.get(`http://localhost:8080/random-jokes/1`, {
      headers: {
        'Bearer': `${this.jwt}`
      }
    })
    .then(response => {
      console.log(response.data)
      console.log(response.data[0].content)
      this.apiData = response.data[0].content;
      this.msg = '';
    })
    .catch(error => {
      this.msg = "Error: Status Code = " + (error.response?.status || 'Unknown');
    })
  },
  isContentTypeOneLiner(): boolean {
    return (this.apiData &&
    this.apiData &&
    this.apiData.type === "one_liner");
  },
  isContentTypeqa(): boolean {
    return (this.apiData &&
    this.apiData &&
    this.apiData.type === "qa");
  },
}
});
</script>

<template>
	<div class="random-joke" >
		<div v-if="isContentTypeOneLiner()">
            {{ this.apiData.text }}
        </div>
        <div v-if="isContentTypeqa()">
            {{ this.apiData.question }}
        </div>
	</div>
</template>

<style>
.random-joke {
  background: #e3f2fd;           /* Light blue background */
  padding: 2rem 2.5rem;
  font-size: 1.5rem;               /* Larger font */
  color: #222;
  text-align: center;
}

.random-joke div {
  margin-bottom: 1rem;
  font-weight: 500;
}
</style>