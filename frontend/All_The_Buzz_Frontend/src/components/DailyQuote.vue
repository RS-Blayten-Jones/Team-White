<template>
	<div class="daily-quote">
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
			quote: {}
		}
	},
	mounted() {
		console.log("token", this.jwt);
		this.getDailyQuote()
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
