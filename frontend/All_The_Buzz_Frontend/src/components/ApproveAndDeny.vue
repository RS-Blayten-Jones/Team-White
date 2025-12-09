<script lang="ts">
import axios from 'axios'
import { defineComponent } from 'vue'
import { getCookie } from '@/utils/cookies'

export default defineComponent({
	name: 'ApproveAndDeny',
		props: {
			id: {
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
	methods: {
		approveData() {
			const token = getCookie('jwt')
			axios.post(`http://localhost:8080/${this.category}/${this.id}/approve`, {}, {
				headers: {
					Bearer: `${token}`
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
			const token = getCookie('jwt')
			axios.post(`http://localhost:8080/${this.category}/${this.id}/deny`, {}, {
				headers: {
					Bearer: `${token}`
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
<style scoped>
 .approve-btn {
  background-color: #28a745;
  color: white;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 600;
  transition: background-color 0.2s;
}

.approve-btn:hover {
  background-color: #218838;
}

.deny-btn {
  background-color: #dc3545;
  color: white;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 600;
  transition: background-color 0.2s;
}

.deny-btn:hover {
  background-color: #c82333;
}
</style>
