<template>
	<a
		v-if="markdownUrl"
		class="markdown-link-inline"
		:href="markdownUrl"
		target="_blank"
		rel="noreferrer"
	>
		(.md)
	</a>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useData } from 'vitepress'

function resolveMarkdownPageURL(url: string, base: string) {
	const { origin, pathname } = new URL(url)
	const pathnameWithoutTrailingSlash = pathname.replace(/\/+$/, '')
	const lastSlashIndex = pathnameWithoutTrailingSlash.lastIndexOf('/')
	const lastDotIndex = pathnameWithoutTrailingSlash.lastIndexOf('.')

	let cleanedPath = pathnameWithoutTrailingSlash
	if (cleanedPath.endsWith('.md.html')) {
		cleanedPath = cleanedPath.slice(0, -5)
	} else if (lastDotIndex > lastSlashIndex && pathnameWithoutTrailingSlash.endsWith('.html')) {
		cleanedPath = pathnameWithoutTrailingSlash.slice(0, lastDotIndex)
	}

	const normalizedBase = base.replace(/\/+$/, '') || '/'
	if (!cleanedPath || cleanedPath === '/' || cleanedPath === normalizedBase) {
		// The plugin skips generating /index.md, so don't render a broken link on the homepage.
		return ''
	}

	return `${origin}${cleanedPath}.md`
}

const { site } = useData()

const markdownUrl = computed(() => {
	if (typeof window === 'undefined') return ''
	return resolveMarkdownPageURL(window.location.href, site.value.base)
})
</script>

<style scoped>
.markdown-link-inline {
	margin-left: 12px;
	font-size: 12px;
	color: var(--vp-c-text-2);
	text-decoration: underline;
	text-underline-offset: 2px;
	white-space: nowrap;
	position: relative;
	top: -2px;
}

.markdown-link-inline:hover {
	color: var(--vp-c-brand-1);
}
</style>
