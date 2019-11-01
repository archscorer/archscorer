module.exports = {
  "transpileDependencies": [
    "vuetify"
  ],
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
