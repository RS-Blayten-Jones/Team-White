<template>
	<div class="daily-quote">
		<blockquote>"The only way to do great work is to love what you do."</blockquote>
		<cite>- Steve Jobs</cite>
		{{ quote }}
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
			quote: {}
		}
	},
	mounted() {
 		console.log('JWT token received:', this.jwt);
 		this.getRandomQuote()
	},
	methods: {
		getRandomQuote() {
			console.log(this.jwt);
			axios.post(`http://localhost:8080/daily-quote`, {}, {
				headers: {
					'Bearer': `${this.jwt}`
				}
			})
			.then(response => {
				this.quote = response.data;
				this.msg = '';
			})
			.catch(error => {
				this.msg = "Error: Status Code = " + (error.response?.status || 'Unknown');
			})
		}
	}
})
</script>

<style scoped>
.daily-quote {
	flex:1;
	text-align: center;
	font-size: 1.25rem;
	color: var(--text-primary, #222);
	margin: 2rem 0;
	background: #d1c1e9ff;
	padding: 1.5rem 2rem;
}

blockquote {
	font-style: italic;
	margin-bottom: 0.5rem;
}
cite {
	display: block;
	color: var(--text-secondary, #666);
	font-size: 1rem;
}
</style>
