<template>
	<div class="daily-quote">
		<blockquote>"The only way to do great work is to love what you do."</blockquote>
		<cite>- Steve Jobs</cite>
	</div>
</template>

<script setup lang="ts">
// No logic needed for hardcoded quote
</script>

<style scoped>
.daily-quote {
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
