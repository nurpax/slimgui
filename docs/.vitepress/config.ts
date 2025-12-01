import { defineConfig } from 'vitepress'
import Token from 'markdown-it/lib/token.mjs'
import llmstxt from 'vitepress-plugin-llms'

function installApiSignatureContainer(md: any) {
	const marker = ':::'
	const containerName = 'api-signature'

	function extractDocParts(content: string) {
		const codeMatch = content.match(/```python\s*\n([\s\S]*?)\n```/)
		const python = codeMatch ? codeMatch[1].trimEnd() : content.trim()
		const lines = python.split('\n')
		let docStart = -1
		let quote = ''

		for (let i = 0; i < lines.length; i++) {
			const trimmed = lines[i].trim()
			if (trimmed === '"""' || trimmed === "'''") {
				docStart = i
				quote = trimmed
				break
			}
		}

		if (docStart === -1) {
			return { signature: python.trim(), docstring: '' }
		}

		let docEnd = lines.length
		for (let i = docStart + 1; i < lines.length; i++) {
			if (lines[i].trim() === quote) {
				docEnd = i
				break
			}
		}

		const signature = lines.slice(0, docStart).join('\n').trimEnd()
			.replace(/:$/, '')
		const docstring = lines
			.slice(docStart + 1, docEnd)
			.map((line) => line.startsWith('    ') ? line.slice(4) : line)
			.join('\n')
			.trim()

		return { signature, docstring }
	}

	md.block.ruler.before('fence', 'api-signature', (state: any, startLine: number, endLine: number, silent: boolean) => {
		const start = state.bMarks[startLine] + state.tShift[startLine]
		const max = state.eMarks[startLine]
		const line = state.src.slice(start, max).trim()

		if (line !== `${marker} ${containerName}`) return false
		if (silent) return true

		let nextLine = startLine + 1
		while (nextLine < endLine) {
			const nextStart = state.bMarks[nextLine] + state.tShift[nextLine]
			const nextMax = state.eMarks[nextLine]
			const nextText = state.src.slice(nextStart, nextMax).trim()
			if (nextText === marker) break
			nextLine += 1
		}

		if (nextLine >= endLine) return false

		const contentStart = state.bMarks[startLine + 1] + state.tShift[startLine + 1]
		const contentEnd = state.eMarks[nextLine - 1]
		const token = state.push('api_signature_block', 'div', 0)
		token.block = true
		token.map = [startLine, nextLine]
		token.content = state.src.slice(contentStart, contentEnd)

		state.line = nextLine + 1
		return true
	}, { alt: ['paragraph', 'reference', 'blockquote', 'list'] })

	md.renderer.rules.api_signature_block = (tokens: any, idx: number, options: any, env: any) => {
		const { signature, docstring } = extractDocParts(tokens[idx].content)
		const signatureHtml = md.render(`\`\`\`python\n${signature}\n\`\`\``, env)
		const docstringHtml = docstring
			? `<div class="api-signature__doc">\n${md.render(docstring, env)}</div>`
			: ''
		return `<div class="api-signature">\n${signatureHtml}${docstringHtml}\n</div>\n`
	}
}

export default defineConfig({
  title: "Slimgui",
  description: "Slimgui bindings and examples",
  base: "/slimgui/",
  head: [['link', { rel: 'icon', href: 'data:,' }]],
  outDir: "dist",
	vite: {
		plugins: [llmstxt({ injectLLMHint: false })],
	},
	markdown: {
		config(md) {
			installApiSignatureContainer(md)

			const orig = md.renderer.render.bind(md.renderer)
			md.renderer.render = (tokens, options, env) => {
				let injected = false

				for (let i = 0; i < tokens.length; i++) {
					const token = tokens[i]
					if (token?.type !== 'heading_open') continue
					if (token.tag !== 'h1' && token.tag !== 'h2') continue

					const inline = tokens[i + 1]
					if (inline?.type === 'inline' && inline.children && !injected) {
						const htmlToken = new Token('html_inline', '', 0)
						htmlToken.content = ' <MarkdownLinkInline />'
						inline.children.push(htmlToken)
						injected = true
						break
					}
				}

				return orig(tokens, options, env)
			}
		},
	},
  themeConfig: {
    nav: [
      { text: "Home", link: "/" },
      { text: "Guide", link: "/guide/getting-started" },
      { text: "Recipes", link: "/recipes/" },
      { text: "API Reference", link: "/api/imgui" }
    ],
    sidebar: [
      {
        text: "Guide",
        items: [
          { text: "Introduction", link: "/" },
          { text: "Getting Started", link: "/guide/getting-started" },
          { text: "Typing", link: "/guide/typing" }
        ]
      },
      {
        text: "API Reference",
        items: [
          { text: "ImGui", link: "/api/imgui" },
          { text: "ImPlot", link: "/api/implot" }
        ]
      },
      {
        text: "Recipes",
        items: [
          { text: "Overview", link: "/recipes/" },
          { text: "Widgets", link: "/recipes/widgets" },
          { text: "Styles", link: "/recipes/styles" },
          { text: "Layout", link: "/recipes/layout" },
          { text: "ImPlot", link: "/recipes/implot" },
        ]
      },
    ]
  }
});
