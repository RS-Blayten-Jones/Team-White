<template>
	<div class="daily-quote" :style="{ backgroundImage: `url(${bgImage})` }">
		<blockquote>{{ quote.content }}</blockquote>
		<cite>- {{ quote.author }}</cite>
		
	</div>
</template>
<script lang="ts">
import axios from 'axios'
import { defineComponent } from 'vue'

export default defineComponent({
	name: 'DailyQuote',
		props: {
			jwt: {
				type: String,
				required: true
			}
		},
	data() {
		return {
			msg: "",
			quote: {},
			bgImage: ''
		}
	},
	mounted() {
		console.log("token", this.jwt);
		this.getDailyQuote();
		const images = ['img1.jpg']; // Add your filenames here
  		const randomImg = images[Math.floor(Math.random() * images.length)];
  		this.bgImage = `/dailyquote/${randomImg}`;
	},
	methods: {
		getDailyQuote() {
			console.log(this.jwt);
			axios.get(`http://localhost:8081/daily-quotes`, {
				headers: {
					'Bearer': `${this.jwt}`,
					'Content-Type': 'application/json'
        		}
			}).then(response => {
				this.quote = response.data;
				this.msg = '';
			}).catch(error => {
				this.msg = "Error: Status Code = " + (error.response?.status || 'Unknown');
			})
		}
	}
})
</script>

<style scoped>
.daily-quote blockquote, .daily-quote cite {
  -webkit-text-stroke: 1px white;
}
.daily-quote {
  aspect-ratio: 1/1; /* modern browsers */
  background-size: cover;
  background-position: center;
  overflow: hidden;
}
.daily-quote {
	background-size: cover;
  	background-position: center;
	flex:1;
	text-align: center;
	font-size: 3rem;
	color: var(--text-primary, #222);
	margin: 2rem 0;
	background: #d1c1e9ff;
	padding: 1.5rem 2rem;
	font-weight: bold;
	
}

blockquote {
	font-style: italic;
	margin-bottom: 0.5rem;
}
cite {
	display: block;
	color: var(--text-secondary, #666);
	font-size: 1.7rem;
}
</style>
