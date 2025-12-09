<template>
	<div class="daily-quote" :style="{ backgroundImage: `url(${bgImage})` }">
		<blockquote>{{ quote.content }}</blockquote>
		<cite>- {{ quote.author }}</cite>
		
	</div>
</template>
<script lang="ts">
import axios from 'axios'
import { defineComponent } from 'vue'
import { getCookie } from '@/utils/cookies'

export default defineComponent({
	name: 'DailyQuote',
	data() {
		return {
			msg: "",
			quote: {},
			bgImage: ''
		}
	},
	mounted() {
		this.getDailyQuote();
		const images = ['img1.jpg','img2.jpg','img3.jpg','img4.jpg']; // Add your filenames here
  		const randomImg = images[Math.floor(Math.random() * images.length)];
  		this.bgImage = `/dailyquote/${randomImg}`;
	},
	methods: {
		getDailyQuote() {
			const token = getCookie('jwt')
			axios.get(`http://localhost:8080/daily-quotes`, {
				headers: {
					'Bearer': `${token}`,
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
  aspect-ratio: 1/1;                /* Always square */                  /* Height controlled by aspect-ratio */
  background-size: cover;           /* Crop to fill square */
  background-position: center;      /* Center image */
  background-repeat: no-repeat;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  
  align-items: center;
  text-align: center;
  font-size: 3rem;
  color: var(--text-primary, #222);
  margin: 2rem 0;
  background: #d1c1e9ff;
  padding: 1.5rem 2rem;
  font-weight: bold;
  flex: 1;    
  width: 100%; /* Or a specific width */
  height: 100%;                       /* Allow flex scaling */
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
