module.exports = {
  "transpileDependencies": [
    "vuetify"
  ],
  outputDir: 'dist',
  assetsDir: 'static',
  devServer: {
    proxy: {
      '^/api': {
        target: 'http://localhost:8008',
        ws: true,
        changeOrigin: true
      }
    }
  }
}
