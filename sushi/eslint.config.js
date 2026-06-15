import pluginVue from 'eslint-plugin-vue'
import globals from 'globals'
import js from '@eslint/js'

export default [
  // 1. Base JS and Vue structures
  js.configs.recommended,
  ...pluginVue.configs['flat/recommended'],

  // 2. Global ignores
  {
    ignores: ['dist', 'node_modules', '.nuxt', '.output']
  },

  // 3. Environment & Core Standard JS Rules
  {
    languageOptions: {
      ecmaVersion: 'latest',
      sourceType: 'module',
      globals: {
        ...globals.browser,
        ...globals.node
      }
    },
    rules: {
      // --- The Core Standard JS Ruleset ---
      'semi': ['error', 'never'], // No semicolons
      'quotes': ['error', 'single', { 'avoidEscape': true }], // Single quotes exclusively
      'indent': ['error', 2, { 'SwitchCase': 1 }], // Strict 2-space tabs
      'comma-dangle': ['error', 'never'], // No trailing commas
      'space-before-function-paren': ['error', 'always'], // space after function name
      'keyword-spacing': ['error', { 'before': true, 'after': true }], // if (), else {} spacing
      'space-infix-ops': 'error', // x = y instead of x=y
      'no-trailing-spaces': 'error', // Clean up line ends
      'object-curly-spacing': ['error', 'always'], // { box } instead of {box}
      'arrow-spacing': ['error', { 'before': true, 'after': true }], // () => {}

      // --- Vue Specific Spacing Adjustments ---
      'vue/html-indent': ['error', 2],
      'vue/html-quotes': ['error', 'double'], // Standard HTML template attributes use double quotes
      'vue/max-attributes-per-line': 'off',
      'vue/multi-word-component-names': 'off'
    }
  }
]
