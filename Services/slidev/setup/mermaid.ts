import { defineMermaidSetup } from '@slidev/types'

export default defineMermaidSetup(() => {
  return {
    flowchart: {
      nodeSpacing: 20,
      rankSpacing: 20,
      padding: 0,
      curve: 'linear',
      subGraphTitleMargin: {
        top: 0,
        bottom: 0,
      },
      defaultRenderer: 'dagre-d3',
    },
  }
})
