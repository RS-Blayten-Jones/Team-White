<script lang="ts">
import axios from 'axios'
import { defineComponent } from 'vue'

export default defineComponent({
	name: 'ApproveAndDeny',
		props: {
			id: {
				type: String,
				required: true
			},
			jwt: {
				type: String,
				required: true
			},
			category: {
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
		this.fetchData(this.id)
	},
	methods: {
		approveData() {
			axios.post(`http://localhost:8080/${this.category}/${this.id}/approve`, {}, {
				headers: {
					Bearer: `${this.jwt}`
				}
			})
			.then(response => {
				this.apiData = response.data;
				this.msg = '';
			})
			.catch(error => {
				this.msg = "Error: Status Code = " + (error.response?.status || 'Unknown');
			})
		},
		denyData() {
			axios.post(`http://localhost:8080/${this.category}/${this.id}/deny`, {}, {
				headers: {
					Bearer: `${this.jwt}`
				}
			})
			.then(response => {
				this.apiData = response.data;
				this.msg = '';
			})
			.catch(error => {
				this.msg = "Error: Status Code = " + (error.response?.status || 'Unknown');
			})
		}
	}
})
</script>
<template>
<button class="approve-btn" v-on:click="approveData()">
	<span>&#10003;</span> APPROVE
</button>
<button class="deny-btn" v-on:click="denyData()">
	<span>&#10006;</span> DENY
</button>
</template>