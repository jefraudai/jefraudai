import { defineMermaidSetup } from '@slidev/types'

export default defineMermaidSetup(() => {
  return {
    flowchart: {
      nodeSpacing: 50,
      rankSpacing: 50,
      padding: 15,
      curve: 'basis',
    },
  }
})
