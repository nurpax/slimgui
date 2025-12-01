import DefaultTheme from 'vitepress/theme'
import type { Theme } from 'vitepress'
import MarkdownLinkInline from './MarkdownLinkInline.vue'
import './style.css'

export default {
	extends: DefaultTheme,
	enhanceApp({ app }) {
		app.component('MarkdownLinkInline', MarkdownLinkInline)
	},
} satisfies Theme
