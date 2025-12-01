# Recipe Example Guidelines

- Keep recipe examples idiomatic for Dear ImGui and Slimgui. The preferred patterns should match how similar problems are solved in `src/c/imgui/imgui_demo.cpp`, even when the recipe is simplified for documentation.
- A recipe example should primarily be a single standalone example function. Use a separate state dataclass only when state is actually needed for the interaction being demonstrated.
- The function docstring is the primary explanation of the recipe. Write it as the text that should appear in the generated markdown page, with enough detail for both human readers and LLMs to understand what the example is doing and why.
- Keep the code focused on one pattern. Avoid defensive scaffolding or incidental abstractions unless they are part of the recipe being taught.
